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
from bot import sizing

# Prefer the books where the 31-day EV was significantly positive.
SERIES = os.environ.get("SERIES", "KXBNB15M,KXSOL15M,KXXRP15M").split(",")
START_EQUITY = float(os.environ.get("START_EQUITY", "20"))
MODE = os.environ.get("MODE", "paper").lower()  # paper | live
POLL_SEC = float(os.environ.get("POLL_SEC", "5"))
PRICE_LO = float(os.environ.get("PRICE_LO", "0.90"))
PRICE_HI = float(os.environ.get("PRICE_HI", "0.97"))
# Signal window: last N seconds before close
WINDOW_SEC = int(os.environ.get("WINDOW_SEC", "180"))
STATE_PATH = Path(os.environ.get("STATE_PATH", "bot/state.json"))
LOG_PATH = Path(os.environ.get("LOG_PATH", "bot/trades.jsonl"))

RUNNING = True


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


@dataclass
class State:
    start_equity: float
    cash: float
    mode: str
    positions: list[Position] = field(default_factory=list)
    closed: list[dict] = field(default_factory=list)
    signaled: list[str] = field(default_factory=list)  # tickers already acted on

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
            "saved_at": time.time(),
        }
        STATE_PATH.write_text(json.dumps(payload, indent=2))

    @classmethod
    def load_or_new(cls, start: float, mode: str) -> "State":
        if STATE_PATH.exists():
            d = json.loads(STATE_PATH.read_text())
            st = cls(start_equity=d["start_equity"], cash=d["cash"], mode=d["mode"],
                     signaled=d.get("signaled", []), closed=d.get("closed", []))
            st.positions = [Position(**p) for p in d.get("positions", [])]
            log(f"resumed state equity=${st.equity:.2f} cash=${st.cash:.2f} "
                f"open={len(st.open_positions)} closed={len(st.closed)}")
            return st
        st = cls(start_equity=start, cash=start, mode=mode)
        st.save()
        return st


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


def signal_side(mid: float) -> tuple[str, float] | None:
    """Return (side, entry_price) if mid qualifies, else None.
    side 'yes' means buy YES at entry; 'no' means buy NO at entry
    (which is resting an ask at 1-entry on the YES book)."""
    if PRICE_LO <= mid < PRICE_HI:
        return "yes", round(math.floor(mid * 100) / 100, 2)
    no_price = 1.0 - mid
    if PRICE_LO <= no_price < PRICE_HI:
        return "no", round(math.floor(no_price * 100) / 100, 2)
    return None


def append_trade_log(row: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(row) + "\n")


def try_open(client: KalshiClient, st: State, m: dict, side: str, entry: float):
    if sizing.should_halt(st.equity, st.start_equity):
        log(f"HALTED equity ${st.equity:.2f} <= "
            f"${st.start_equity * sizing.HALT_EQUITY_FRAC:.2f}")
        return
    unit = sizing.contracts_for_equity(st.equity, entry)
    if unit <= 0:
        return
    if len(st.open_positions) >= sizing.max_concurrent(st.equity, entry):
        log(f"skip {m['ticker']}: at max concurrent")
        return
    cost = unit * entry
    if cost > st.cash:
        log(f"skip {m['ticker']}: need ${cost:.2f}, cash ${st.cash:.2f}")
        return

    ticker = m["ticker"]
    try:
        last_at = float(m["last_price_dollars"]) if m.get("last_price_dollars") is not None else None
    except (TypeError, ValueError):
        last_at = None
    pos = Position(
        ticker=ticker, series=m.get("event_ticker", ticker.split("-")[0]),
        side=side, contracts=unit, entry=entry, cost=cost,
        opened_ts=time.time(), close_ts=parse_ts(m["close_time"]),
        last_at_signal=last_at,
    )

    if st.mode == "live":
        book_side = "bid" if side == "yes" else "ask"
        book_price = entry if side == "yes" else round(1 - entry, 4)
        try:
            resp = client.create_order(ticker, book_side, unit, book_price, post_only=True)
            pos.order_id = resp.get("order_id", "")
            pos.client_order_id = resp.get("client_order_id", "")
            fill = float(resp.get("fill_count", "0") or 0)
            # post_only should not take liquidity; treat remaining as resting
            if fill > 0:
                # unexpected immediate fill (crossed) — still record
                pos.filled = True
                st.cash -= entry * fill
                pos.contracts = fill
                pos.cost = entry * fill
            log(f"LIVE order {book_side} {unit} @ {book_price} on {ticker} "
                f"order_id={pos.order_id} fill={fill}")
        except Exception as e:
            log(f"LIVE order failed {ticker}: {e}")
            return
    else:
        # paper: rest the order; fill checked on subsequent polls
        log(f"PAPER rest {side.upper()} {unit:.2f} @ {entry:.2f} on {ticker} "
            f"(mid signal, {int(pos.close_ts - time.time())}s to close)")

    st.positions.append(pos)
    st.signaled.append(ticker)
    st.save()
    append_trade_log({"event": "signal", "mode": st.mode, **asdict(pos)})


