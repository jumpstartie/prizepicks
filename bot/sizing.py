"""Unit sizing for the near-expiry favorite maker strategy.

Default is a capped risk band (~$3–5 on a $21 book). When EDGE_SIZING=1,
risk fraction is set from live edge estimates (fractional Kelly), cut when
recent EV/WR decays, and never sized past the halt buffer.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass

# Strategy assumptions from the 31-day backtest
AVG_ENTRY = 0.93
AVG_WIN_PAYOFF = 1.0 - AVG_ENTRY  # ~0.07
LOSS_PER_CONTRACT = AVG_ENTRY     # lose the entry price on a loser
WIN_RATE = 0.95

# Risk controls for a ~$20 test account (profit-first sizing)
RISK_FRACTION = 0.18              # base ~$3.8/trade; overridden by edge sizer
RISK_FRAC_MIN = float(os.environ.get("RISK_FRAC_MIN", "0.13"))   # keep overnight size from collapsing
RISK_FRAC_MAX = float(os.environ.get("RISK_FRAC_MAX", "0.25"))   # post-cluster cap
EDGE_SIZING = os.environ.get("EDGE_SIZING", "1").lower() in ("1", "true", "yes", "on")
EDGE_LOOKBACK = int(os.environ.get("EDGE_LOOKBACK", "30"))       # recent filled closes
EDGE_MIN_SAMPLES = int(os.environ.get("EDGE_MIN_SAMPLES", "8"))
EDGE_KELLY_FRAC = float(os.environ.get("EDGE_KELLY_FRAC", "0.33"))  # ~0.33 Kelly
EDGE_PRIOR_WR = float(os.environ.get("EDGE_PRIOR_WR", "0.93"))
EDGE_PRIOR_STRENGTH = float(os.environ.get("EDGE_PRIOR_STRENGTH", "12"))  # pseudo-counts
# 1 full-loss buffer to the raised floor so MAX risk can still bind near ~$70
HALT_LOSS_BUFFER = int(os.environ.get("HALT_LOSS_BUFFER", "1"))
MAX_EXPOSURE_FRAC = 0.60
MAX_CONCURRENT = 7
HALT_EQUITY_FRAC = 0.50
HALT_FLOOR_DOLLARS = 70.0
MIN_CONTRACTS = 0.01
CONTRACT_STEP = 0.01


@dataclass
class EdgeStats:
    n: int
    wins: int
    wr: float
    avg_win: float
    avg_loss: float          # positive magnitude
    avg_entry: float
    ev_per_trade: float
    kelly: float
    risk_frac: float
    reason: str


def _filled_closed(closed: list[dict], for_edge: bool = False) -> list[dict]:
    out = []
    for c in closed:
        if not c.get("filled"):
            continue
        if c.get("pnl") is None:
            continue
        # skip pure cancels / zero-cost ghosts
        if (c.get("cost") or 0) <= 0:
            continue
        if for_edge:
            # Size off the current strategy regime only (settle / spike TP).
            # Old stop-loss exits are a different playbook and bias Kelly down.
            reason = (c.get("exit_reason") or "settle").lower()
            if reason in ("stop", "binance_cancel"):
                continue
        out.append(c)
    return out


def estimate_edge(closed: list[dict],
                  lookback: int | None = None,
                  base_risk: float | None = None) -> EdgeStats:
    """Blend live results with a prior; return recommended risk fraction."""
    base = RISK_FRACTION if base_risk is None else base_risk
    lb = EDGE_LOOKBACK if lookback is None else lookback
    rows = _filled_closed(closed, for_edge=True)[-lb:]
    n = len(rows)
    if n == 0:
        return EdgeStats(
            n=0, wins=0, wr=EDGE_PRIOR_WR, avg_win=AVG_WIN_PAYOFF * AVG_ENTRY,
            avg_loss=AVG_ENTRY, avg_entry=AVG_ENTRY, ev_per_trade=0.0,
            kelly=0.0, risk_frac=_clamp(base), reason="prior_no_samples",
        )

    wins_rows = [r for r in rows if (r.get("pnl") or 0) > 0]
    loss_rows = [r for r in rows if (r.get("pnl") or 0) <= 0]
    wins = len(wins_rows)
    raw_wr = wins / n
    # Bayesian shrink toward prior
    wr = (wins + EDGE_PRIOR_STRENGTH * EDGE_PRIOR_WR) / (n + EDGE_PRIOR_STRENGTH)

    avg_entry = sum(float(r.get("entry") or AVG_ENTRY) for r in rows) / n
    if wins_rows:
        avg_win = sum(float(r["pnl"]) for r in wins_rows) / len(wins_rows)
    else:
        avg_win = 0.0
    if loss_rows:
        avg_loss = abs(sum(float(r["pnl"]) for r in loss_rows) / len(loss_rows))
    else:
        avg_loss = 0.0

    # Per-trade EV on the recent sample (unshrunk dollars)
    ev = sum(float(r["pnl"]) for r in rows) / n

    # Binary favorite Kelly on bankroll fraction:
    #   risk stake S; win +(1-e)/e * S; lose -S
    #   f* = p - (1-p)/b  with b = (1-e)/e
    b_net = (1.0 - avg_entry) / avg_entry if 0 < avg_entry < 1 else 0.0
    q = 1.0 - wr
    kelly_full = (wr - q / b_net) if b_net > 0 else 0.0
    kelly = max(0.0, kelly_full)
    frag = kelly * EDGE_KELLY_FRAC

    reason = "edge_kelly"
    risk = frag

    # Not enough samples: blend toward base
    if n < EDGE_MIN_SAMPLES:
        w = n / EDGE_MIN_SAMPLES
        risk = w * frag + (1 - w) * base
        reason = f"blend_n={n}"

    # Negative live dollar EV or non-positive Kelly → cut to floor
    if ev < 0 or kelly_full <= 0:
        risk = RISK_FRAC_MIN
        reason = "cut_neg_edge"
    elif kelly_full < 0.05:
        # Tiny theoretical edge — stay conservative
        risk = min(risk, (RISK_FRAC_MIN + base) / 2)
        reason = "soft_thin_edge"

    risk = _clamp(risk)
    return EdgeStats(
        n=n, wins=wins, wr=wr, avg_win=avg_win, avg_loss=avg_loss,
        avg_entry=avg_entry, ev_per_trade=ev, kelly=kelly_full,
        risk_frac=risk, reason=reason,
    )


def _clamp(x: float) -> float:
    return max(RISK_FRAC_MIN, min(RISK_FRAC_MAX, x))


def halt_capped_risk(equity: float, entry: float,
                     floor: float | None = None,
                     risk_frac: float | None = None) -> float:
    """Cap risk so ~HALT_LOSS_BUFFER full losses don't breach the floor."""
    rf = RISK_FRACTION if risk_frac is None else risk_frac
    abs_floor = HALT_FLOOR_DOLLARS if floor is None else floor
    room = max(0.0, equity - abs_floor)
    if room <= 0 or entry <= 0 or HALT_LOSS_BUFFER <= 0:
        return RISK_FRAC_MIN
    # each loss ≈ risk_frac * equity (stake)
    max_frac = room / (HALT_LOSS_BUFFER * equity)
    return _clamp(min(rf, max_frac))


