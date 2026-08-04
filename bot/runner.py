"""Live paper/live runner for the near-expiry favorite maker strategy.

Strategy (from research/):
  In the final 3 minutes of a 15-minute crypto up/down market, if either side
  trades at 90-97c, rest a post-only bid on that side at mid (maker, no fee).
  Hold to settlement.

Default mode is PAPER: uses the public market-data API, simulates maker fills
when the market subsequently trades through our resting price. No API keys
needed. Set MODE=live plus KALSHI_API_KEY_ID / KALSHI_PRIVATE_KEY(_PATH) to
place real orders.

Usage:
  START_EQUITY=20 MODE=paper python3 bot/runner.py
"""
from __future__ import annotations

import json
import math
import os
import signal
import sys
import time
import datetime
from dataclasses import dataclass, asdict, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bot.kalshi_client import KalshiClient
from bot import metals, series_gov, setup_gov, time_phase
from bot import sizing
from bot.binance_lead import BinanceLeadFeed, lean_enabled, lean_mode, symbol_for

# Profit-first defaults from live + 31d research: core favorites only, hold to settle.
# (HYPE/ZEC stops were the only live losses; BTC/DOGE/ETH were flat in backtest.)
SERIES = [
    s.strip() for s in os.environ.get(
        "SERIES", "KXBNB15M,KXSOL15M,KXXRP15M,KXETH15M"
    ).split(",") if s.strip()
]
# Optional half-size satellites (also scanned for signals)
SATELLITE_SERIES = set(
    s.strip()
    for s in os.environ.get("SATELLITE_SERIES", "KXBTC15M,KXDOGE15M,KXNEAR15M").split(",")
    if s.strip()
)
SATELLITE_SIZE_MULT = float(os.environ.get("SATELLITE_SIZE_MULT", "0.5"))
# Markets we actually poll = core + satellites
ALL_SERIES = list(dict.fromkeys(SERIES + sorted(SATELLITE_SERIES)))
START_EQUITY = float(os.environ.get("START_EQUITY", "20"))
MODE = os.environ.get("MODE", "paper").lower()  # paper | live
POLL_SEC = float(os.environ.get("POLL_SEC", "3"))
# High-frequency band: trade any clear favorite for most of the 15m window.
# Research sweet-spot was 90–97; this prioritizes fill rate over edge purity.
PRICE_LO = float(os.environ.get("PRICE_LO", "0.70"))
PRICE_HI = float(os.environ.get("PRICE_HI", "0.999"))
# 0 = disabled. Live data: settle exits +EV, stop exits wiped the edge.
STOP_LOSS_PCT = float(os.environ.get("STOP_LOSS_PCT", "0"))
# Do not stop-loss in the final N seconds — hold to settlement (favorites wick).
STOP_DISABLE_SECS = int(os.environ.get("STOP_DISABLE_SECS", "60"))
# Almost the full 15m candle (leave a little buffer after open)
WINDOW_SEC = int(os.environ.get("WINDOW_SEC", "840"))
# Require at least this much time left to enter
MIN_SECS_LEFT = int(os.environ.get("MIN_SECS_LEFT", "15"))
# Require the favorite band on the same side for this many consecutive polls
CONFIRM_POLLS = int(os.environ.get("CONFIRM_POLLS", "1"))
# Requotes after a post-only-cross rejection
MAX_REQUOTES = int(os.environ.get("MAX_REQUOTES", "3"))
# Per-trade take-profit on top of hold-to-settle favorites:
#   ABS:  mark hits a near-ceiling spike (main exit; default 0.98)
#   GAIN: optional mark >= entry + $ (0 = off)
#   MULT: optional Nx entry (0 = off; not used for 90¢+ favorites)
# Near-ceiling spike exit; with rich entries this rarely beats settle
TAKE_PROFIT_ABS = float(os.environ.get("TAKE_PROFIT_ABS", "0.98"))
TAKE_PROFIT_GAIN = float(os.environ.get("TAKE_PROFIT_GAIN", "0"))
TAKE_PROFIT_MULT = float(os.environ.get("TAKE_PROFIT_MULT", "0"))
TAKE_PROFIT_CAP = float(os.environ.get("TAKE_PROFIT_CAP", "0.99"))
# Abs/gain TP only for entries at/above this (soft favorites ride to settle).
TAKE_PROFIT_MIN_ENTRY = float(os.environ.get("TAKE_PROFIT_MIN_ENTRY", "0.88"))
# Soft entries still lock a near-certain spike at this mark (0 = off).
SOFT_SPIKE_TP = float(os.environ.get("SOFT_SPIKE_TP", "0.97"))
# Spike-fade guard: once a position's mark peaks ≥ SPIKE_PEAK, sell if it
# gives back ≥ SPIKE_GIVEBACK while still ≥ entry + SPIKE_MIN_GAIN.
SPIKE_FADE = os.environ.get("SPIKE_FADE", "1").lower() in ("1", "true", "yes", "on")
SPIKE_PEAK = float(os.environ.get("SPIKE_PEAK", "0.93"))
SPIKE_GIVEBACK = float(os.environ.get("SPIKE_GIVEBACK", "0.06"))
SPIKE_MIN_GAIN = float(os.environ.get("SPIKE_MIN_GAIN", "0.03"))
# Whale harvest: when MARKED equity spikes ≥ trigger×flat-baseline, sell all
# winning opens (mark ≥ min) into the bid — converts phantom marks to cash so
# the trailing floor can ratchet on the spike instead of watching it fade.
EQUITY_HARVEST = os.environ.get("EQUITY_HARVEST", "1").lower() in ("1", "true", "yes", "on")
HARVEST_TRIGGER_FRAC = float(os.environ.get("HARVEST_TRIGGER_FRAC", "1.25"))
HARVEST_MIN_MARK = float(os.environ.get("HARVEST_MIN_MARK", "0.90"))
HARVEST_COOLDOWN_SEC = float(os.environ.get("HARVEST_COOLDOWN_SEC", "300"))
# Absolute bankroll floor — stop the run if equity hits this (banked-profit floor)
HALT_FLOOR = float(os.environ.get("HALT_FLOOR", "70.0"))
# Trailing floor: ratchet to this fraction of realized (flat) high-water.
# Keeps drawdown room proportional as the book grows; never drops below HALT_FLOOR.
HALT_TRAIL_FRAC = float(os.environ.get("HALT_TRAIL_FRAC", "0.70"))
# Bank +$N from start_equity, then freeze new entries (0 = disabled)
HALT_PROFIT = float(os.environ.get("HALT_PROFIT", "0"))
# Soft favorites: SIZE_MULT=1.0 disables the flat cut (strategy #3 full max-frequency).
SOFT_ENTRY_MAX = float(os.environ.get("SOFT_ENTRY_MAX", "0.85"))
SOFT_ENTRY_SIZE_MULT = float(os.environ.get("SOFT_ENTRY_SIZE_MULT", "1.0"))
SOFT_ENTRY_EARLY_SECS = float(os.environ.get("SOFT_ENTRY_EARLY_SECS", "300"))
# 1.0 = disabled.
SOFT_ENTRY_EARLY_MULT = float(os.environ.get("SOFT_ENTRY_EARLY_MULT", "1.0"))
# Cap how many soft (<SOFT_ENTRY_MAX) positions can be open together (corr risk).
SOFT_CORR_MAX = int(os.environ.get("SOFT_CORR_MAX", "3"))
# Staged size by time-left: >10m ×0.5, >5m ×0.75, else full.
STAGE_SIZE = os.environ.get("STAGE_SIZE", "1").lower() in ("1", "true", "yes", "on")
STAGE_SIZE_10M_MULT = float(os.environ.get("STAGE_SIZE_10M_MULT", "0.50"))
STAGE_SIZE_5M_MULT = float(os.environ.get("STAGE_SIZE_5M_MULT", "0.75"))
# Soft entries require a Binance lean in our favor (skip flat/disagree).
SOFT_BINANCE_STRICT = os.environ.get("SOFT_BINANCE_STRICT", "1").lower() in (
    "1", "true", "yes", "on",
)
# After N losses in the same 15m bucket, cut risk for a cooldown window.
LOSS_COOLDOWN_LOSSES = int(os.environ.get("LOSS_COOLDOWN_LOSSES", "2"))
LOSS_COOLDOWN_SEC = float(os.environ.get("LOSS_COOLDOWN_SEC", "900"))
LOSS_COOLDOWN_RISK_MULT = float(os.environ.get("LOSS_COOLDOWN_RISK_MULT", "0.50"))
# Concurrent positions: allow one per series, up to exposure budget
MAX_CONCURRENT = int(os.environ.get("MAX_CONCURRENT", str(sizing.MAX_CONCURRENT)))
MAX_EXPOSURE_FRAC = float(os.environ.get("MAX_EXPOSURE_FRAC", str(sizing.MAX_EXPOSURE_FRAC)))
# Allow override of risk fraction without editing sizing.py
if os.environ.get("RISK_FRACTION"):
    sizing.RISK_FRACTION = float(os.environ["RISK_FRACTION"])
