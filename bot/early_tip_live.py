"""Early-tip LIVE module — the speed play.

Buys the Binance-lead side in the first minutes of a 15m window while the
Kalshi book is still cheap (fav <= FAV_MAX), instead of waiting for 70c+
like the favorite-maker. Taker entry: speed over queue position.

SAFETY / ARMING
  - Starts DISARMED. Arms itself only when the paper observer record
    (bot/early_tip_obs.jsonl) plus its own settled fills reach
    ARM_WINS wins with <= ARM_MAX_LOSSES losses (default 5-0).
    Set EARLY_FORCE_ARM=1 to skip the paper W/L gate (see start_early_live.sh).
  - Auto-disarms for the day after DAY_STOP_LOSS dollars of losses or
    3 losses in the last 10 settles (still applies under force-arm).
  - Small fixed stakes (STAKE_FRAC of balance, capped STAKE_CAP dollars),
    MAX_OPEN concurrent, one shot per ticker.

Runs standalone in its own tmux; never touches the favorite-maker state.
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bot.kalshi_client import KalshiClient
from bot.binance_lead import BinanceLeadFeed, symbol_for

SERIES = [s.strip() for s in os.environ.get(
    "EARLY_SERIES",
    "KXBTC15M,KXETH15M,KXXRP15M,KXBNB15M,KXDOGE15M,KXSOL15M,KXNEAR15M",
).split(",") if s.strip()]

EARLY_SECS = float(os.environ.get("EARLY_SECS", "180"))
FAV_MAX = float(os.environ.get("EARLY_FAV_MAX", "0.68"))
STRONG_PCT = float(os.environ.get("EARLY_STRONG_PCT", "0.0008"))
MV_MIN_AGREE = int(os.environ.get("EARLY_MV_MIN_AGREE", "2"))
ENTRY_MAX = float(os.environ.get("EARLY_ENTRY_MAX", "0.72"))   # never chase past this
STAKE_FRAC = float(os.environ.get("EARLY_STAKE_FRAC", "0.08"))
STAKE_CAP = float(os.environ.get("EARLY_STAKE_CAP", "12"))
MAX_OPEN = int(os.environ.get("EARLY_MAX_OPEN", "2"))
POLL_SEC = float(os.environ.get("EARLY_POLL_SEC", "2"))
ARM_WINS = int(os.environ.get("EARLY_ARM_WINS", "5"))
ARM_MAX_LOSSES = int(os.environ.get("EARLY_ARM_MAX_LOSSES", "0"))
FORCE_ARM = os.environ.get("EARLY_FORCE_ARM", "0").strip() in ("1", "true", "yes")
DAY_STOP_LOSS = float(os.environ.get("EARLY_DAY_STOP_LOSS", "15"))
DISARM_LOSSES_IN_10 = int(os.environ.get("EARLY_DISARM_LOSSES_IN_10", "3"))

OBS_PATH = Path("bot/early_tip_obs.jsonl")
TRADES_PATH = Path("bot/early_tip_trades.jsonl")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def mid_of(m: dict) -> float | None:
    bid, ask = m.get("yes_bid_dollars"), m.get("yes_ask_dollars")
    last = m.get("last_price_dollars")
    try:
        if bid is not None and ask is not None:
            b, a = float(bid), float(ask)
            if 0 < b < 1 and 0 < a < 1:
                return (b + a) / 2
        if last is not None:
            return float(last)
    except (TypeError, ValueError):
        pass
    return None


def parse_ts(iso: str) -> float:
    import datetime
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def record_rows() -> list[dict]:
    rows = []
    for path in (OBS_PATH, TRADES_PATH):
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("won") is not None:
                rows.append(o)
    rows.sort(key=lambda o: float(o.get("close_ts") or 0))
    return rows


def armed_status() -> tuple[bool, str]:
    rows = record_rows()
    wins = sum(1 for o in rows if o.get("won"))
    losses = sum(1 for o in rows if o.get("won") == 0)
    if not FORCE_ARM and (wins < ARM_WINS or losses > ARM_MAX_LOSSES):
        return False, f"disarmed {wins}-{losses} (need {ARM_WINS}-{ARM_MAX_LOSSES})"
    # daily loss stop on our own live fills only (paper losses don't count)
    today = time.strftime("%Y-%m-%d")
    day_pnl = 0.0
    live_rows = []
    if TRADES_PATH.exists():
        for line in TRADES_PATH.read_text().splitlines():
            try:
                o = json.loads(line)
            except Exception:
                continue
            live_rows.append(o)
            if o.get("day") == today and o.get("pnl") is not None:
                day_pnl += float(o["pnl"])
    if day_pnl <= -DAY_STOP_LOSS:
        return False, f"disarmed: day stop {day_pnl:+.2f}"
    # Streak disarm: paper+live when gated; LIVE-only under force-arm so a
    # single paper miss can't kill the module after we intentionally go live.
    if FORCE_ARM:
        streak = [o for o in live_rows if o.get("won") is not None][-10:]
        tag = "FORCE"
    else:
        streak = rows[-10:]
        tag = "armed"
    if sum(1 for o in streak if o.get("won") == 0) >= DISARM_LOSSES_IN_10:
        return False, f"disarmed: {DISARM_LOSSES_IN_10}+ losses in last 10"
    return True, f"{tag} {wins}-{losses} day_pnl={day_pnl:+.2f}"


def main() -> None:
    client = KalshiClient()
    feed = BinanceLeadFeed(
        symbols=sorted({s for t in SERIES if (s := symbol_for(t))})
    )
    feed.start()
    arm_desc = "FORCE" if FORCE_ARM else f"{ARM_WINS}-{ARM_MAX_LOSSES}"
    log(f"early-tip live up series={SERIES} strong≥{100*STRONG_PCT:.3f}% "
        f"mv≥{MV_MIN_AGREE} fav≤{FAV_MAX} entry≤{ENTRY_MAX} "
        f"stake={STAKE_FRAC:.0%}/${STAKE_CAP:.0f} arm={arm_desc}")

    open_pos: dict[str, dict] = {}
    done: set[str] = set()
    last_arm_log = ""
    arm_cache = (0.0, False, "")

    while True:
        now = time.time()
        try:
            # cached arming check (records change rarely)
            if now - arm_cache[0] > 20:
                ok, why = armed_status()
                arm_cache = (now, ok, why)
                if why != last_arm_log:
                    log(f"ARM: {why}")
                    last_arm_log = why
            armed = arm_cache[1]

            for series in SERIES:
                if not armed or len(open_pos) >= MAX_OPEN:
                    break
                try:
                    markets = client.open_markets(series)
                except Exception:
                    continue
                for m in markets:
                    ticker = m.get("ticker") or ""
                    if not ticker or ticker in open_pos or ticker in done:
                        continue
                    close_ts = parse_ts(m["close_time"])
                    into = 900.0 - (close_ts - now)
                    if into < 5 or into > EARLY_SECS:
                        continue
                    mid = mid_of(m)
                    if mid is None or max(mid, 1 - mid) > FAV_MAX:
                        continue
                    sig = feed.signal(ticker)
                    if (sig is None or sig.direction == "flat"
                            or abs(sig.ret_pct) < STRONG_PCT):
                        continue
                    votes = feed.venue_votes(ticker)
                    agree = sum(1 for _v, d, _r in votes if d == sig.direction)
                    if agree < MV_MIN_AGREE:
                        continue
                    # taker-flow must not oppose
                    if sig.flow_qty > 0 and (
                        (sig.direction == "up" and sig.flow_imb < -0.3)
                        or (sig.direction == "down" and sig.flow_imb > 0.3)
                    ):
                        continue
                    side = "yes" if sig.direction == "up" else "no"
                    try:
                        ybid = float(m.get("yes_bid_dollars") or 0)
                        yask = float(m.get("yes_ask_dollars") or 0)
                    except (TypeError, ValueError):
                        continue
                    if side == "yes":
                        px = yask if 0 < yask < 1 else None
                        book_side = "bid"
                    else:
                        px = (1 - ybid) if 0 < ybid < 1 else None
                        book_side = "ask"
                    if px is None or px > ENTRY_MAX:
                        continue
                    try:
                        bal = client.balance()
                        cash = float(bal.get("balance_dollars")
                                     or (bal.get("balance", 0) / 100))
                    except Exception:
                        continue
                    stake = min(STAKE_CAP, STAKE_FRAC * cash)
                    count = max(1.0, round(stake / px, 2))
                    book_price = px if side == "yes" else round(1.0 - px, 4)
                    try:
                        resp = client.create_order(
                            ticker, book_side, count, book_price,
                            post_only=False,
                            expiration_ts=int(close_ts),
                            client_order_id=str(uuid.uuid4()),
                        )
                    except Exception as e:
                        log(f"order failed {ticker}: {e}")
                        done.add(ticker)
                        continue
                    fill = float(resp.get("fill_count", "0") or 0)
                    open_pos[ticker] = {
                        "ticker": ticker, "series": series, "side": side,
                        "ts": now, "day": time.strftime("%Y-%m-%d"),
                        "entry": px, "count": count, "filled": fill,
                        "order_id": resp.get("order_id", ""),
                        "lead_ret": sig.ret_pct, "mv_agree": agree,
                        "mv_n": len(votes), "secs_into": round(into, 1),
                        "close_ts": close_ts, "source": "live",
                    }
                    log(f"EARLY BUY {ticker} {side.upper()} {count:.2f}@{px:.2f} "
                        f"fill={fill} lead={sig.direction}{100*sig.ret_pct:+.3f}% "
                        f"mv={agree}/{len(votes)} into={into:.0f}s")

            # manage fills / settles
            for ticker, o in list(open_pos.items()):
                if o["filled"] <= 0 and now < o["close_ts"]:
                    # check fill; cancel if unfilled after 25s (market ran)
                    try:
                        od = client.get_order(o["order_id"])
                        o["filled"] = float(od.get("fill_count", "0") or 0)
                    except Exception:
                        pass
                    if o["filled"] <= 0 and now - o["ts"] > 25:
                        try:
                            client.cancel_order(o["order_id"], market_ticker=ticker)
                            log(f"cancel unfilled {ticker}")
                        except Exception:
                            pass
                        done.add(ticker)
                        open_pos.pop(ticker, None)
                    continue
                if now < o["close_ts"] + 25:
                    continue
                try:
                    m = client.market(ticker)
                except Exception:
                    continue
                result = (m.get("result") or "").lower()
                if result not in ("yes", "no"):
                    if now > o["close_ts"] + 300:
                        done.add(ticker); open_pos.pop(ticker, None)
                    continue
                won = 1 if result == o["side"] else 0
                filled = o["filled"] if o["filled"] > 0 else 0
                pnl = filled * ((1 - o["entry"]) if won else -o["entry"])
                o.update({"result": result, "won": won, "pnl": round(pnl, 4)})
                with TRADES_PATH.open("a") as f:
                    f.write(json.dumps(o) + "\n")
                log(f"EARLY SETTLE {ticker} {o['side'].upper()} "
                    f"{'WIN' if won else 'LOSS'} pnl={pnl:+.2f}")
                done.add(ticker)
                open_pos.pop(ticker, None)
        except Exception as e:
            log(f"loop error: {e}")
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
