"""Per-series performance governor.

Watches recent closed trades per series and auto-adjusts size so a
chopping series (e.g. SOL 4-5 −$17 in a morning) can't keep taking
full-size tickets, while hot series (ETH 28-0) get a modest boost.

Rules over the last SERIES_GOV_N non-flat closes of a series:
  net ≤ ICE_NET             → ×ICE_MULT   (nearly off)
  net ≤ COLD_NET or 3+ losses with net<0 → ×COLD_MULT
  WR ≥ HOT_WR and net ≥ HOT_NET          → ×HOT_MULT
  otherwise                               → ×1.0

Cold/ice decisions require ≥ MIN_SAMPLE closes so one bad settle
doesn't bench a series.
"""
from __future__ import annotations

import os


ENABLED = os.environ.get("SERIES_GOV", "1").lower() in ("1", "true", "yes", "on")
N = int(os.environ.get("SERIES_GOV_N", "8"))
MIN_SAMPLE = int(os.environ.get("SERIES_GOV_MIN_SAMPLE", "5"))

COLD_NET = float(os.environ.get("SERIES_GOV_COLD_NET", "-4"))
COLD_MULT = float(os.environ.get("SERIES_GOV_COLD_MULT", "0.5"))
ICE_NET = float(os.environ.get("SERIES_GOV_ICE_NET", "-9"))
ICE_MULT = float(os.environ.get("SERIES_GOV_ICE_MULT", "0.25"))

HOT_WR = float(os.environ.get("SERIES_GOV_HOT_WR", "0.90"))
HOT_NET = float(os.environ.get("SERIES_GOV_HOT_NET", "3"))
HOT_MULT = float(os.environ.get("SERIES_GOV_HOT_MULT", "1.25"))


def series_risk_mult(closed: list[dict], series: str) -> tuple[float, str]:
    """Return (size_mult, tag) for a series based on its recent closes."""
    if not ENABLED:
        return 1.0, ""
    recent: list[float] = []
    for c in reversed(closed[-300:]):
        t = c.get("ticker") or ""
        if not t.startswith(series):
            continue
        pnl = float(c.get("pnl") or 0)
        if pnl == 0 and not c.get("result"):
            continue  # unfilled / scratch
        recent.append(pnl)
        if len(recent) >= N:
            break
    if len(recent) < MIN_SAMPLE:
        return 1.0, ""
    net = sum(recent)
    wins = sum(1 for p in recent if p > 0)
    losses = sum(1 for p in recent if p < 0)
    wr = wins / len(recent)
    if net <= ICE_NET:
        return ICE_MULT, f"gov_ice×{ICE_MULT:g}(net{net:+.1f}/{len(recent)})"
    if net <= COLD_NET or (losses >= 3 and net < 0):
        return COLD_MULT, f"gov_cold×{COLD_MULT:g}(net{net:+.1f},{wins}-{losses})"
    if wr >= HOT_WR and net >= HOT_NET:
        return HOT_MULT, f"gov_hot×{HOT_MULT:g}(net{net:+.1f},{wins}-{losses})"
    return 1.0, ""


def describe() -> str:
    if not ENABLED:
        return "series_gov=OFF"
    return (
        f"series_gov=last{N}: ice≤{ICE_NET:g}×{ICE_MULT:g} "
        f"cold≤{COLD_NET:g}×{COLD_MULT:g} "
        f"hot≥{100*HOT_WR:.0f}%&+{HOT_NET:g}×{HOT_MULT:g}"
    )
