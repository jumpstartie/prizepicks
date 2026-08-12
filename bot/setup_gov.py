"""Setup-level performance governor (the quant notch).

Sizes the *next* ticket from how similar setups performed recently —
not vibes, not a single ticker hot-hand.

Axes (independent, multiplied, then clamped):
  band   : soft (<SOFT_MAX) | mid | rich (≥RICH_MIN)
  lead   : agree | flat | disagree   (from stored binance_dir vs side)
  phase  : early | mid | late        (secs_left_at_entry)
  asset  : metals | crypto

Per axis, over the last SETUP_GOV_N matching closes:
  net ≤ ICE_NET                         → ×ICE_MULT
  net ≤ COLD_NET or (≥3 losses & net<0) → ×COLD_MULT
  WR ≥ HOT_WR and net ≥ HOT_NET         → ×HOT_MULT
  else / n < MIN_SAMPLE                 → ×1.0

Product of axis mults is clamped to [MIN_MULT, MAX_MULT] so a hot streak
can't stack with series_gov into ruin, and ice on one axis can't zero size.
"""
from __future__ import annotations

import os
from typing import Iterable

ENABLED = os.environ.get("SETUP_GOV", "1").lower() in ("1", "true", "yes", "on")
N = int(os.environ.get("SETUP_GOV_N", "20"))
MIN_SAMPLE = int(os.environ.get("SETUP_GOV_MIN_SAMPLE", "8"))

SOFT_MAX = float(os.environ.get("SETUP_GOV_SOFT_MAX",
                                os.environ.get("SOFT_ENTRY_MAX", "0.85")))
RICH_MIN = float(os.environ.get("SETUP_GOV_RICH_MIN",
                                os.environ.get("TAKE_PROFIT_MIN_ENTRY", "0.88")))
EARLY_SECS = float(os.environ.get("SETUP_GOV_EARLY_SECS",
                                  os.environ.get("EARLY_WINDOW_SEC", "720")))
LATE_SECS = float(os.environ.get("SETUP_GOV_LATE_SECS",
                                 os.environ.get("LATE_WINDOW_SEC", "180")))

COLD_NET = float(os.environ.get("SETUP_GOV_COLD_NET", "-5"))
COLD_MULT = float(os.environ.get("SETUP_GOV_COLD_MULT", "0.60"))
ICE_NET = float(os.environ.get("SETUP_GOV_ICE_NET", "-10"))
ICE_MULT = float(os.environ.get("SETUP_GOV_ICE_MULT", "0.35"))
HOT_WR = float(os.environ.get("SETUP_GOV_HOT_WR", "0.90"))
HOT_NET = float(os.environ.get("SETUP_GOV_HOT_NET", "4"))
HOT_MULT = float(os.environ.get("SETUP_GOV_HOT_MULT", "1.20"))
# Keys that must never receive HOT_MULT (TP-inflated flat sample nuked the book).
NO_HOT_KEYS = {
    k.strip()
    for k in os.environ.get("SETUP_GOV_NO_HOT_KEYS", "lead_flat").split(",")
    if k.strip()
}

MIN_MULT = float(os.environ.get("SETUP_GOV_MIN_MULT", "0.35"))
MAX_MULT = float(os.environ.get("SETUP_GOV_MAX_MULT", "1.35"))

# When an axis is iced, skip new entries on that axis (frees book for hot setups).
BLOCK_ICE = os.environ.get("SETUP_GOV_BLOCK_ICE", "1").lower() in (
    "1", "true", "yes", "on",
)
BLOCK_ICE_AXES = tuple(
    a.strip().lower()
    for a in os.environ.get("SETUP_GOV_BLOCK_ICE_AXES", "band").split(",")
    if a.strip()
)
# Drop iced-band closes from Kelly sample so soft ice doesn't mute mid/rich risk.
EDGE_EXCLUDE_ICED = os.environ.get("SETUP_GOV_EDGE_EXCLUDE_ICED", "1").lower() in (
    "1", "true", "yes", "on",
)

METALS_PREFIXES = tuple(
    s.strip().upper()
    for s in os.environ.get("METALS_SERIES", "KXGOLD15M,KXSILVER15M").split(",")
    if s.strip()
)