# Skip only absurd locked books (set 1.0 to never skip on richness)
SKIP_ENTRY_RICH = float(os.environ.get("SKIP_ENTRY_RICH", "0.95"))
# Soft + fast Binance agree size boost (aggressive when tape confirms)
SOFT_BN_AGREE_MULT = float(os.environ.get("SOFT_BN_AGREE_MULT", "1.50"))
SOFT_BN_FLAT_MULT = float(os.environ.get("SOFT_BN_FLAT_MULT", "0.50"))
# Hard cap on the stacked size multiplier (BN agree × early × hot gov, etc.).
# Uncapped stacking hit ~2.3× and turned single soft losses into -$12..-17.
MAX_SIZE_MULT = float(os.environ.get("MAX_SIZE_MULT", "1.50"))
# Max yes-spread (ask-bid) to enter; wide books = adverse selection
MAX_SPREAD = float(os.environ.get("MAX_SPREAD", "0.20"))
# Binance lead: lean/filter Kalshi YES/NO using spot direction (XRP/BNB/SOL…)
BINANCE_LEAD = lean_enabled()
BINANCE_LEAD_MODE = lean_mode()  # filter | strict | off
STATE_PATH = Path(os.environ.get(
    "STATE_PATH",
    "bot/state_live.json" if MODE == "live" else "bot/state.json",
))
LOG_PATH = Path(os.environ.get(
    "LOG_PATH",
    "bot/trades_live.jsonl" if MODE == "live" else "bot/trades.jsonl",
))

RUNNING = True
LEAD_FEED: BinanceLeadFeed | None = None
_COOLDOWN_UNTIL = 0.0
_COOLDOWN_RISK_MULT = 1.0


def log(msg: str):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def parse_ts(iso: str) -> float:
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


@dataclass
class Position:
    ticker: str
    series: str
    side: str          # "yes" or "no"
    contracts: float
    entry: float
    cost: float
    opened_ts: float
    close_ts: float
    order_id: str = ""
    client_order_id: str = ""
    filled: bool = False
    settled: bool = False
    result: int | None = None  # 1 if our side won
    pnl: float | None = None
    last_at_signal: float | None = None  # for paper fill de-dupe
    exit_reason: str = ""  # "" | "settle" | "stop" | "take_profit"
    exit_price: float | None = None
    exit_order_id: str = ""
    tp_price: float | None = None  # entry * TAKE_PROFIT_MULT, if reachable (<= cap)
    peak_mark: float | None = None  # highest mark seen while open (spike-fade)
    # Quant instrumentation
    signal_mid: float | None = None
    signal_spread: float | None = None
    secs_left_at_entry: float | None = None
    binance_ret: float | None = None
    binance_dir: str = ""
    binance_confirmed: bool | None = None
    risk_frac: float | None = None
    edge_wr: float | None = None
    edge_reason: str = ""
    mark_at_fill: float | None = None
    setup_tag: str = ""          # setup_gov decision tag at entry
    setup_keys: str = ""         # band|lead|phase|asset keys at entry


@dataclass
class State:
    start_equity: float
    cash: float
    mode: str
    positions: list[Position] = field(default_factory=list)
    closed: list[dict] = field(default_factory=list)
    signaled: list[str] = field(default_factory=list)  # tickers already acted on
    halted: bool = False  # True once loss floor / drawdown halt trips
    # series_root -> last settled market direction ("up"|"down")
    last_settle_dir: dict = field(default_factory=dict)
    # highest realized (flat) cash seen — basis for the trailing floor
    high_water: float = 0.0

    @property
    def open_positions(self) -> list[Position]:
        return [p for p in self.positions if not p.settled]

    @property
    def equity(self) -> float:
        # mark open filled positions at entry (conservative; true MTM unused)
        locked = sum(p.cost for p in self.open_positions if p.filled)
        return self.cash + locked

    def save(self):
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "start_equity": self.start_equity,
            "cash": self.cash,
            "mode": self.mode,
            "positions": [asdict(p) for p in self.positions],
            "closed": self.closed,
            "signaled": self.signaled,
            "halted": self.halted,
            "last_settle_dir": self.last_settle_dir,
            "high_water": self.high_water,
            "saved_at": time.time(),
        }
        STATE_PATH.write_text(json.dumps(payload, indent=2))

    @classmethod
    def load_or_new(cls, start: float, mode: str) -> "State":
        if STATE_PATH.exists():
            d = json.loads(STATE_PATH.read_text())
            st = cls(start_equity=d["start_equity"], cash=d["cash"], mode=d["mode"],
                     signaled=d.get("signaled", []), closed=d.get("closed", []),
                     halted=bool(d.get("halted", False)),
                     last_settle_dir=dict(d.get("last_settle_dir") or {}),
                     high_water=float(d.get("high_water") or 0.0))
            fields = set(Position.__dataclass_fields__)
            st.positions = [
                Position(**{k: v for k, v in p.items() if k in fields})
                for p in d.get("positions", [])
            ]
            if not st.last_settle_dir:
                st.last_settle_dir = _seed_settle_dirs(st.closed)
            log(f"resumed state equity=${st.equity:.2f} cash=${st.cash:.2f} "
                f"open={len(st.open_positions)} closed={len(st.closed)} "
                f"halted={st.halted} prior_dirs={len(st.last_settle_dir)}")
            return st
        st = cls(start_equity=start, cash=start, mode=mode)
        st.save()
        return st


def _seed_settle_dirs(closed: list[dict]) -> dict:
    """Rebuild last settle direction per series from closed settle events."""
    out: dict[str, tuple[float, str]] = {}
    for c in closed:
        if (c.get("exit_reason") or "") != "settle" and c.get("event") not in (None, "settle"):
            # closed list items are positions; prefer exit_reason==settle
            pass
        if (c.get("exit_reason") or "") != "settle":
            continue
        side = c.get("side")
        pnl = float(c.get("pnl") or 0)
        if side not in ("yes", "no") or pnl == 0:
            # pnl==0 could be scratch; skip
            if c.get("result") is None:
                continue
        won = bool(c.get("result")) if c.get("result") is not None else pnl > 0
        if side not in ("yes", "no"):
            continue
        d = time_phase.settle_direction(side, won)
        ts = float(c.get("close_ts") or c.get("opened_ts") or 0)
        ser = series_root(c.get("ticker") or "")
        if not ser:
            continue
        prev = out.get(ser)
        if prev is None or ts >= prev[0]:
            out[ser] = (ts, d)
    return {k: v[1] for k, v in out.items()}


def tp_targets_for_entry(entry: float) -> list[tuple[float, str]]:
    """Reachable take-profit (price, reason) pairs, lowest first.

    Favorites at 90¢+ cannot 2x on a $1 binary; abs/gain catch near-ceiling spikes.
    Soft entries below TAKE_PROFIT_MIN_ENTRY skip abs/gain TP and ride to settle
    (fatter payoff was the monster-hour driver).
    """
    if entry <= 0:
        return []
    out: list[tuple[float, str]] = []
    rich_enough = entry >= TAKE_PROFIT_MIN_ENTRY
    if rich_enough and TAKE_PROFIT_ABS > 0:
        abs_px = min(TAKE_PROFIT_ABS, TAKE_PROFIT_CAP)
        if abs_px > entry:
            out.append((round(abs_px, 4), "abs"))
    if not rich_enough and SOFT_SPIKE_TP > 0:
        spike_px = min(SOFT_SPIKE_TP, TAKE_PROFIT_CAP)
        if spike_px > entry:
            out.append((round(spike_px, 4), "soft_spike"))
    if rich_enough and TAKE_PROFIT_GAIN > 0:
        gain_px = round(min(entry + TAKE_PROFIT_GAIN, TAKE_PROFIT_CAP), 4)
        if gain_px > entry:
            out.append((gain_px, "gain"))
    if TAKE_PROFIT_MULT > 1.0:
        mult_px = round(entry * TAKE_PROFIT_MULT, 4)
        if mult_px <= TAKE_PROFIT_CAP and mult_px > entry:
            out.append((mult_px, "mult"))
    # de-dupe by price, keep first reason, sort ascending
    best: dict[float, str] = {}
    for px, reason in out:
        best.setdefault(px, reason)
    return sorted(best.items(), key=lambda x: x[0])


def tp_price_for_entry(entry: float) -> float | None:
    """Lowest reachable take-profit mark, or None if no upside target."""
    targets = tp_targets_for_entry(entry)
    return targets[0][0] if targets else None


def tp_hit(entry: float, mark: float) -> tuple[float, str] | None:
    """If mark has reached any TP target, return (target, reason)."""
    for px, reason in tp_targets_for_entry(entry):
        if mark >= px:
            return px, reason
    return None


def mid_of(m: dict) -> float | None:
    bid = m.get("yes_bid_dollars")
    ask = m.get("yes_ask_dollars")
    last = m.get("last_price_dollars")
    try:
        if bid is not None and ask is not None:
            b, a = float(bid), float(ask)
            if 0 < b < 1 and 0 < a < 1:
                return (b + a) / 2
        if last is not None:
            return float(last)
    except (TypeError, ValueError):
        return None
    return None


def signal_side(m: dict, mid: float) -> tuple[str, float] | None:
    """Return (side, entry_price) if mid qualifies, else None.

    Prices are set to join the touch so a post-only order can actually rest
    in the queue: buy YES at the current yes bid; buy NO by resting an ask
    at the current yes ask (entry NO price = 1 - yes_ask).
    """
    try:
        bid = float(m["yes_bid_dollars"]) if m.get("yes_bid_dollars") is not None else None
        ask = float(m["yes_ask_dollars"]) if m.get("yes_ask_dollars") is not None else None
    except (TypeError, ValueError):
        bid = ask = None

    if PRICE_LO <= mid < PRICE_HI:
        # Join/improve the YES bid by at most staying inside the spread
        if bid is not None and PRICE_LO <= bid < PRICE_HI:
            entry = round(bid, 2)
        else:
            entry = round(math.floor(mid * 100) / 100, 2)
        if PRICE_LO <= entry < PRICE_HI:
            return "yes", entry

    no_mid = 1.0 - mid
    if PRICE_LO <= no_mid < PRICE_HI:
        # Rest YES ask at the touch; NO entry = 1 - that ask
        if ask is not None:
            yes_ask = round(ask, 2)
            entry = round(1.0 - yes_ask, 2)
        else:
            entry = round(math.floor(no_mid * 100) / 100, 2)
        if PRICE_LO <= entry < PRICE_HI:
            return "no", entry
    return None