def update_paper_fills(st: State, mkt: dict):
    """Fill resting paper bids when the market subsequently trades through us.

    Requires a NEW last price (different from the signal snapshot) at or through
    our resting price, or the opposite side of the book crossing us. Avoids
    instantly filling on the same quote that triggered the signal.
    """
    ticker = mkt["ticker"]
    last = mkt.get("last_price_dollars")
    bid = mkt.get("yes_bid_dollars")
    ask = mkt.get("yes_ask_dollars")
    try:
        last_f = float(last) if last is not None else None
        bid_f = float(bid) if bid is not None else None
        ask_f = float(ask) if ask is not None else None
    except (TypeError, ValueError):
        return

    for p in st.open_positions:
        if p.ticker != ticker or p.filled:
            continue
        # give the order at least one poll cycle to rest
        if time.time() - p.opened_ts < POLL_SEC:
            continue
        filled = False
        new_trade = last_f is not None and last_f != p.last_at_signal
        if p.side == "yes":
            if (new_trade and last_f <= p.entry) or (ask_f is not None and ask_f <= p.entry):
                filled = True
        else:
            yes_px = round(1 - p.entry, 4)
            if (new_trade and last_f >= yes_px) or (bid_f is not None and bid_f >= yes_px):
                filled = True
        if filled:
            p.filled = True
            st.cash -= p.cost
            log(f"PAPER FILL {p.side.upper()} {p.contracts:.2f} @ {p.entry:.2f} "
                f"on {p.ticker}  cash=${st.cash:.2f}")
            append_trade_log({"event": "fill", **asdict(p)})
            st.save()


def settle_due(client: KalshiClient, st: State):
    now = time.time()
    for p in list(st.open_positions):
        if now < p.close_ts + 15:  # wait ~15s past close for finalization
            continue
        try:
            m = client.market(p.ticker)
        except Exception as e:
            log(f"settle fetch failed {p.ticker}: {e}")
            continue
        status = m.get("status")
        result = m.get("result")
        if status not in ("finalized", "determined", "settled") and result not in ("yes", "no"):
            # cancel unfilled resting orders past close
            if not p.filled and now > p.close_ts + 30:
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
        st.cash += payout
        p.settled = True
        p.result = int(won)
        p.pnl = pnl
        st.closed.append(asdict(p))
        log(f"SETTLE {p.ticker} {p.side.upper()} {'WIN' if won else 'LOSS'} "
            f"pnl={pnl:+.4f}  cash=${st.cash:.2f} equity=${st.equity:.2f}")
        append_trade_log({"event": "settle", "won": won, "pnl": pnl,
                          "cash": st.cash, "equity": st.equity, **asdict(p)})
        st.save()


def summary(st: State) -> str:
    closed = [c for c in st.closed if c.get("filled")]
    n = len(closed)
    if n == 0:
        return (f"equity=${st.equity:.2f} cash=${st.cash:.2f} "
                f"open={len(st.open_positions)} closed=0  unit="
                f"{sizing.contracts_for_equity(st.equity):.2f}")
    wins = sum(1 for c in closed if c.get("result") == 1)
    pnl = sum(c.get("pnl") or 0 for c in closed)
    return (f"equity=${st.equity:.2f} cash=${st.cash:.2f} "
            f"open={len(st.open_positions)} closed={n} "
            f"win%={100*wins/n:.0f} pnl={pnl:+.4f}  "
            f"unit={sizing.contracts_for_equity(st.equity):.2f}")


def handle_stop(signum, frame):
    global RUNNING
    RUNNING = False
    log("shutting down...")


def main():
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    demo = os.environ.get("KALSHI_DEMO", "").lower() in ("1", "true", "yes")
    client = KalshiClient(demo=demo)
    if MODE == "live" and not client.can_trade:
        log("MODE=live but no API keys set. Export KALSHI_API_KEY_ID and "
            "KALSHI_PRIVATE_KEY or KALSHI_PRIVATE_KEY_PATH. Aborting.")
        sys.exit(1)

    st = State.load_or_new(START_EQUITY, MODE)
    log(f"starting MODE={st.mode}  {sizing.describe(st.start_equity)}")
    log(f"series={SERIES}  window={WINDOW_SEC}s  price=[{PRICE_LO},{PRICE_HI})")
    if st.mode == "live":
        try:
            bal = client.balance()
            log(f"live balance: {bal}")
        except Exception as e:
            log(f"warning: could not fetch balance: {e}")

    last_summary = 0.0
    while RUNNING:
        try:
            settle_due(client, st)
            now = time.time()
            for series in SERIES:
                try:
                    markets = client.open_markets(series)
                except Exception as e:
                    log(f"open_markets {series}: {e}")
                    continue
                for m in markets:
                    ticker = m["ticker"]
                    close_ts = parse_ts(m["close_time"])
                    secs_left = close_ts - now

                    # refresh for fills / more accurate quotes
                    try:
                        m = client.market(ticker)
                    except Exception:
                        pass

                    update_paper_fills(st, m)

                    if ticker in st.signaled:
                        continue
                    if not (0 < secs_left <= WINDOW_SEC):
                        continue
                    mid = mid_of(m)
                    if mid is None:
                        continue
                    sig = signal_side(mid)
                    if sig is None:
                        continue
                    side, entry = sig
                    log(f"signal {ticker} mid={mid:.3f} -> {side} @{entry:.2f} "
                        f"({secs_left:.0f}s left)")
                    try_open(client, st, m, side, entry)

            if now - last_summary > 60:
                log(summary(st))
                last_summary = now
        except Exception as e:
            log(f"loop error: {e}")
        time.sleep(POLL_SEC)

    st.save()
    log(f"stopped. {summary(st)}")


if __name__ == "__main__":
    main()
