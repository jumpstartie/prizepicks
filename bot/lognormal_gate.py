"""Driftless lognormal / Black-Scholes digital gate for 15m up/down favorites.

Models P(YES) ≈ Φ(d2) for strike_type greater_or_equal (S_T ≥ K), r=q=0:
  d2 = (ln(S/K) - 0.5 σ_τ²) / σ_τ

Used as an *entry filter* on top of RTP-20: only take favorites the model
also likes (high side-prob + positive edge vs entry), then bank via TP /
pre-settle — not hold-to-settle hunting of 50¢ underdogs.
"""
from __future__ import annotations

import math
import os
from typing import Any

YEAR_SEC = 365.25 * 24 * 3600.0

LOGNORMAL_GATE = os.environ.get("LOGNORMAL_GATE", "0").lower() in (
    "1", "true", "yes", "on",
)
LOGNORMAL_MIN_EDGE = float(os.environ.get("LOGNORMAL_MIN_EDGE", "0.03"))
LOGNORMAL_MIN_PROB = float(os.environ.get("LOGNORMAL_MIN_PROB", "0.65"))
# realized = scale short-horizon lead vol to remaining τ; fixed = annualized σ
LOGNORMAL_SIGMA_MODE = os.environ.get("LOGNORMAL_SIGMA_MODE", "realized").lower()
LOGNORMAL_SIGMA = float(os.environ.get("LOGNORMAL_SIGMA", "0.80"))  # ann, fixed mode
LOGNORMAL_SIGMA_FLOOR = float(os.environ.get("LOGNORMAL_SIGMA_FLOOR", "0.40"))  # ann floor
LOGNORMAL_STRICT = os.environ.get("LOGNORMAL_STRICT", "0").lower() in (
    "1", "true", "yes", "on",
)
# When on, refuse bn=flat / weak venue (model alone is not enough)
LOGNORMAL_REQUIRE_AGREE = os.environ.get("LOGNORMAL_REQUIRE_AGREE", "0").lower() in (
    "1", "true", "yes", "on",
)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def digital_yes_prob(spot: float, strike: float, sigma_tau: float) -> float:
    """P(S_T ≥ K) under driftless lognormal with total vol σ_τ over remaining life."""
    if spot <= 0 or strike <= 0:
        return float("nan")
    if sigma_tau <= 1e-12:
        return 1.0 if spot >= strike else 0.0
    d2 = (math.log(spot / strike) - 0.5 * sigma_tau * sigma_tau) / sigma_tau
    return _norm_cdf(d2)


def floor_strike(m: dict) -> float | None:
    raw = m.get("floor_strike")
    if raw is None:
        return None
    try:
        k = float(raw)
    except (TypeError, ValueError):
        return None
    return k if k > 0 else None


def sigma_tau_from_signal(
    sig: Any,
    secs_left: float,
    *,
    mode: str | None = None,
    sigma_ann: float | None = None,
    sigma_floor_ann: float | None = None,
) -> tuple[float, str]:
    """Return (σ over remaining τ, tag)."""
    mode = (mode or LOGNORMAL_SIGMA_MODE).lower()
    sigma_ann = LOGNORMAL_SIGMA if sigma_ann is None else float(sigma_ann)
    sigma_floor_ann = (
        LOGNORMAL_SIGMA_FLOOR if sigma_floor_ann is None else float(sigma_floor_ann)
    )
    tau = max(1.0, float(secs_left))
    floor_tau = max(1e-8, sigma_floor_ann * math.sqrt(tau / YEAR_SEC))

    if mode == "fixed":
        st = max(floor_tau, sigma_ann * math.sqrt(tau / YEAR_SEC))
        return st, f"fixed_ann={sigma_ann:g}"

    # realized: LeadSignal.vol ≈ return-std over signal.window_sec
    vol = float(getattr(sig, "vol", 0.0) or 0.0)
    win = float(getattr(sig, "window_sec", 0.0) or 0.0)
    if vol > 0 and win > 0:
        st = vol * math.sqrt(tau / win)
        if st < floor_tau:
            return floor_tau, f"realized_floored<{sigma_floor_ann:g}ann"
        return st, f"realized_vol={vol:.5f}/{win:.0f}s"
    st = max(floor_tau, sigma_ann * math.sqrt(tau / YEAR_SEC))
    return st, f"fallback_ann={sigma_ann:g}"


def evaluate(
    m: dict,
    side: str,
    entry: float,
    secs_left: float,
    spot: float,
    sig: Any = None,
) -> tuple[bool, str, dict]:
    """Return (allow, reason, detail).

    When LOGNORMAL_GATE is off, always allows.
    """
    detail: dict = {
        "entry": entry,
        "side": side,
        "secs_left": secs_left,
        "spot": spot,
    }
    if not LOGNORMAL_GATE:
        return True, "gate_off", detail

    strike = floor_strike(m)
    detail["strike"] = strike
    if strike is None or spot is None or spot <= 0:
        if LOGNORMAL_STRICT:
            return False, "no_spot_or_strike", detail
        return True, "no_inputs_pass", detail

    sigma_tau, sigma_tag = sigma_tau_from_signal(sig, secs_left)
    detail["sigma_tau"] = sigma_tau
    detail["sigma_tag"] = sigma_tag

    p_yes = digital_yes_prob(spot, strike, sigma_tau)
    if math.isnan(p_yes):
        if LOGNORMAL_STRICT:
            return False, "model_nan", detail
        return True, "model_nan_pass", detail

    model_prob = p_yes if side == "yes" else (1.0 - p_yes)
    edge = model_prob - float(entry)
    detail["p_yes"] = p_yes
    detail["model_prob"] = model_prob
    detail["edge"] = edge

    if model_prob < LOGNORMAL_MIN_PROB:
        return False, (
            f"model_prob={model_prob:.3f}<{LOGNORMAL_MIN_PROB:.3f}"
            f"|edge={edge:+.3f}|{sigma_tag}"
        ), detail
    if edge < LOGNORMAL_MIN_EDGE:
        return False, (
            f"edge={edge:+.3f}<{LOGNORMAL_MIN_EDGE:.3f}"
            f"|prob={model_prob:.3f}|{sigma_tag}"
        ), detail
    return True, (
        f"ok prob={model_prob:.3f} edge={edge:+.3f} "
        f"S={spot:g}/K={strike:g} {sigma_tag}"
    ), detail


def require_agree_ok(bn_why: str) -> tuple[bool, str]:
    """Optional: block flat / weak BN tags when LOGNORMAL_REQUIRE_AGREE."""
    if not LOGNORMAL_REQUIRE_AGREE:
        return True, ""
    tag = (bn_why or "").lower()
    if "bnagree" in tag or tag.startswith("agree"):
        return True, ""
    # soft_binance tags look like bnagree×… / bnflat×… / disagree…
    if "bnflat" in tag or "flat" in tag or not tag:
        return False, f"require_agree:{bn_why or 'empty'}"
    if "disagree" in tag or "weak" in tag:
        return False, f"require_agree:{bn_why}"
    return True, ""
