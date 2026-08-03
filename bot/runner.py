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

# Books with positive 31-day favorite-maker EV. BTC/DOGE omitted (flat/negative).
SERIES = os.environ.get(
    "SERIES", "KXBNB15M,KXSOL15M,KXXRP15M,KXZEC15M,KXHYPE15M"
).split(",")
START_EQUITY = float(os.environ.get("START_EQUITY", "20"))
MODE = os.environ.get("MODE", "paper").lower()  # paper | live
POLL_SEC = float(os.environ.get("POLL_SEC", "5"))
PRICE_LO = float(os.environ.get("PRICE_LO", "0.90"))
PRICE_HI = float(os.environ.get("PRICE_HI", "0.97"))
# Exit if our side's mark falls this fraction below entry (0.20 = 20%)
STOP_LOSS_PCT = float(os.environ.get("STOP_LOSS_PCT", "0.20"))
# Do not stop-loss in the final N seconds — hold to settlement (favorites wick).
STOP_DISABLE_SECS = int(os.environ.get("STOP_DISABLE_SECS", "60"))
# Signal window: last N seconds before close
WINDOW_SEC = int(os.environ.get("WINDOW_SEC", "180"))
# Require at least this much time left to enter (blocks last-second flip chases)
MIN_SECS_LEFT = int(os.environ.get("MIN_SECS_LEFT", "60"))
# Require the favorite band on the same side for this many consecutive polls
CONFIRM_POLLS = int(os.environ.get("CONFIRM_POLLS", "2"))
# Requotes after a post-only-cross rejection
MAX_REQUOTES = int(os.environ.get("MAX_REQUOTES", "3"))
# Per-trade take-profit: exit when mark >= entry * mult (binaries cap at $1,
# so this only fires when entry <= 1/mult, e.g. entry <= 33¢ for 3x).
TAKE_PROFIT_MULT = float(os.environ.get("TAKE_PROFIT_MULT", "3.0"))
TAKE_PROFIT_CAP = float(os.environ.get("TAKE_PROFIT_CAP", "0.99"))
# Absolute bankroll floor — stop the run if equity hits this (overnight loss cap)
HALT_FLOOR = float(os.environ.get("HALT_FLOOR", "15.0"))
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
    exit_reason: str = ""  # "" | "settle" | "stop" | "take_profit"
    exit_price: float | None = None
    exit_order_id: str = ""
    tp_price: float | None = None  # entry * TAKE_PROFIT_MULT, if reachable (<= cap)


@dataclass
class State:
    start_equity: float
    cash: float
    mode: str
    positions: list[Position] = field(default_factory=list)
    closed: list[dict] = field(default_factory=list)
    signaled: list[str] = field(default_factory=list)  # tickers already acted on
    halted: bool = False  # True once loss floor / drawdown halt trips

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
            "saved_at": time.time(),
        }
        STATE_PATH.write_text(json.dumps(payload, indent=2))

    @classmethod
    def load_or_new(cls, start: float, mode: str) -> "State":
        if STATE_PATH.exists():
            d = json.loads(STATE_PATH.read_text())
            st = cls(start_equity=d["start_equity"], cash=d["cash"], mode=d["mode"],
                     signaled=d.get("signaled", []), closed=d.get("closed", []),
                     halted=bool(d.get("halted", False)))
            fields = set(Position.__dataclass_fields__)
            st.positions = [
                Position(**{k: v for k, v in p.items() if k in fields})
                for p in d.get("positions", [])
            ]
            log(f"resumed state equity=${st.equity:.2f} cash=${st.cash:.2f} "
                f"open={len(st.open_positions)} closed={len(st.closed)} "
                f"halted={st.halted}")
            return st
        st = cls(start_equity=start, cash=start, mode=mode)
        st.save()
        return st


def tp_price_for_entry(entry: float) -> float | None:
    """Return take-profit mark if 3x entry is attainable on a $0–$1 binary."""
    raw = entry * TAKE_PROFIT_MULT
    if raw > TAKE_PROFIT_CAP:
        return None  # unreachable (typical for 90c+ favorites)
    return round(raw, 4)


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


def enforce_halt(client: KalshiClient, st: State) -> bool:
    """If equity hit the floor, cancel resting orders and freeze new entries."""
    if st.halted:
        return True
    if not sizing.should_halt(st.equity, st.start_equity, floor=HALT_FLOOR):
        return False
    st.halted = True
    log(f"HALT RUN equity=${st.equity:.2f} <= floor ${HALT_FLOOR:.2f} "
        f"(start was ${st.start_equity:.2f}) — no new trades")
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
    append_trade_log({"event": "halt", "equity": st.equity, "floor": HALT_FLOOR,
                      "start_equity": st.start_equity, "cash": st.cash})
    return True