# Which axes to score. Default omits `asset`: asset_crypto is nearly the whole
# book and double-counts global Kelly; enable asset once metals have sample.
AXES = tuple(
    a.strip().lower()
    for a in os.environ.get("SETUP_GOV_AXES", "band,lead,phase").split(",")
    if a.strip()
)


def _series_root(ticker: str) -> str:
    return (ticker or "").split("-", 1)[0].upper()


def _is_metal_ticker(ticker: str) -> bool:
    root = _series_root(ticker)
    return any(root == p or root.startswith(p) for p in METALS_PREFIXES)


def band_key(entry: float) -> str:
    e = float(entry or 0)
    if e <= 0:
        return "band_unk"
    if e < SOFT_MAX:
        return "band_soft"
    if e >= RICH_MIN:
        return "band_rich"
    return "band_mid"


def lead_key(side: str, binance_dir: str | None) -> str:
    d = (binance_dir or "").lower()
    if d not in ("up", "down", "flat"):
        return "lead_unk"
    if d == "flat":
        return "lead_flat"
    want = "up" if side == "yes" else "down"
    return "lead_agree" if d == want else "lead_disagree"


def phase_key(secs_left: float | None) -> str:
    if secs_left is None:
        return "phase_unk"
    s = float(secs_left)
    if s >= EARLY_SECS:
        return "phase_early"
    if 0 < s <= LATE_SECS:
        return "phase_late"
    return "phase_mid"


def asset_key(ticker: str) -> str:
    return "asset_metals" if _is_metal_ticker(ticker) else "asset_crypto"


def classify_keys(
    entry: float,
    side: str,
    secs_left: float | None,
    binance_dir: str | None,
    ticker: str = "",
) -> dict[str, str]:
    """Axis → key for this ticket."""
    return {
        "band": band_key(entry),
        "lead": lead_key(side, binance_dir),
        "phase": phase_key(secs_left),
        "asset": asset_key(ticker),
    }


def _row_keys(c: dict) -> dict[str, str]:
    return classify_keys(
        entry=float(c.get("entry") or 0),
        side=str(c.get("side") or ""),
        secs_left=c.get("secs_left_at_entry"),
        binance_dir=c.get("binance_dir"),
        ticker=str(c.get("ticker") or ""),
    )


def _pnl_sample(closed: list[dict], key: str) -> list[float]:
    """Recent filled pnls whose classification includes `key`."""
    out: list[float] = []
    for c in reversed(closed[-400:]):
        if not c.get("filled"):
            continue
        pnl = c.get("pnl")
        if pnl is None:
            continue
        if (c.get("cost") or 0) <= 0:
            continue
        reason = (c.get("exit_reason") or "settle").lower()
        if reason in ("stop", "binance_cancel"):
            continue
        keys = _row_keys(c)
        if key not in keys.values():
            continue
        out.append(float(pnl))
        if len(out) >= N:
            break
    return out


def _axis_mult(pnls: list[float], key: str) -> tuple[float, str]:
    if len(pnls) < MIN_SAMPLE:
        return 1.0, ""
    net = sum(pnls)
    wins = sum(1 for p in pnls if p > 0)
    losses = sum(1 for p in pnls if p < 0)
    wr = wins / len(pnls)
    if net <= ICE_NET:
        return ICE_MULT, f"setup_{key}:ice×{ICE_MULT:g}({wins}-{losses},net{net:+.1f})"
    if net <= COLD_NET or (losses >= 3 and net < 0):
        return COLD_MULT, f"setup_{key}:cold×{COLD_MULT:g}({wins}-{losses},net{net:+.1f})"
    if wr >= HOT_WR and net >= HOT_NET:
        if key in NO_HOT_KEYS:
            return 1.0, f"setup_{key}:hot_blocked({wins}-{losses},net{net:+.1f})"
        return HOT_MULT, f"setup_{key}:hot×{HOT_MULT:g}({wins}-{losses},net{net:+.1f})"
    return 1.0, ""


def iced_keys(closed: list[dict], axes: Iterable[str] | None = None) -> dict[str, str]:
    """Return {axis_key: tag} for setups currently in ice state."""
    axes = tuple(axes) if axes is not None else AXES
    out: dict[str, str] = {}
    # Evaluate canonical keys per axis
    candidates = {
        "band": ("band_soft", "band_mid", "band_rich"),
        "lead": ("lead_agree", "lead_flat", "lead_disagree"),
        "phase": ("phase_early", "phase_mid", "phase_late"),
        "asset": ("asset_crypto", "asset_metals"),
    }
    for axis in axes:
        for key in candidates.get(axis, ()):
            pnls = _pnl_sample(closed, key)
            m, tag = _axis_mult(pnls, key)
            if tag and ":ice" in tag:
                out[key] = tag
    return out