def append_trade_log(row: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(row) + "\n")


def _passive_reprice(side: str, entry: float) -> float | None:
    """Step one cent more passive after a post-only cross."""
    if side == "yes":
        nxt = round(entry - 0.01, 2)
    else:
        # raising the YES ask by 1c lowers the NO entry by 1c
        yes_ask = round(1.0 - entry, 2) + 0.01
        nxt = round(1.0 - yes_ask, 2)
    if PRICE_LO <= nxt < PRICE_HI:
        return nxt
    return None


def place_live_maker(client: KalshiClient, ticker: str, side: str, entry: float,
                     unit: float, close_ts: float) -> tuple[dict | None, str, float, Exception | None]:
    """Place post-only maker order; on cross, refresh touch and requote."""
    last_err: Exception | None = None
    for attempt in range(MAX_REQUOTES):
        book_side = "bid" if side == "yes" else "ask"
        book_price = entry if side == "yes" else round(1.0 - entry, 4)
        try:
            resp = client.create_order(
                ticker, book_side, unit, book_price, post_only=True,
                expiration_ts=int(close_ts),
            )
            return resp, side, entry, None
        except Exception as e:
            last_err = e
            err = str(e).lower()
            if "post only cross" not in err and "post_only_cross" not in err:
                return None, side, entry, e
            try:
                m = client.market(ticker)
            except Exception as e2:
                return None, side, entry, e2
            mid = mid_of(m)
            if mid is None:
                return None, side, entry, e
            sig = signal_side(m, mid)
            if sig is None or sig[0] != side:
                # band gone — step passive once from last entry as fallback
                nxt = _passive_reprice(side, entry)
            else:
                nxt = sig[1]
                # if touch unchanged, force one tick more passive
                if nxt == entry:
                    nxt = _passive_reprice(side, entry)
            if nxt is None:
                return None, side, entry, e
            log(f"post-only cross on {ticker}, requote {attempt+1}/{MAX_REQUOTES} "
                f"{side} {entry:.2f}->{nxt:.2f}")
            entry = nxt
    return None, side, entry, last_err


def effective_floor(st: State) -> float:
    """Static floor, ratcheted up by the trailing high-water rule."""
    if HALT_TRAIL_FRAC <= 0:
        return HALT_FLOOR
    return max(HALT_FLOOR, round(HALT_TRAIL_FRAC * (st.high_water or 0.0), 2))


def update_high_water(st: State) -> None:
    """Track realized high-water only when flat (open costs inflate equity)."""
    if not st.open_positions and st.cash > (st.high_water or 0.0):
        st.high_water = st.cash


def halt_reason(st: State) -> str | None:
    """Return why we should halt, or None if still trading."""
    if sizing.should_halt(st.equity, st.start_equity, floor=effective_floor(st)):
        return "loss_floor"
    if sizing.should_halt_profit(st.equity, st.start_equity, HALT_PROFIT):
        return "profit_target"
    return None


_HALT_BREACHES = 0
# Consecutive breach reads required — transient cash-vs-fill races (boot,
# balance sync landing before a fill is recorded) must not trip the floor.
HALT_CONFIRM_POLLS = int(os.environ.get("HALT_CONFIRM_POLLS", "2"))


def enforce_halt(client: KalshiClient, st: State) -> bool:
    """If loss floor or profit target hit, cancel resting orders and freeze entries."""
    global _HALT_BREACHES
    if st.halted:
        return True
    why = halt_reason(st)
    if why is None:
        _HALT_BREACHES = 0
        return False
    _HALT_BREACHES += 1
    if _HALT_BREACHES < HALT_CONFIRM_POLLS:
        log(f"halt breach {_HALT_BREACHES}/{HALT_CONFIRM_POLLS} "
            f"(equity=${st.equity:.2f}) — confirming before halt")
        return False
    st.halted = True
    profit = st.equity - st.start_equity
    if why == "profit_target":
        log(f"HALT RUN PROFIT equity=${st.equity:.2f} "
            f"(+${profit:.2f} >= target ${HALT_PROFIT:.2f}; "
            f"start ${st.start_equity:.2f}) — no new trades")
    else:
        log(f"HALT RUN equity=${st.equity:.2f} <= floor ${effective_floor(st):.2f} "
            f"(static ${HALT_FLOOR:.2f}, high_water ${st.high_water:.2f}, "
            f"start was ${st.start_equity:.2f}) — no new trades")
    for p in list(st.open_positions):
        if p.filled or not p.order_id or st.mode != "live":
            continue
        try:
            client.cancel_order(p.order_id, market_ticker=p.ticker)
            log(f"HALT cancel resting {p.ticker}")
            p.settled = True
            p.pnl = 0.0
            st.closed.append(asdict(p))
        except Exception as e:
            log(f"HALT cancel {p.ticker}: {e}")
    st.save()
    append_trade_log({
        "event": "halt", "reason": why, "equity": st.equity,
        "profit": profit, "profit_target": HALT_PROFIT,
        "floor": effective_floor(st), "static_floor": HALT_FLOOR,
        "high_water": st.high_water,
        "start_equity": st.start_equity, "cash": st.cash,
    })
    return True


def series_root(ticker: str) -> str:
    return ticker.split("-", 1)[0]


def size_mult_for(ticker: str, entry: float | None = None,
                  secs_left: float | None = None,
                  bn_size_mult: float = 1.0,
                  bn_tag: str = "") -> tuple[float, str]:
    """Position size multiplier + reason tag (satellite / soft / staged / BN)."""
    mult = SATELLITE_SIZE_MULT if series_root(ticker) in SATELLITE_SERIES else 1.0
    tags: list[str] = []
    if series_root(ticker) in SATELLITE_SERIES:
        tags.append(f"sat×{SATELLITE_SIZE_MULT:g}")
    if entry is not None and entry < SOFT_ENTRY_MAX and SOFT_ENTRY_SIZE_MULT < 1:
        mult *= SOFT_ENTRY_SIZE_MULT
        tags.append(f"soft<{SOFT_ENTRY_MAX:g}×{SOFT_ENTRY_SIZE_MULT:g}")
        if (secs_left is not None and secs_left > SOFT_ENTRY_EARLY_SECS
                and SOFT_ENTRY_EARLY_MULT < 1):
            mult *= SOFT_ENTRY_EARLY_MULT
            tags.append(f"early>{SOFT_ENTRY_EARLY_SECS:g}s×{SOFT_ENTRY_EARLY_MULT:g}")
    # Stage by time only on soft favorites — don't cut rich/late winners.
    if (STAGE_SIZE and entry is not None and entry < SOFT_ENTRY_MAX
            and secs_left is not None):
        if secs_left > 600 and STAGE_SIZE_10M_MULT < 1:
            mult *= STAGE_SIZE_10M_MULT
            tags.append(f"stage>10m×{STAGE_SIZE_10M_MULT:g}")
        elif secs_left > 300 and STAGE_SIZE_5M_MULT < 1:
            mult *= STAGE_SIZE_5M_MULT
            tags.append(f"stage>5m×{STAGE_SIZE_5M_MULT:g}")
    if bn_size_mult != 1.0:
        mult *= bn_size_mult
        tags.append(bn_tag or f"bn×{bn_size_mult:g}")
    return mult, ("+".join(tags) if tags else "full")


def apply_phase_size(ticker: str, side: str, entry: float, secs_left: float,
                     st: State, bn_mult: float, base_mult: float,
                     base_tag: str) -> tuple[float, str]:
    """Layer time-phase / optional prior-dir size on top of size_mult_for."""
    prior = (st.last_settle_dir or {}).get(series_root(ticker))
    bn_agreed = bn_mult >= 1.0  # agree boost or full; flat is <1
    phase_m, phase_tag = time_phase.phase_size_mult(
        entry, secs_left, side, prior, bn_agreed=bn_agreed,
    )
    mult = base_mult * phase_m
    tags = [t for t in (base_tag, phase_tag, time_phase.phase_label(secs_left)) if t]
    # Always keep phase label for logs
    if not phase_tag:
        tags = [base_tag or "full", time_phase.phase_label(secs_left)]
        tags = [t for t in tags if t]
    return mult, "+".join(tags)


def soft_open_count(st: State, metal: bool | None = None) -> int:
    """Count soft opens; metal=True/False splits the correlated buckets."""
    n = 0
    for p in st.open_positions:
        if (p.entry or 0) >= SOFT_ENTRY_MAX:
            continue
        is_m = metals.is_metal(p.ticker)
        if metal is True and not is_m:
            continue
        if metal is False and is_m:
            continue
        n += 1
    return n


