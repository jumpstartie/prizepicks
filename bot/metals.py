"""Gold/silver 15m helpers — settlement-aligned edge vs retail bots.

Competitive design (why this can beat other traders/quants on Kalshi metals):

1. Settlement truth: Kalshi gold/silver 15m resolve off Pyth. We use Hermes
   Metal.XAU/XAG as the *primary* lean, not PAXG/chart TA that can diverge.
2. Confirm, don't invent: Coinbase XAU/XAG must agree for full soft size.
3. Session awareness: skip dead metals tape (daily COMEX-style break + weekend).
4. Correlated bucket: gold+silver share a soft-corr cap so one theme can't
   stack like independent alts.
5. No crypto risk-veto bleed: BTC dump ≠ fade gold automatically.

This module stays small — lead math lives in binance_lead.py; runner calls
session / series helpers here.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

METALS_SERIES = frozenset(
    s.strip().upper()
    for s in os.environ.get("METALS_SERIES", "KXGOLD15M,KXSILVER15M").split(",")
    if s.strip()
)
METALS_SOFT_CORR_MAX = int(os.environ.get("METALS_SOFT_CORR_MAX", "2"))
METALS_SESSION = os.environ.get("METALS_SESSION", "1").lower() in (
    "1", "true", "yes", "on",
)
# America/New_York schedule mirrors Pyth Metal.* feed metadata:
# trade 00:00–17:00 and 18:00–24:00 ET weekdays (daily 17:00–18:00 break).
METALS_TZ = ZoneInfo(os.environ.get("METALS_TZ", "America/New_York"))


def series_root(ticker_or_series: str) -> str:
    return (ticker_or_series or "").split("-", 1)[0].upper()


def is_metal(ticker_or_series: str) -> bool:
    return series_root(ticker_or_series) in METALS_SERIES


def metals_session_ok(now: datetime | None = None) -> tuple[bool, str]:
    """Allow metals entries only in liquid ET hours when METALS_SESSION=1."""
    if not METALS_SESSION:
        return True, ""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    et = now.astimezone(METALS_TZ)
    # Sat=5 Sun=6 — metals spot/futures thin; skip
    if et.weekday() >= 5:
        return False, f"metals_weekend:{et.strftime('%a %H:%M ET')}"
    mins = et.hour * 60 + et.minute
    # Daily break ~17:00–18:00 ET
    if 17 * 60 <= mins < 18 * 60:
        return False, f"metals_daily_break:{et.strftime('%H:%M ET')}"
    return True, ""