def should_block_entry(
    closed: list[dict],
    *,
    entry: float,
    side: str,
    secs_left: float | None,
    binance_dir: str | None,
    ticker: str = "",
) -> tuple[bool, str]:
    """True = skip. Blocks tickets whose BLOCK_ICE_AXES key is currently iced."""
    if not ENABLED or not BLOCK_ICE:
        return False, ""
    keys = classify_keys(entry, side, secs_left, binance_dir, ticker)
    iced = iced_keys(closed, BLOCK_ICE_AXES)
    if not iced:
        return False, ""
    for axis in BLOCK_ICE_AXES:
        key = keys.get(axis)
        if key and key in iced:
            return True, iced[key]
    return False, ""


def filter_closed_for_edge(closed: list[dict]) -> list[dict]:
    """Exclude closes from currently iced bands so Kelly tracks tradable setups."""
    if not ENABLED or not EDGE_EXCLUDE_ICED:
        return closed
    iced = iced_keys(closed, ("band",))
    if not iced:
        return closed
    out = []
    for c in closed:
        k = band_key(float(c.get("entry") or 0))
        if k in iced:
            continue
        out.append(c)
    return out if out else closed


def setup_risk_mult(
    closed: list[dict],
    *,
    entry: float,
    side: str,
    secs_left: float | None,
    binance_dir: str | None,
    ticker: str = "",
) -> tuple[float, str, dict[str, str]]:
    """Return (size_mult, tag, keys) from setup-level recent performance."""
    keys = classify_keys(entry, side, secs_left, binance_dir, ticker)
    if not ENABLED:
        return 1.0, "", keys

    mult = 1.0
    tags: list[str] = []
    for axis in AXES:
        key = keys.get(axis)
        if not key or key.endswith("_unk"):
            continue
        pnls = _pnl_sample(closed, key)
        m, tag = _axis_mult(pnls, key)
        if m != 1.0:
            mult *= m
            tags.append(tag)

    if mult < MIN_MULT:
        tags.append(f"setup_floor×{MIN_MULT:g}")
        mult = MIN_MULT
    elif mult > MAX_MULT:
        tags.append(f"setup_cap×{MAX_MULT:g}")
        mult = MAX_MULT

    return mult, "+".join(tags), keys


def summarize_axes(closed: list[dict],
                   keys: Iterable[str] | None = None) -> list[str]:
    """Human-readable status lines for logs / research."""
    keys = list(keys) if keys is not None else [
        "band_soft", "band_mid", "band_rich",
        "lead_agree", "lead_flat", "lead_disagree",
        "phase_early", "phase_mid", "phase_late",
        "asset_crypto", "asset_metals",
    ]
    lines = []
    for key in keys:
        pnls = _pnl_sample(closed, key)
        if len(pnls) < 3:
            continue
        m, tag = _axis_mult(pnls, key)
        net = sum(pnls)
        wins = sum(1 for p in pnls if p > 0)
        losses = sum(1 for p in pnls if p < 0)
        state = tag.split(":")[-1].split("×")[0] if tag else "neutral"
        lines.append(
            f"{key}:{state} n={len(pnls)} {wins}-{losses} net{net:+.1f} →×{m:g}"
        )
    return lines


def describe() -> str:
    if not ENABLED:
        return "setup_gov=OFF"
    return (
        f"setup_gov=last{N}/min{MIN_SAMPLE} axes={','.join(AXES)} "
        f"ice≤{ICE_NET:g}×{ICE_MULT:g} cold≤{COLD_NET:g}×{COLD_MULT:g} "
        f"hot≥{100*HOT_WR:.0f}%&+{HOT_NET:g}×{HOT_MULT:g} "
        f"clamp[{MIN_MULT:g},{MAX_MULT:g}] "
        f"block_ice={'/'.join(BLOCK_ICE_AXES) if BLOCK_ICE else 'OFF'} "
        f"edge_ex_ice={'ON' if EDGE_EXCLUDE_ICED else 'OFF'}"
    )