def soft_binance_gate(ticker: str, side: str, entry: float) -> tuple[bool, float, str]:
    """Soft favorites: fast-window Binance gate + asymmetric size.

    Returns (allow, size_mult, reason_tag).
      agree  → SOFT_BN_AGREE_MULT (default 1.25×)
      flat   → SOFT_BN_FLAT_MULT (default 0.50×)
      disagree → block
    Also: BTC/ETH risk veto + taker-flow filter (inside lead feed).
    """
    if entry >= SOFT_ENTRY_MAX or not SOFT_BINANCE_STRICT:
        return True, 1.0, ""
    if not _lead_active() or LEAD_FEED is None:
        return True, SOFT_BN_FLAT_MULT, f"bnflat×{SOFT_BN_FLAT_MULT:g}(no_lead)"
    ok_rv, why_rv = LEAD_FEED.risk_veto(ticker, side)
    if not ok_rv:
        return False, 0.0, why_rv
    ok, sig, reason = LEAD_FEED.agrees(
        ticker, side,
        require_lean=False,
        block_disagree_only=True,
        window_sec=LEAD_FEED.fast_window_sec,
        base_threshold=LEAD_FEED.fast_threshold,
    )
    detail = "n/a" if sig is None else (
        f"{sig.direction}:{sig.ret_pct*100:+.3f}%/{sig.window_sec:.0f}s"
        f"|f{sig.flow_imb:+.2f}"
    )
    if not ok:
        return False, 0.0, f"{reason}:{detail}"
    if sig is None or sig.direction == "flat":
        return True, SOFT_BN_FLAT_MULT, f"bnflat×{SOFT_BN_FLAT_MULT:g}:{detail}"
    # Binance leans our way — require multi-venue confirm for full size
    mv_status, agree_n, venue_n, mv_detail = LEAD_FEED.multi_venue_confirm(ticker, side)
    mv_tag = f"mv{agree_n}/{venue_n}[{mv_detail}]"
    if mv_status == "confirmed":
        return True, SOFT_BN_AGREE_MULT, (
            f"bnagree×{SOFT_BN_AGREE_MULT:g}:{detail}+{mv_tag}"
        )
    if mv_status == "unavailable":
        # Feeds still warming — allow half size, don't block
        return True, SOFT_BN_FLAT_MULT, (
            f"bnflat×{SOFT_BN_FLAT_MULT:g}:{detail}+{mv_tag}"
        )
    # weak confirm
    if getattr(LEAD_FEED, "multi_venue_strict", False):
        return False, 0.0, f"multi_venue_weak:{detail}+{mv_tag}"
    return True, SOFT_BN_FLAT_MULT, (
        f"bnflat×{SOFT_BN_FLAT_MULT:g}:{detail}+{mv_tag}"
    )


def cooldown_risk_mult() -> float:
    if time.time() >= _COOLDOWN_UNTIL:
        return 1.0
    return _COOLDOWN_RISK_MULT


