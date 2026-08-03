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
# Exit if our side's mark falls this fraction below entry (0.20 = 20%)
STOP_LOSS_PCT = float(os.environ.get("STOP_LOSS_PCT", "0.20"))
# Signal window: last N seconds before close
WINDOW_SEC = int(os.environ.get("WINDOW_SEC", "180"))
STATE_PATH = Path(os.environ.get(
    "STATE_PATH",
    "bot/state_live.json" if MODE == "live" else "bot/state.json",
))
LOG_PATH = Path(os.environ.get(
    "LOG_PATH",
    "bot/trades_live.jsonl" if MODE == "live" else "bot/trades.jsonl",
))

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
    exit_reason: str = ""  # "" | "settle" | "stop"
    exit_price: float | None = None
    exit_order_id: str = ""


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
            resp = client.create_order(
                ticker, book_side, unit, book_price, post_only=True,
                expiration_ts=int(pos.close_ts),
            )
            pos.order_id = resp.get("order_id", "")
            pos.client_order_id = resp.get("client_order_id", "")
            fill = float(resp.get("fill_count", "0") or 0)
            if fill > 0:
                pos.filled = True
                pos.contracts = fill
                pos.cost = entry * fill
                st.cash -= pos.cost
            log(f"LIVE order {book_side} {unit:.2f} @ {book_price:.4f} on {ticker} "
                f"order_id={pos.order_id} fill={fill}")
        except Exception as e:
            log(f"LIVE order failed {ticker}: {e}")
            return
    else:
        log(f"PAPER rest {side.upper()} {unit:.2f} @ {entry:.2f} on {ticker} "
            f"(mid signal, {int(pos.close_ts - time.time())}s to close)")

    st.positions.append(pos)
    st.signaled.append(ticker)
    st.save()
    append_trade_log({"event": "signal", "mode": st.mode, **asdict(pos)})


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
            sync_live_cash(client, st)
            log(f"LIVE FILL {p.side.upper()} {fill:.2f} @ ~{p.entry:.2f} on {p.ticker} "
                f"status={status} cash=${st.cash:.2f}")
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


def close_position_stop(client: KalshiClient, st: State, p: Position, m: dict, mark: float):
    """Flatten a filled position after stop-loss. Live: IOC reduce-only. Paper: mark fill."""
    if p.settled or not p.filled:
        return
    exit_px = mark
    if st.mode == "live":
        try:
            if p.side == "yes":
                # dump YES into the bid
                resp = client.create_order(
                    p.ticker, "ask", p.contracts, 0.01,
                    post_only=False, time_in_force="immediate_or_cancel",
                    reduce_only=True,
                )
            else:
                # cover NO by buying YES through the ask
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
                # average_fill_price is YES price; convert to our side
                exit_px = avg_f if p.side == "yes" else (1.0 - avg_f)
            if fill <= 0:
                log(f"STOP IOC no fill {p.ticker} — will retry next poll")
                return
            p.contracts = fill
        except Exception as e:
            log(f"STOP exit failed {p.ticker}: {e}")
            return
        sync_live_cash(client, st)
    else:
        st.cash += exit_px * p.contracts

    pnl = exit_px * p.contracts - p.cost
    if st.mode == "live":
        sync_live_cash(client, st)

    p.exit_price = exit_px
    p.exit_reason = "stop"
    p.pnl = pnl
    p.result = 1 if pnl > 0 else 0
    p.settled = True
    st.closed.append(asdict(p))
    log(f"STOP {p.ticker} {p.side.upper()} entry={p.entry:.2f} mark={mark:.2f} "
        f"(-{100*STOP_LOSS_PCT:.0f}%) exit~{exit_px:.2f} pnl={pnl:+.4f} "
        f"cash=${st.cash:.2f}")
    append_trade_log({"event": "stop", "mark": mark, "exit_price": exit_px,
                      "pnl": pnl, "cash": st.cash, **asdict(p)})
    st.save()


def check_stops(client: KalshiClient, st: State, markets_by_ticker: dict):
    for p in list(st.open_positions):
        if not p.filled or p.settled:
            continue
        m = markets_by_ticker.get(p.ticker)
        if not m:
            try:
                m = client.market(p.ticker)
            except Exception:
                continue
        mark = side_mark(m, p.side)
        if mark is None:
            continue
        if stop_triggered(p.entry, mark):
            log(f"stop trigger {p.ticker} {p.side} entry={p.entry:.2f} mark={mark:.2f} "
                f"threshold={p.entry * (1 - STOP_LOSS_PCT):.2f}")
            close_position_stop(client, st, p, m, mark)


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
    if st.mode == "live":
        eq = sync_live_cash(client, st)
        if not st.closed and not st.positions:
            st.start_equity = st.cash
            st.save()
        log(f"live balance cash=${st.cash:.4f} (equity~${eq:.4f})")
    log(f"starting MODE={st.mode}  {sizing.describe(st.cash if st.mode == 'live' else st.start_equity)}")
    log(f"series={SERIES}  window={WINDOW_SEC}s  price=[{PRICE_LO},{PRICE_HI})  "
        f"stop_loss={100*STOP_LOSS_PCT:.0f}% under entry")

    last_summary = 0.0
    while RUNNING:
        try:
            if st.mode == "live":
                update_live_fills(client, st)
            settle_due(client, st)
            now = time.time()
            markets_by_ticker: dict[str, dict] = {}
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

                    try:
                        m = client.market(ticker)
                    except Exception:
                        pass
                    markets_by_ticker[ticker] = m

                    if st.mode == "paper":
                        update_paper_fills(st, m)

                    if ticker in st.signaled:
                        continue
                    if not (0 < secs_left <= WINDOW_SEC):
                        continue
                    mid = mid_of(m)
                    if mid is None:
                        continue
                    sig = signal_side(m, mid)
                    if sig is None:
                        continue
                    side, entry = sig
                    log(f"signal {ticker} mid={mid:.3f} -> {side} @{entry:.2f} "
                        f"({secs_left:.0f}s left)")
                    try_open(client, st, m, side, entry)

            check_stops(client, st, markets_by_ticker)

            if now - last_summary > 60:
                if st.mode == "live":
                    sync_live_cash(client, st)
                log(summary(st))
                last_summary = now
        except Exception as e:
            log(f"loop error: {e}")
        time.sleep(POLL_SEC)

    st.save()
    log(f"stopped. {summary(st)}")


if __name__ == "__main__":
    main()