def try_open(client: KalshiClient, st: State, m: dict, side: str, entry: float):
    if st.halted or sizing.should_halt(st.equity, st.start_equity, floor=HALT_FLOOR):
        enforce_halt(client, st)
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
    close_ts = parse_ts(m["close_time"])
    tp = tp_price_for_entry(entry)
    pos = Position(
        ticker=ticker, series=m.get("event_ticker", ticker.split("-")[0]),
        side=side, contracts=unit, entry=entry, cost=cost,
        opened_ts=time.time(), close_ts=close_ts,
        last_at_signal=last_at, tp_price=tp,
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
            st.cash -= pos.cost
        tp_note = f"tp={tp:.2f}" if tp is not None else f"tp=n/a (need entry≤{TAKE_PROFIT_CAP/TAKE_PROFIT_MULT:.2f} for {TAKE_PROFIT_MULT:.0f}x)"
        log(f"LIVE order {book_side} {unit:.2f} @ {book_price:.4f} on {ticker} "
            f"order_id={pos.order_id} fill={fill}  {tp_note}")
    else:
        tp_note = f"tp={tp:.2f}" if tp is not None else "tp=n/a"
        log(f"PAPER rest {side.upper()} {unit:.2f} @ {entry:.2f} on {ticker} "
            f"(mid signal, {int(close_ts - time.time())}s to close)  {tp_note}")

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


def close_position_exit(client: KalshiClient, st: State, p: Position, mark: float,
                        reason: str):
    """Flatten a filled position (stop or take-profit). Live: IOC reduce-only."""
    if p.settled or not p.filled:
        return
    exit_px = mark
    label = "STOP" if reason == "stop" else "TAKE PROFIT"
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
    log(f"{label} {p.ticker} {p.side.upper()} entry={p.entry:.2f} mark={mark:.2f} "
        f"exit~{exit_px:.2f} pnl={pnl:+.4f} cash=${st.cash:.2f}")
    append_trade_log({"event": reason, "mark": mark, "exit_price": exit_px,
                      "pnl": pnl, "cash": st.cash, **asdict(p)})
    st.save()


def check_exits(client: KalshiClient, st: State, markets_by_ticker: dict):
    """Stop-loss and per-trade take-profit (3x entry when attainable)."""
    now = time.time()
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

        # Take-profit first: 3x entry (only if tp_price was attainable at entry)
        tp = p.tp_price if p.tp_price is not None else tp_price_for_entry(p.entry)
        if tp is not None and mark >= tp:
            log(f"tp trigger {p.ticker} {p.side} entry={p.entry:.2f} mark={mark:.2f} "
                f"target={tp:.2f} ({TAKE_PROFIT_MULT:.0f}x)")
            close_position_exit(client, st, p, mark, "take_profit")
            continue

        # Stop-loss: disabled in final STOP_DISABLE_SECS
        if secs_left <= STOP_DISABLE_SECS:
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
    bank = st.cash if st.mode == "live" else st.start_equity
    log(f"starting MODE={st.mode}  {sizing.describe(bank, floor=HALT_FLOOR)}")
    log(f"series={SERIES}  window={WINDOW_SEC}s  min_left={MIN_SECS_LEFT}s  "
        f"confirm={CONFIRM_POLLS}  price=[{PRICE_LO},{PRICE_HI})  "
        f"stop_loss={100*STOP_LOSS_PCT:.0f}% (off last {STOP_DISABLE_SECS}s)  "
        f"take_profit={TAKE_PROFIT_MULT:.0f}x entry (cap {TAKE_PROFIT_CAP:.2f})  "
        f"halt_floor=${HALT_FLOOR:.2f}")
    if st.halted:
        log(f"already HALTED from prior run — settling only, no new trades")

    pending: dict[str, dict] = {}  # ticker -> {side, hits, entry}
    last_summary = 0.0
    while RUNNING:
        try:
            if st.mode == "live":
                update_live_fills(client, st)
                sync_live_cash(client, st)
            enforce_halt(client, st)
            settle_due(client, st)
            now = time.time()
            markets_by_ticker: dict[str, dict] = {}
            seen_tickers: set[str] = set()
            for series in SERIES:
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
                    sig = signal_side(m, mid)
                    if sig is None:
                        pending.pop(ticker, None)
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
                last_summary = now
        except Exception as e:
            log(f"loop error: {e}")
        time.sleep(POLL_SEC)

    st.save()
    log(f"stopped. {summary(st)}")


if __name__ == "__main__":
    main()