def effective_risk_fraction(equity: float,
                            closed: list[dict] | None = None,
                            entry: float = AVG_ENTRY,
                            floor: float | None = None,
                            base_risk: float | None = None) -> tuple[float, EdgeStats]:
    """Risk fraction to use on the next trade (+ diagnostics)."""
    base = RISK_FRACTION if base_risk is None else base_risk
    if not EDGE_SIZING:
        stats = EdgeStats(
            n=0, wins=0, wr=EDGE_PRIOR_WR, avg_win=0.0, avg_loss=0.0,
            avg_entry=entry, ev_per_trade=0.0, kelly=0.0,
            risk_frac=_clamp(base), reason="edge_sizing_off",
        )
        return halt_capped_risk(equity, entry, floor, stats.risk_frac), stats

    stats = estimate_edge(closed or [], base_risk=base)
    capped = halt_capped_risk(equity, entry, floor, stats.risk_frac)
    if capped < stats.risk_frac - 1e-9:
        stats = EdgeStats(**{**stats.__dict__, "risk_frac": capped,
                             "reason": stats.reason + "+halt_cap"})
    else:
        stats = EdgeStats(**{**stats.__dict__, "risk_frac": capped})
    return capped, stats


def contracts_for_equity(equity: float, entry: float = AVG_ENTRY,
                         size_mult: float = 1.0,
                         risk_frac: float | None = None) -> float:
    """Contracts to buy on the next signal given current equity.

    size_mult < 1 scales down (e.g. 0.5 for untested satellite markets).
    """
    if equity <= 0 or entry <= 0 or size_mult <= 0:
        return 0.0
    rf = RISK_FRACTION if risk_frac is None else risk_frac
    risk_budget = equity * rf * size_mult
    raw = risk_budget / entry
    stepped = math.floor(raw / CONTRACT_STEP) * CONTRACT_STEP
    if stepped < MIN_CONTRACTS:
        return MIN_CONTRACTS if equity >= entry * MIN_CONTRACTS else 0.0
    return round(stepped, 2)