def note_loss_cooldown(st: State, pos: Position | dict, pnl: float) -> None:
    """After clustered settle/stop losses, temporarily cut risk.

    Caller should append the loss to st.closed before invoking.
    """
    global _COOLDOWN_UNTIL, _COOLDOWN_RISK_MULT
    if pnl >= 0 or LOSS_COOLDOWN_LOSSES <= 0:
        return
    close_ts = float(pos["close_ts"] if isinstance(pos, dict) else pos.close_ts)
    bucket = int(close_ts // 900) if close_ts > 0 else 0
    losses = sum(
        1 for c in st.closed[-30:]
        if (c.get("pnl") or 0) < 0
        and float(c.get("close_ts") or 0) > 0
        and int(float(c.get("close_ts") or 0) // 900) == bucket
    )
    if losses >= LOSS_COOLDOWN_LOSSES:
        _COOLDOWN_UNTIL = time.time() + LOSS_COOLDOWN_SEC
        _COOLDOWN_RISK_MULT = LOSS_COOLDOWN_RISK_MULT
        log(f"LOSS COOLDOWN {losses} losses in bucket {bucket} — "
            f"risk×{LOSS_COOLDOWN_RISK_MULT:g} for {LOSS_COOLDOWN_SEC:.0f}s")
        append_trade_log({
            "event": "loss_cooldown", "losses": losses, "bucket": bucket,
            "risk_mult": LOSS_COOLDOWN_RISK_MULT, "sec": LOSS_COOLDOWN_SEC,
        })


def book_spread(m: dict) -> float | None:
    try:
        bid = float(m["yes_bid_dollars"]) if m.get("yes_bid_dollars") is not None else None
        ask = float(m["yes_ask_dollars"]) if m.get("yes_ask_dollars") is not None else None
    except (TypeError, ValueError):
        return None
    if bid is None or ask is None:
        return None
    return max(0.0, ask - bid)


def mispricing_ok(ticker: str, side: str, entry: float, m: dict) -> tuple[bool, str]:
    """Quant gates: skip rich favorites / wide spreads unless Binance agrees hard."""
    if entry >= SKIP_ENTRY_RICH:
        # Allow only if Binance strongly agrees (early intel confirmed)
        if _lead_active() and LEAD_FEED is not None:
            ok, sig, reason = LEAD_FEED.agrees(ticker, side, require_lean=True)
            if ok and sig and sig.direction != "flat" and sig.confirmed is not False:
                return True, "rich_but_binance_agree"
        return False, f"rich_entry>={SKIP_ENTRY_RICH:.3f}"
    spr = book_spread(m)
    if spr is not None and spr > MAX_SPREAD:
        return False, f"wide_spread={spr:.3f}>{MAX_SPREAD:.3f}"
    return True, "ok"


def try_open(client: KalshiClient, st: State, m: dict, side: str, entry: float):
    if st.halted or halt_reason(st) is not None:
        enforce_halt(client, st)
        return
    ticker = m["ticker"]
    ok_m, why_m = mispricing_ok(ticker, side, entry, m)
    if not ok_m:
        log(f"skip {ticker}: mispricing gate ({why_m})")
        append_trade_log({"event": "skip_mispricing", "ticker": ticker,
                          "side": side, "entry": entry, "reason": why_m})
        return
    if metals.is_metal(ticker):
        ok_sess, why_sess = metals.metals_session_ok()
        if not ok_sess:
            log(f"skip {ticker}: metals session ({why_sess})")
            append_trade_log({"event": "skip_metals_session", "ticker": ticker,
                              "side": side, "entry": entry, "reason": why_sess})
            return
    ok_bn, bn_mult, why_bn = soft_binance_gate(ticker, side, entry)
    if not ok_bn:
        log(f"skip {ticker}: soft Binance gate ({why_bn})")
        append_trade_log({"event": "skip_soft_binance", "ticker": ticker,
                          "side": side, "entry": entry, "reason": why_bn})
        return

    try:
        last_at = float(m["last_price_dollars"]) if m.get("last_price_dollars") is not None else None
    except (TypeError, ValueError):
        last_at = None
    close_ts = parse_ts(m["close_time"])
    secs_left = close_ts - time.time()
    phase = time_phase.phase_label(secs_left)
    prior_dir = (st.last_settle_dir or {}).get(series_root(ticker))
    blocked, why_late = time_phase.late_rich_blocked(entry, secs_left)
    if blocked:
        log(f"skip {ticker}: time-phase gate ({why_late})")
        append_trade_log({
            "event": "skip_late_rich", "ticker": ticker, "side": side,
            "entry": entry, "reason": why_late, "phase": phase,
            "prior_dir": prior_dir, "secs_left": secs_left,
        })
        return
    if entry < SOFT_ENTRY_MAX:
        if metals.is_metal(ticker):
            cap = metals.METALS_SOFT_CORR_MAX
            n_soft = soft_open_count(st, metal=True)
            bucket = "metals"
        else:
            cap = SOFT_CORR_MAX
            n_soft = soft_open_count(st, metal=False)
            bucket = "crypto"
        if n_soft >= cap:
            log(f"skip {ticker}: soft corr cap {cap} [{bucket}] "
                f"(entry={entry:.2f}<{SOFT_ENTRY_MAX:g})")
            append_trade_log({"event": "skip_soft_corr", "ticker": ticker,
                              "side": side, "entry": entry, "cap": cap,
                              "bucket": bucket})
            return
    mult, mult_tag = size_mult_for(
        ticker, entry=entry, secs_left=secs_left,
        bn_size_mult=bn_mult, bn_tag=why_bn,
    )
    mult, mult_tag = apply_phase_size(
        ticker, side, entry, secs_left, st, bn_mult, mult, mult_tag,
    )
    gov_mult, gov_tag = series_gov.series_risk_mult(st.closed, series_root(ticker))
    if gov_mult != 1.0:
        mult *= gov_mult
        mult_tag = f"{mult_tag}+{gov_tag}" if mult_tag else gov_tag
    # Quant notch: size from how *this setup* (band/lead/phase/asset) has been doing
    lead_dir = ""
    if LEAD_FEED is not None:
        _sig = (LEAD_FEED.signal_fast(ticker) if entry < SOFT_ENTRY_MAX
                else LEAD_FEED.signal(ticker))
        if _sig is not None:
            lead_dir = _sig.direction or ""
    block_ice, why_ice = setup_gov.should_block_entry(
        st.closed,
        entry=entry,
        side=side,
        secs_left=secs_left,
        binance_dir=lead_dir,
        ticker=ticker,
    )
    if block_ice:
        log(f"skip {ticker}: setup ice block ({why_ice})")
        append_trade_log({
            "event": "skip_setup_ice", "ticker": ticker, "side": side,
            "entry": entry, "reason": why_ice,
        })
        return
    setup_mult, setup_tag, setup_keys = setup_gov.setup_risk_mult(
        st.closed,
        entry=entry,
        side=side,
        secs_left=secs_left,
        binance_dir=lead_dir,
        ticker=ticker,
    )
    if setup_mult != 1.0:
        mult *= setup_mult
        mult_tag = f"{mult_tag}+{setup_tag}" if mult_tag else setup_tag
    if MAX_SIZE_MULT > 0 and mult > MAX_SIZE_MULT:
        mult_tag = f"{mult_tag}+cap×{MAX_SIZE_MULT:g}"
        mult = MAX_SIZE_MULT
    # Kelly on tradable setups only — iced soft won't mute mid/rich risk
    edge_closed = setup_gov.filter_closed_for_edge(st.closed)
    risk_frac, edge = sizing.effective_risk_fraction(
        st.equity, closed=edge_closed, entry=entry, floor=effective_floor(st),
    )
    cd_mult = cooldown_risk_mult()
    if cd_mult < 1:
        risk_frac *= cd_mult
        edge = type(edge)(**{**edge.__dict__, "reason": edge.reason + "+cooldown"})
    unit = sizing.contracts_for_equity(
        st.equity, entry, size_mult=mult, risk_frac=risk_frac,
    )
    if unit <= 0:
        return
    # Already in this market?
    if any(p.ticker == ticker for p in st.open_positions):
        return
    conc_cap = sizing.max_concurrent(
        st.equity, entry, hard_cap=MAX_CONCURRENT, exposure_frac=MAX_EXPOSURE_FRAC,
        risk_frac=risk_frac,
    )
    if len(st.open_positions) >= conc_cap:
        log(f"skip {ticker}: at max concurrent {conc_cap}")
        return
    cost = unit * entry
    committed = sum(p.cost for p in st.open_positions)
    if committed + cost > st.equity * MAX_EXPOSURE_FRAC:
        log(f"skip {ticker}: exposure ${committed+cost:.2f} > "
            f"{100*MAX_EXPOSURE_FRAC:.0f}% of equity")
        return
    if cost > st.cash:
        log(f"skip {ticker}: need ${cost:.2f}, cash ${st.cash:.2f}")
        return

    mid = mid_of(m)
    spr = book_spread(m)
    if LEAD_FEED is not None and entry < SOFT_ENTRY_MAX:
        lead = LEAD_FEED.signal_fast(ticker)
    elif LEAD_FEED is not None:
        lead = LEAD_FEED.signal(ticker)
    else:
        lead = None
    tp = tp_price_for_entry(entry)
    keys_str = "|".join(f"{k}:{v}" for k, v in setup_keys.items())
    pos = Position(
        ticker=ticker, series=m.get("event_ticker", series_root(ticker)),
        side=side, contracts=unit, entry=entry, cost=cost,
        opened_ts=time.time(), close_ts=close_ts,
        last_at_signal=last_at, tp_price=tp,
        signal_mid=mid, signal_spread=spr, secs_left_at_entry=secs_left,
        binance_ret=(lead.ret_pct if lead else None),
        binance_dir=(lead.direction if lead else lead_dir),
        binance_confirmed=(lead.confirmed if lead else None),
        risk_frac=risk_frac, edge_wr=edge.wr, edge_reason=edge.reason,
        setup_tag=setup_tag, setup_keys=keys_str,
    )

    if st.mode == "live":
        resp, side, entry, err = place_live_maker(
            client, ticker, side, entry, unit, close_ts
        )
        if resp is None:
            log(f"LIVE order failed {ticker}: {err}")
            return
        pos.side = side
        pos.entry = entry
        pos.cost = unit * entry
        pos.order_id = resp.get("order_id", "")
        pos.client_order_id = resp.get("client_order_id", "")
        fill = float(resp.get("fill_count", "0") or 0)
        book_side = "bid" if side == "yes" else "ask"
        book_price = entry if side == "yes" else round(1.0 - entry, 4)
        if fill > 0:
            pos.filled = True
            pos.contracts = fill
            pos.cost = entry * fill
            pos.mark_at_fill = mid
            st.cash -= pos.cost
        targets = tp_targets_for_entry(entry)
        if targets:
            tp_note = "tp=" + ",".join(f"{px:.2f}({r})" for px, r in targets)
        else:
            tp_note = "tp=n/a (no upside to cap)"
        size_note = f"  size={mult_tag}(×{mult:g})" if mult != 1 else f"  size={mult_tag}"
        log(f"LIVE order {book_side} {unit:.2f} @ {book_price:.4f} on {ticker} "
            f"order_id={pos.order_id} fill={fill}  {tp_note}{size_note}  "
            f"phase={phase} prior={prior_dir or '-'}  "
            f"risk={100*risk_frac:.1f}%({edge.reason}) wr~{100*edge.wr:.1f}% "
            f"mid={mid} spr={spr} bn={pos.binance_dir}:{None if lead is None else f'{lead.ret_pct*100:+.3f}%'}")
    else:
        targets = tp_targets_for_entry(entry)
        tp_note = ("tp=" + ",".join(f"{px:.2f}({r})" for px, r in targets)
                   if targets else "tp=n/a")
        size_note = f"  size={mult_tag}(×{mult:g})" if mult != 1 else f"  size={mult_tag}"
        log(f"PAPER rest {side.upper()} {unit:.2f} @ {entry:.2f} on {ticker} "
            f"(mid signal, {int(secs_left)}s to close)  {tp_note}{size_note}  "
            f"phase={phase} prior={prior_dir or '-'}  "
            f"risk={100*risk_frac:.1f}%({edge.reason})")

    st.positions.append(pos)
    st.signaled.append(ticker)
    st.save()
    append_trade_log({
        "event": "signal", "mode": st.mode,
        "edge_ev": edge.ev_per_trade, "edge_kelly": edge.kelly,
        "edge_n": edge.n,
        "phase": phase, "prior_dir": prior_dir,
        "size_mult": mult, "size_tag": mult_tag,
        **asdict(pos),
    })


def sync_live_cash(client: KalshiClient, st: State):
    """Refresh cash from Kalshi balance; equity = cash + open filled cost."""
    try:
        bal = client.balance()
        dollars = float(bal.get("balance_dollars") or (bal.get("balance", 0) / 100))
        # balance_dollars is free cash; portfolio_value is marked open positions
        port = float(bal.get("portfolio_value") or 0)
        # portfolio_value may be in cents on older payloads
        if port > 1000 and dollars < 100:
            port = port / 100.0
        st.cash = dollars
        return dollars + port
    except Exception as e:
        log(f"balance sync failed: {e}")
        return st.equity


def update_live_fills(client: KalshiClient, st: State):
    """Poll resting live orders for fills / cancels."""
    for p in st.open_positions:
        if p.filled or not p.order_id:
            continue
        try:
            o = client.get_order(p.order_id)
        except Exception as e:
            log(f"get_order {p.order_id}: {e}")
            continue
        fill = float(o.get("fill_count_fp") or o.get("fill_count") or 0)
        status = o.get("status")
        if fill > 0 and not p.filled:
            # cost: prefer maker_fill_cost, else entry * fill
            cost_s = o.get("maker_fill_cost_dollars") or o.get("taker_fill_cost_dollars")
            try:
                cost = float(cost_s) if cost_s not in (None, "", "0", "0.0000") else p.entry * fill
            except (TypeError, ValueError):
                cost = p.entry * fill
            # if cost looks like cents integer leftover, ignore
            p.filled = True
            p.contracts = fill
            p.cost = cost
            if p.mark_at_fill is None:
                p.mark_at_fill = p.signal_mid
            sync_live_cash(client, st)
            log(f"LIVE FILL {p.side.upper()} {fill:.2f} @ ~{p.entry:.2f} on {p.ticker} "
                f"status={status} cash=${st.cash:.2f} "
                f"risk={None if p.risk_frac is None else f'{100*p.risk_frac:.1f}%'} "
                f"bn={p.binance_dir}")
            append_trade_log({"event": "fill", "mode": "live", "status": status,
                              **asdict(p)})
            st.save()
        elif status == "canceled" and fill <= 0:
            log(f"LIVE cancel unfilled {p.ticker} order={p.order_id}")
            p.settled = True
            p.pnl = 0.0
            st.closed.append(asdict(p))
            st.save()


def update_paper_fills(st: State, mkt: dict):
    """Fill resting paper orders when at the touch and a new trade prints, or
    when the book crosses us. PAPER_FILL=backtest fills on the next poll
    (matches the research mid-fill assumption — optimistic).
    """
    ticker = mkt["ticker"]
    fill_mode = os.environ.get("PAPER_FILL", "touch").lower()
    try:
        last_f = float(mkt["last_price_dollars"]) if mkt.get("last_price_dollars") is not None else None
        bid_f = float(mkt["yes_bid_dollars"]) if mkt.get("yes_bid_dollars") is not None else None
        ask_f = float(mkt["yes_ask_dollars"]) if mkt.get("yes_ask_dollars") is not None else None
        vol = float(mkt.get("volume_fp") or mkt.get("volume") or 0)
    except (TypeError, ValueError):
        return

    for p in st.open_positions:
        if p.ticker != ticker or p.filled:
            continue
        if time.time() - p.opened_ts < POLL_SEC:
            continue
        filled = False
        new_trade = last_f is not None and last_f != p.last_at_signal
        if fill_mode == "backtest":
            filled = True
        elif p.side == "yes":
            # crossed, or at/inside bid with a fresh trade at <= entry
            if ask_f is not None and ask_f <= p.entry:
                filled = True
            elif new_trade and last_f <= p.entry and bid_f is not None and bid_f >= p.entry - 0.001:
                filled = True
        else:
            yes_px = round(1 - p.entry, 4)
            if bid_f is not None and bid_f >= yes_px:
                filled = True
            elif new_trade and last_f is not None and last_f >= yes_px - 0.001 \
                    and ask_f is not None and ask_f <= yes_px + 0.001:
                filled = True
        if filled:
            p.filled = True
            st.cash -= p.cost
            log(f"PAPER FILL ({fill_mode}) {p.side.upper()} {p.contracts:.2f} @ "
                f"{p.entry:.2f} on {p.ticker}  cash=${st.cash:.2f}")
            append_trade_log({"event": "fill", "fill_mode": fill_mode, **asdict(p)})
            st.save()


def side_mark(m: dict, side: str) -> float | None:
    """Mark price of our side from the YES book (bid for long YES, 1-ask for long NO)."""
    try:
        bid = float(m["yes_bid_dollars"]) if m.get("yes_bid_dollars") is not None else None
        ask = float(m["yes_ask_dollars"]) if m.get("yes_ask_dollars") is not None else None
        last = float(m["last_price_dollars"]) if m.get("last_price_dollars") is not None else None
    except (TypeError, ValueError):
        return None
    if side == "yes":
        # what we could sell YES for now
        if bid is not None:
            return bid
        if last is not None:
            return last
    else:
        # NO mark = 1 - yes ask (what we'd pay to buy YES / receive selling NO)
        if ask is not None:
            return 1.0 - ask
        if last is not None:
            return 1.0 - last
    return None


def stop_triggered(entry: float, mark: float) -> bool:
    return mark <= entry * (1.0 - STOP_LOSS_PCT)


def close_position_exit(client: KalshiClient, st: State, p: Position, mark: float,
                        reason: str):
    """Flatten a filled position (stop or take-profit). Live: IOC reduce-only."""
    if p.settled or not p.filled:
        return
    exit_px = mark
    label = {"stop": "STOP", "spike_fade": "SPIKE FADE",
             "whale_harvest": "WHALE HARVEST"}.get(reason, "TAKE PROFIT")
    if st.mode == "live":
        try:
            if p.side == "yes":
                # For TP, sell into bid aggressively; for stop same
                resp = client.create_order(
                    p.ticker, "ask", p.contracts, 0.01,
                    post_only=False, time_in_force="immediate_or_cancel",
                    reduce_only=True,
                )
            else:
                resp = client.create_order(
                    p.ticker, "bid", p.contracts, 0.99,
                    post_only=False, time_in_force="immediate_or_cancel",
                    reduce_only=True,
                )
            p.exit_order_id = resp.get("order_id", "")
            fill = float(resp.get("fill_count", "0") or 0)
            avg = resp.get("average_fill_price")
            if avg is not None:
                avg_f = float(avg)
                exit_px = avg_f if p.side == "yes" else (1.0 - avg_f)
            if fill <= 0:
                log(f"{label} IOC no fill {p.ticker} — will retry next poll")
                return
            p.contracts = fill
        except Exception as e:
            log(f"{label} exit failed {p.ticker}: {e}")
            return
        sync_live_cash(client, st)
    else:
        st.cash += exit_px * p.contracts

    pnl = exit_px * p.contracts - p.cost
    if st.mode == "live":
        sync_live_cash(client, st)

    p.exit_price = exit_px
    p.exit_reason = reason
    p.pnl = pnl
    p.result = 1 if pnl > 0 else 0
    p.settled = True
    st.closed.append(asdict(p))
    if pnl < 0:
        note_loss_cooldown(st, p, pnl)
    log(f"{label} {p.ticker} {p.side.upper()} entry={p.entry:.2f} mark={mark:.2f} "
        f"exit~{exit_px:.2f} pnl={pnl:+.4f} cash=${st.cash:.2f}")
    append_trade_log({"event": reason, "mark": mark, "exit_price": exit_px,
                      "pnl": pnl, "cash": st.cash, **asdict(p)})
    st.save()


_LAST_HARVEST_TS = 0.0


def whale_harvest(client: KalshiClient, st: State,
                  marks: list[tuple[Position, float]]) -> bool:
    """Convert a marked-equity spike into flat cash (floor can then ratchet)."""
    global _LAST_HARVEST_TS
    if not EQUITY_HARVEST or not marks:
        return False
    now = time.time()
    if now - _LAST_HARVEST_TS < HARVEST_COOLDOWN_SEC:
        return False
    marked_eq = st.cash + sum(mk * p.contracts for p, mk in marks)
    baseline = max(st.high_water or 0.0, st.cash)
    if baseline <= 0 or marked_eq < baseline * HARVEST_TRIGGER_FRAC:
        return False
    winners = [(p, mk) for p, mk in marks
               if mk >= HARVEST_MIN_MARK and mk > p.entry]
    if not winners:
        return False
    _LAST_HARVEST_TS = now
    log(f"WHALE HARVEST trigger: marked=${marked_eq:.2f} ≥ "
        f"{HARVEST_TRIGGER_FRAC:g}× baseline ${baseline:.2f} — "
        f"selling {len(winners)} winners ≥{HARVEST_MIN_MARK:.2f}")
    append_trade_log({"event": "whale_harvest_trigger",
                      "marked_equity": marked_eq, "baseline": baseline,
                      "n_winners": len(winners), "cash": st.cash})
    for p, mk in winners:
        close_position_exit(client, st, p, mk, "whale_harvest")
    return True


def check_exits(client: KalshiClient, st: State, markets_by_ticker: dict):
    """Stop-loss and per-trade take-profit (3x entry when attainable)."""
    now = time.time()
    live_marks: list[tuple[Position, float]] = []
    for p in list(st.open_positions):
        if not p.filled or p.settled:
            continue
        secs_left = p.close_ts - now
        if secs_left <= 0:
            continue  # book marks unreliable after close
        m = markets_by_ticker.get(p.ticker)
        if not m:
            try:
                m = client.market(p.ticker)
            except Exception:
                continue
        mark = side_mark(m, p.side)
        if mark is None:
            continue
        live_marks.append((p, mark))
    whale_harvest(client, st, live_marks)

    for p, mark in live_marks:
        if p.settled:
            continue  # harvested above
        secs_left = p.close_ts - now
        if p.peak_mark is None or mark > p.peak_mark:
            p.peak_mark = mark

        # Take-profit: near-ceiling spike, +gain from entry, or Nx on cheap entries
        hit = tp_hit(p.entry, mark)
        if hit is not None:
            tp, reason = hit
            log(f"tp trigger {p.ticker} {p.side} entry={p.entry:.2f} mark={mark:.2f} "
                f"target={tp:.2f} ({reason})")
            close_position_exit(client, st, p, mark, "take_profit")
            continue

        # Spike-fade guard: lock gains if a big spike starts reverting.
        if (SPIKE_FADE and p.peak_mark is not None
                and p.peak_mark >= SPIKE_PEAK
                and mark <= p.peak_mark - SPIKE_GIVEBACK
                and mark >= p.entry + SPIKE_MIN_GAIN
                and secs_left > STOP_DISABLE_SECS):
            log(f"spike fade {p.ticker} {p.side} entry={p.entry:.2f} "
                f"peak={p.peak_mark:.2f} mark={mark:.2f} — locking gain")
            close_position_exit(client, st, p, mark, "spike_fade")
            continue

        # Stop-loss (off when STOP_LOSS_PCT <= 0); also disabled in final minute
        if STOP_LOSS_PCT <= 0 or secs_left <= STOP_DISABLE_SECS:
            continue
        if stop_triggered(p.entry, mark):
            log(f"stop trigger {p.ticker} {p.side} entry={p.entry:.2f} mark={mark:.2f} "
                f"threshold={p.entry * (1 - STOP_LOSS_PCT):.2f}")
            close_position_exit(client, st, p, mark, "stop")


def settle_due(client: KalshiClient, st: State):
    now = time.time()
    for p in list(st.open_positions):
        # cancel resting live orders a few seconds after close if still open
        if st.mode == "live" and not p.filled and p.order_id and now >= p.close_ts + 5:
            try:
                client.cancel_order(p.order_id, market_ticker=p.ticker)
                log(f"LIVE cancel past-close {p.ticker}")
            except Exception as e:
                # already filled/canceled is fine
                if "404" not in str(e) and "not found" not in str(e).lower():
                    log(f"cancel {p.ticker}: {e}")

        if now < p.close_ts + 20:
            continue
        # final fill check before settling
        if st.mode == "live" and p.order_id and not p.filled:
            update_live_fills(client, st)

        try:
            m = client.market(p.ticker)
        except Exception as e:
            log(f"settle fetch failed {p.ticker}: {e}")
            continue
        status = m.get("status")
        result = m.get("result")
        if status not in ("finalized", "determined", "settled") and result not in ("yes", "no"):
            if not p.filled and now > p.close_ts + 45:
                log(f"expire unfilled {p.ticker}")
                p.settled = True
                p.pnl = 0.0
                st.closed.append(asdict(p))
                st.save()
            continue
        won = (result == "yes" and p.side == "yes") or (result == "no" and p.side == "no")
        if not p.filled:
            log(f"settle skip unfilled {p.ticker} result={result}")
            p.settled = True
            p.pnl = 0.0
            p.result = int(won)
            st.closed.append(asdict(p))
            st.save()
            continue
        payout = p.contracts * (1.0 if won else 0.0)
        pnl = payout - p.cost
        p.settled = True
        p.result = int(won)
        p.pnl = pnl
        p.exit_reason = "settle"
        p.exit_price = 1.0 if won else 0.0
        if st.mode == "live":
            sync_live_cash(client, st)
        else:
            st.cash += payout
        st.closed.append(asdict(p))
        # Markout vs entry: settle payout/contract - entry (favorites ~ +0.04 to +0.10)
        markout = (1.0 if won else 0.0) - p.entry
        settle_dir = time_phase.settle_direction(p.side, won)
        st.last_settle_dir[series_root(p.ticker)] = settle_dir
        log(f"SETTLE {p.ticker} {p.side.upper()} {'WIN' if won else 'LOSS'} "
            f"pnl={pnl:+.4f} markout/c={markout:+.3f}  "
            f"cash=${st.cash:.2f} equity=${st.equity:.2f} "
            f"risk={None if p.risk_frac is None else f'{100*p.risk_frac:.1f}%'} "
            f"bn={p.binance_dir}:{None if p.binance_ret is None else f'{p.binance_ret*100:+.3f}%'} "
            f"dir={settle_dir}")
        append_trade_log({
            "event": "settle", "won": won, "pnl": pnl,
            "markout_per_contract": markout,
            "settle_dir": settle_dir,
            "cash": st.cash, "equity": st.equity, **asdict(p),
        })
        if not won:
            note_loss_cooldown(st, p, pnl)
        st.save()


def summary(st: State) -> str:
    closed = [c for c in st.closed if c.get("filled")]
    rf, edge = sizing.effective_risk_fraction(
        st.equity, closed=st.closed, floor=effective_floor(st),
    )
    unit = sizing.contracts_for_equity(st.equity, risk_frac=rf)
    n = len(closed)
    if n == 0:
        return (f"equity=${st.equity:.2f} cash=${st.cash:.2f} "
                f"open={len(st.open_positions)} closed=0  unit={unit:.2f}  "
                f"risk={100*rf:.1f}%({edge.reason})")
    wins = sum(1 for c in closed if c.get("result") == 1)
    pnl = sum(c.get("pnl") or 0 for c in closed)
    return (f"equity=${st.equity:.2f} cash=${st.cash:.2f} "
            f"open={len(st.open_positions)} closed={n} "
            f"win%={100*wins/n:.0f} pnl={pnl:+.4f}  "
            f"unit={unit:.2f}  risk={100*rf:.1f}%({edge.reason}) "
            f"edge_wr={100*edge.wr:.1f}% ev=${edge.ev_per_trade:+.3f}")


def handle_stop(signum, frame):
    global RUNNING
    RUNNING = False
    log("shutting down...")


def _lead_active() -> bool:
    return bool(
        BINANCE_LEAD
        and LEAD_FEED is not None
        and BINANCE_LEAD_MODE not in ("off", "0", "false")
    )


def binance_allows(ticker: str, side: str) -> bool:
    """Apply Binance lead filter to a Kalshi favorite signal.

    filter: block only when Binance has a strong opposite lean
    strict: require Binance lean to match Kalshi side (yes=up, no=down)
    off / disabled: always allow
    """
    if not _lead_active() or symbol_for(ticker) is None:
        return True
    require = BINANCE_LEAD_MODE == "strict"
    ok, sig, reason = LEAD_FEED.agrees(ticker, side, require_lean=require)
    if sig is None:
        return True
    detail = (f"{sig.symbol} {sig.direction} {sig.ret_pct*100:+.3f}%/"
              f"{sig.window_sec:.0f}s @{sig.price:g}")
    if ok:
        if reason == "agree":
            log(f"binance LEAN {ticker} {side} ← {detail}")
        return True
    log(f"binance BLOCK {ticker} {side} ← {detail} ({reason})")
    append_trade_log({
        "event": "binance_block",
        "ticker": ticker,
        "side": side,
        "reason": reason,
        "symbol": sig.symbol,
        "direction": sig.direction,
        "ret_pct": sig.ret_pct,
        "price": sig.price,
        "window_sec": sig.window_sec,
        "source": sig.source,
    })
    return False


def sync_lead_symbols(st: State) -> None:
    """Track Binance symbols for every configured series + open position."""
    if LEAD_FEED is None:
        return
    wanted: set[str] = set()
    for series in ALL_SERIES:
        sym = symbol_for(series.strip())
        if sym:
            wanted.add(sym)
    for p in st.open_positions:
        sym = symbol_for(p.ticker)
        if sym:
            wanted.add(sym)
    added = LEAD_FEED.ensure_symbols(wanted)
    if added:
        log(f"binance lead added symbols={added}")


def binance_manage_opens(client: KalshiClient, st: State) -> None:
    """Use Binance lean on live opens for all bot markets.

    - Unfilled resting orders: cancel if Binance strongly opposes our side
      (stale favorite after an underlying flip).
    - Filled positions: log when Binance agrees/disagrees (info only; we still
      hold to settle / spike TP — no stop-loss).
    """
    if not _lead_active():
        return
    sync_lead_symbols(st)
    require = BINANCE_LEAD_MODE == "strict"
    for p in list(st.open_positions):
        if symbol_for(p.ticker) is None:
            continue
        ok, sig, reason = LEAD_FEED.agrees(p.ticker, p.side, require_lean=require)
        if sig is None or sig.price <= 0:
            continue
        detail = (f"{sig.symbol} {sig.direction} {sig.ret_pct*100:+.3f}%/"
                  f"{sig.window_sec:.0f}s @{sig.price:g}")

        # Cancel unfilled rests that Binance now opposes
        if not p.filled and p.order_id and reason == "disagree":
            log(f"binance CANCEL resting {p.ticker} {p.side} ← {detail}")
            if st.mode == "live":
                try:
                    client.cancel_order(p.order_id, market_ticker=p.ticker)
                except Exception as e:
                    log(f"binance cancel failed {p.ticker}: {e}")
                    continue
            p.settled = True
            p.pnl = 0.0
            p.exit_reason = "binance_cancel"
            st.closed.append(asdict(p))
            # allow a fresh signal later in the window if lean flips back
            if p.ticker in st.signaled:
                try:
                    st.signaled.remove(p.ticker)
                except ValueError:
                    pass
            st.save()
            append_trade_log({
                "event": "binance_cancel",
                "ticker": p.ticker,
                "side": p.side,
                "reason": reason,
                "symbol": sig.symbol,
                "direction": sig.direction,
                "ret_pct": sig.ret_pct,
                "price": sig.price,
                "mode": st.mode,
            })
            continue

        # Filled: surface lean vs position (throttled)
        if p.filled and reason in ("agree", "disagree"):
            now = time.time()
            note_key = f"{p.ticker}:{p.side}:{reason}"
            last = _BINANCE_NOTE_TS.get(note_key, 0.0)
            if now - last >= 30:
                _BINANCE_NOTE_TS[note_key] = now
                tag = "CONFIRM" if reason == "agree" else "WARN"
                log(f"binance {tag} open {p.ticker} {p.side} ← {detail}")


_BINANCE_NOTE_TS: dict[str, float] = {}
_BINANCE_INTEL_TS: dict[str, float] = {}


def binance_intel(ticker: str, mid: float | None, secs_left: float) -> str | None:
    """Early intel: Binance already leaned, Kalshi mid still looks stale.

    Returns suggested Kalshi side ('yes'/'no') when Binance moved first,
    else None. Does not place orders by itself — used to log + bias filters.
    """
    if not _lead_active() or mid is None or symbol_for(ticker) is None:
        return None
    sig = LEAD_FEED.signal(ticker)
    if sig is None or sig.direction == "flat" or sig.price <= 0:
        return None

    # Binance UP => Kalshi YES should get expensive; if yes-mid still soft, stale
    # Binance DOWN => Kalshi NO should get expensive; if yes-mid still high, stale
    if sig.direction == "up":
        suggested = "yes"
        stale = mid < 0.85  # Kalshi hasn't fully priced the up move yet
    else:
        suggested = "no"
        stale = mid > 0.15  # yes still bid — down move not fully priced

    if not stale:
        return None

    now = time.time()
    key = f"{ticker}:{sig.direction}"
    if now - _BINANCE_INTEL_TS.get(key, 0.0) < 20:
        return suggested
    _BINANCE_INTEL_TS[key] = now
    log(
        f"binance INTEL {ticker} {sig.symbol} {sig.direction} "
        f"{sig.ret_pct*100:+.3f}%/{sig.window_sec:.0f}s @{sig.price:g} "
        f"but Kalshi mid={mid:.3f} still stale → lean {suggested} "
        f"({secs_left:.0f}s left)"
    )
    append_trade_log({
        "event": "binance_intel",
        "ticker": ticker,
        "suggested_side": suggested,
        "kalshi_mid": mid,
        "secs_left": secs_left,
        "symbol": sig.symbol,
        "direction": sig.direction,
        "ret_pct": sig.ret_pct,
        "price": sig.price,
        "window_sec": sig.window_sec,
        "source": sig.source,
    })
    return suggested


def main():
    global LEAD_FEED
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    demo = os.environ.get("KALSHI_DEMO", "").lower() in ("1", "true", "yes")
    client = KalshiClient(demo=demo)
    if MODE == "live" and not client.can_trade:
        log("MODE=live but no API keys set. Export KALSHI_API_KEY_ID and "
            "KALSHI_PRIVATE_KEY or KALSHI_PRIVATE_KEY_PATH. Aborting.")
        sys.exit(1)

    if BINANCE_LEAD and BINANCE_LEAD_MODE not in ("off", "0", "false"):
        syms = sorted({
            s for series in ALL_SERIES
            if (s := symbol_for(series.strip()))
        })
        if syms:
            LEAD_FEED = BinanceLeadFeed(symbols=syms)
            LEAD_FEED.start()
            log(f"binance lead ON mode={BINANCE_LEAD_MODE} symbols={LEAD_FEED.symbols} "
                f"window={LEAD_FEED.window_sec:.0f}s "
                f"thresh={100*LEAD_FEED.base_threshold:.3f}%  "
                f"fast={LEAD_FEED.fast_window_sec:.0f}s@"
                f"{100*LEAD_FEED.fast_threshold:.3f}%  "
                f"taker_flow={'ON' if LEAD_FEED.taker_flow else 'OFF'}  "
                f"risk_veto={'ON' if LEAD_FEED.risk_veto_enabled else 'OFF'}"
                f"@{100*LEAD_FEED.risk_veto_pct:.2f}%  "
                f"multi_venue={'ON' if LEAD_FEED.multi_venue else 'OFF'}"
                f"≥{LEAD_FEED.multi_venue_min}")
            # warm up a couple samples so first signals aren't empty
            time.sleep(min(4.0, LEAD_FEED.poll_sec * 2))
            log(LEAD_FEED.status_line())
        else:
            log("binance lead enabled but no mapped series symbols")

    st = State.load_or_new(START_EQUITY, MODE)
    if st.mode == "live":
        eq = sync_live_cash(client, st)
        if not st.closed and not st.positions:
            st.start_equity = st.cash
            st.save()
        log(f"live balance cash=${st.cash:.4f} (equity~${eq:.4f})")
    bank = st.cash if st.mode == "live" else st.start_equity
    log(f"starting MODE={st.mode}  "
        f"{sizing.describe(bank, floor=HALT_FLOOR, closed=st.closed)}")
    log(f"series={ALL_SERIES}  satellites={sorted(SATELLITE_SERIES)}×{SATELLITE_SIZE_MULT}  "
        f"window={WINDOW_SEC}s  min_left={MIN_SECS_LEFT}s  "
        f"confirm={CONFIRM_POLLS}  max_concurrent={MAX_CONCURRENT}  "
        f"exposure≤{100*MAX_EXPOSURE_FRAC:.0f}%  price=[{PRICE_LO},{PRICE_HI})  "
        f"stop_loss={'OFF' if STOP_LOSS_PCT <= 0 else f'{100*STOP_LOSS_PCT:.0f}% (off last {STOP_DISABLE_SECS}s)'}  "
        f"take_profit="
        f"{'abs≥'+format(TAKE_PROFIT_ABS,'.2f') if TAKE_PROFIT_ABS>0 else 'absOFF'}|"
        f"{'gain+'+format(TAKE_PROFIT_GAIN,'.2f') if TAKE_PROFIT_GAIN>0 else 'gainOFF'}|"
        f"{(str(int(TAKE_PROFIT_MULT))+'x') if TAKE_PROFIT_MULT>1 else 'multOFF'} "
        f"(cap {TAKE_PROFIT_CAP:.2f}"
        f"{'' if TAKE_PROFIT_MIN_ENTRY<=0 else f', tp≥entry{TAKE_PROFIT_MIN_ENTRY:.2f}'}"
        f"{f', soft_spike≥{SOFT_SPIKE_TP:.2f}' if SOFT_SPIKE_TP>0 else ''}"
        f"{f', fade@{SPIKE_PEAK:.2f}-{SPIKE_GIVEBACK:.2f}' if SPIKE_FADE else ''})  "
        f"halt_floor=${HALT_FLOOR:.2f}"
        f"{f'+trail{HALT_TRAIL_FRAC:g}×HW' if HALT_TRAIL_FRAC > 0 else ''}  "
        f"halt_profit={'OFF' if HALT_PROFIT <= 0 else f'+${HALT_PROFIT:.2f}'}  "
        f"soft_entry=<{SOFT_ENTRY_MAX:g}×{SOFT_ENTRY_SIZE_MULT:g}"
        f"{f'/early>{SOFT_ENTRY_EARLY_SECS:g}s×{SOFT_ENTRY_EARLY_MULT:g}' if SOFT_ENTRY_EARLY_MULT < 1 else ''}  "
        f"soft_corr≤{SOFT_CORR_MAX}"
        f"/metals≤{metals.METALS_SOFT_CORR_MAX}  "
        f"metals_session={'ON' if metals.METALS_SESSION else 'OFF'}  "
        f"phase=early≥{time_phase.EARLY_WINDOW_SEC:.0f}s×{time_phase.EARLY_SIZE_MULT:g}/"
        f"late≤{time_phase.LATE_WINDOW_SEC:.0f}s≠≥{time_phase.LATE_RICH_ENTRY:g}/"
        f"prior_bias={'ON' if time_phase.PRIOR_DIR_BIAS else 'OFF'}  "
        f"{series_gov.describe()}  "
        f"{setup_gov.describe()}  "
        f"stage_size={'ON' if STAGE_SIZE else 'OFF'}  "
        f"soft_bn_strict={'ON' if SOFT_BINANCE_STRICT else 'OFF'}  "
        f"loss_cooldown={LOSS_COOLDOWN_LOSSES}@{LOSS_COOLDOWN_SEC:.0f}s×{LOSS_COOLDOWN_RISK_MULT:g}  "
        f"binance_lead={'OFF' if not (BINANCE_LEAD and LEAD_FEED) else BINANCE_LEAD_MODE}")
    if st.halted:
        log(f"already HALTED from prior run — settling only, no new trades")
    elif HALT_PROFIT > 0:
        tgt = st.start_equity + HALT_PROFIT
        log(f"profit pause armed: halt new entries at equity >= ${tgt:.2f} "
            f"(+${HALT_PROFIT:.2f} from start ${st.start_equity:.2f})")
    if setup_gov.ENABLED:
        axis_lines = setup_gov.summarize_axes(st.closed)
        if axis_lines:
            log("setup_gov axes: " + " | ".join(axis_lines[:8]))
        else:
            log("setup_gov axes: warming (need more classified closes)")

    pending: dict[str, dict] = {}  # ticker -> {side, hits, entry}
    last_summary = 0.0
    last_watch: dict[str, float] = {}
    try:
        while RUNNING:
            try:
                if st.mode == "live":
                    update_live_fills(client, st)
                    sync_live_cash(client, st)
                binance_manage_opens(client, st)
                update_high_water(st)
                enforce_halt(client, st)
                settle_due(client, st)
                now = time.time()
                markets_by_ticker: dict[str, dict] = {}
                seen_tickers: set[str] = set()
                for series in ALL_SERIES:
                    try:
                        markets = client.open_markets(series)
                    except Exception as e:
                        log(f"open_markets {series}: {e}")
                        continue
                    for m in markets:
                        ticker = m["ticker"]
                        seen_tickers.add(ticker)
                        close_ts = parse_ts(m["close_time"])
                        secs_left = close_ts - now

                        try:
                            m = client.market(ticker)
                        except Exception:
                            pass
                        markets_by_ticker[ticker] = m

                        if st.mode == "paper":
                            update_paper_fills(st, m)

                        if st.halted:
                            pending.pop(ticker, None)
                            continue
                        if ticker in st.signaled:
                            pending.pop(ticker, None)
                            continue
                        if secs_left <= 0 or secs_left > WINDOW_SEC:
                            pending.pop(ticker, None)
                            continue
                        if secs_left < MIN_SECS_LEFT:
                            pending.pop(ticker, None)
                            continue

                        mid = mid_of(m)
                        if mid is None:
                            continue
                        # Early warning: Binance moved, Kalshi book still lagging
                        binance_intel(ticker, mid, secs_left)
                        sig = signal_side(m, mid)
                        if sig is None:
                            pending.pop(ticker, None)
                            # In-window but no 90–97¢ favorite — say why (throttled)
                            fav = max(mid, 1.0 - mid)
                            if now - last_watch.get(ticker, 0.0) >= 30:
                                last_watch[ticker] = now
                                log(f"watch {ticker} {secs_left:.0f}s left mid={mid:.3f} "
                                    f"fav≈{fav:.3f} — need [{PRICE_LO},{PRICE_HI}) "
                                    f"{'too rich' if fav >= PRICE_HI else 'too cheap/coin-flip'}")
                            continue
                        side, entry = sig
                        hit = pending.get(ticker)
                        if hit is None or hit["side"] != side:
                            pending[ticker] = {"side": side, "hits": 1, "entry": entry}
                            log(f"signal pending {ticker} mid={mid:.3f} -> {side} @{entry:.2f} "
                                f"(1/{CONFIRM_POLLS}, {secs_left:.0f}s left)")
                            continue
                        hit["hits"] += 1
                        hit["entry"] = entry
                        if hit["hits"] < CONFIRM_POLLS:
                            log(f"signal pending {ticker} mid={mid:.3f} -> {side} @{entry:.2f} "
                                f"({hit['hits']}/{CONFIRM_POLLS}, {secs_left:.0f}s left)")
                            continue
                        log(f"signal confirmed {ticker} mid={mid:.3f} -> {side} @{entry:.2f} "
                            f"({secs_left:.0f}s left)")
                        if not binance_allows(ticker, side):
                            # Keep pending so a later agreeing lean can still fire
                            # within the window; do not mark signaled.
                            continue
                        pending.pop(ticker, None)
                        try_open(client, st, m, side, entry)

                # drop pending for markets that disappeared
                for t in list(pending):
                    if t not in seen_tickers:
                        pending.pop(t, None)

                check_exits(client, st, markets_by_ticker)

                if now - last_summary > 60:
                    if st.mode == "live":
                        sync_live_cash(client, st)
                    halt_tag = "  HALTED" if st.halted else ""
                    log(summary(st) + halt_tag)
                    if LEAD_FEED is not None:
                        log(LEAD_FEED.status_line())
                    last_summary = now
            except Exception as e:
                log(f"loop error: {e}")
            time.sleep(POLL_SEC)
    finally:
        if LEAD_FEED is not None:
            LEAD_FEED.stop()

    st.save()
    log(f"stopped. {summary(st)}")


if __name__ == "__main__":
    main()