def max_concurrent(equity: float, entry: float = AVG_ENTRY,
                   hard_cap: int | None = None,
                   exposure_frac: float | None = None,
                   risk_frac: float | None = None) -> int:
    """Max simultaneous open positions at the current unit size."""
    unit = contracts_for_equity(equity, entry, risk_frac=risk_frac)
    if unit <= 0:
        return 0
    frac = MAX_EXPOSURE_FRAC if exposure_frac is None else exposure_frac
    cap = equity * frac
    by_capital = max(1, int(cap // (entry * unit)))
    limit = MAX_CONCURRENT if hard_cap is None else hard_cap
    return max(1, min(by_capital, limit))


def should_halt(equity: float, start_equity: float,
                floor: float | None = None) -> bool:
    """Halt on fractional drawdown or absolute dollar floor (whichever is higher)."""
    frac_floor = start_equity * HALT_EQUITY_FRAC
    abs_floor = HALT_FLOOR_DOLLARS if floor is None else floor
    return equity <= max(frac_floor, abs_floor)


def should_halt_profit(equity: float, start_equity: float,
                       profit_target: float | None = None) -> bool:
    """Halt after bankroll profit target is reached (0/None = disabled)."""
    if profit_target is None or profit_target <= 0:
        return False
    return (equity - start_equity) >= profit_target


def describe(start_equity: float = 20.0, floor: float | None = None,
             closed: list[dict] | None = None) -> str:
    rf, stats = effective_risk_fraction(start_equity, closed=closed, floor=floor)
    unit = contracts_for_equity(start_equity, risk_frac=rf)
    conc = max_concurrent(start_equity, risk_frac=rf)
    risk = unit * LOSS_PER_CONTRACT
    locked = conc * unit * AVG_ENTRY
    abs_floor = HALT_FLOOR_DOLLARS if floor is None else floor
    halt_at = max(start_equity * HALT_EQUITY_FRAC, abs_floor)
    return (
        f"bankroll=${start_equity:.2f}  unit={unit:.2f} contracts/trade  "
        f"risk/trade=${risk:.2f} ({100*rf:.1f}% of bankroll, {stats.reason})  "
        f"edge: n={stats.n} wr={100*stats.wr:.1f}% ev=${stats.ev_per_trade:+.3f} "
        f"kelly={100*stats.kelly:.1f}%  "
        f"max concurrent={conc}/{MAX_CONCURRENT} (locks ~${locked:.2f}, "
        f"{100*MAX_EXPOSURE_FRAC:.0f}% exposure)  "
        f"halt if equity <= ${halt_at:.2f}"
    )


if __name__ == "__main__":
    demo = [
        {"filled": True, "pnl": 0.12, "entry": 0.93, "cost": 2.0},
        {"filled": True, "pnl": 0.10, "entry": 0.94, "cost": 2.1},
        {"filled": True, "pnl": -2.0, "entry": 0.94, "cost": 2.0},
    ] * 4
    for e in (20.0, 50.0, 100.0):
        print(describe(e, closed=demo))
        print(describe(e, closed=[]))
