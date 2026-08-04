"""Paper observer: early Binance direction pulls vs Kalshi 50-65c books.

Question under test: at the START of a 15m window (first EARLY_SECS seconds),
when Binance shows a real directional pull while the Kalshi book is still
coin-flippy (fav <= FAV_MAX), does buying the lead side pay?

Zero live orders — records would-be entries + settle results to JSONL:

  bot/early_tip_obs.jsonl   one row per hypothetical trade
  bot/observer.log          heartbeat + running scoreboard

Run:  python3 -u bot/early_tip_observer.py  (own tmux session)
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bot.kalshi_client import KalshiClient
from bot.binance_lead import BinanceLeadFeed, symbol_for

SERIES = [s.strip() for s in os.environ.get(
    "OBS_SERIES",
    "KXBTC15M,KXETH15M,KXXRP15M,KXBNB15M,KXDOGE15M,KXSOL15M,KXNEAR15M",
).split(",") if s.strip()]

EARLY_SECS = float(os.environ.get("OBS_EARLY_SECS", "180"))     # first 3m of window
FAV_MAX = float(os.environ.get("OBS_FAV_MAX", "0.68"))          # book still coin-flippy
LEAN_PCT = float(os.environ.get("OBS_LEAN_PCT", "0.0004"))      # min |15s ret| to record
STRONG_PCT = float(os.environ.get("OBS_STRONG_PCT", "0.0008"))  # strong tier
POLL_SEC = float(os.environ.get("OBS_POLL_SEC", "5"))
OBS_PATH = Path(os.environ.get("OBS_PATH", "bot/early_tip_obs.jsonl"))

WINDOW_LEN = 900.0


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


def kalshi_fee(price: float, contracts: float = 1.0) -> float:
    """Kalshi taker fee ≈ 0.07 * P * (1-P) per contract."""
    return 0.07 * price * (1.0 - price) * contracts


def main() -> None:
    client = KalshiClient()
    feed = BinanceLeadFeed(
        symbols=sorted({s for t in SERIES if (s := symbol_for(t))})
    )
    feed.start()
    log(f"observer up series={SERIES} early≤{EARLY_SECS:.0f}s fav≤{FAV_MAX} "
        f"lean≥{100*LEAN_PCT:.3f}% strong≥{100*STRONG_PCT:.3f}%")

    taken: dict[str, dict] = {}      # ticker -> live observation (until settle)
    done: set[str] = set()
    score = {"n": 0, "wins": 0, "pnl_mid": 0.0, "pnl_ask": 0.0}
    per_sym: dict[str, list[int]] = {}
    last_beat = 0.0

    while True:
        now = time.time()
        try:
            for series in SERIES:
                try:
                    markets = client.open_markets(series)
                except Exception:
                    continue
                for m in markets:
                    ticker = m.get("ticker") or ""
                    if not ticker or ticker in taken or ticker in done:
                        continue
                    close_ts = parse_ts(m["close_time"])
                    secs_left = close_ts - now
                    into = WINDOW_LEN - secs_left
                    if into < 0 or into > EARLY_SECS:
                        continue
                    mid = mid_of(m)
                    if mid is None:
                        continue
                    fav = max(mid, 1 - mid)
                    if fav > FAV_MAX:
                        continue
                    sig = feed.signal(ticker)  # 15s window lean
                    if sig is None or sig.direction == "flat" or sig.price <= 0:
                        continue
                    if abs(sig.ret_pct) < LEAN_PCT:
                        continue
                    side = "yes" if sig.direction == "up" else "no"
                    # would-be entry prices
                    try:
                        ybid = float(m.get("yes_bid_dollars") or 0)
                        yask = float(m.get("yes_ask_dollars") or 0)
                    except (TypeError, ValueError):
                        ybid = yask = 0
                    if side == "yes":
                        px_mid, px_ask = mid, (yask if 0 < yask < 1 else mid)
                    else:
                        px_mid, px_ask = 1 - mid, (1 - ybid if 0 < ybid < 1 else 1 - mid)
                    votes = feed.venue_votes(ticker)
                    agree = sum(1 for _v, d, _r in votes if d == sig.direction)
                    tier = "strong" if abs(sig.ret_pct) >= STRONG_PCT else "weak"
                    taken[ticker] = {
                        "ticker": ticker, "series": series, "side": side,
                        "ts": now, "secs_into": round(into, 1),
                        "fav_at_signal": round(fav, 3),
                        "px_mid": round(px_mid, 3), "px_ask": round(px_ask, 3),
                        "lead_ret": sig.ret_pct, "lead_tier": tier,
                        "flow_imb": sig.flow_imb,
                        "mv_agree": agree, "mv_n": len(votes),
                        "peak_fav_side": round(px_mid, 3),
                        "close_ts": close_ts,
                    }
                    log(f"WOULD-BUY {ticker} {side.upper()} @~{px_ask:.2f} "
                        f"(mid {px_mid:.2f}) lead={sig.direction}{100*sig.ret_pct:+.3f}% "
                        f"[{tier}] mv={agree}/{len(votes)} into={into:.0f}s")

            # track peaks + settle
            for ticker, o in list(taken.items()):
                if now < o["close_ts"]:
                    try:
                        m = client.market(ticker)
                    except Exception:
                        continue
                    mid = mid_of(m)
                    if mid is not None:
                        side_px = mid if o["side"] == "yes" else 1 - mid
                        o["peak_fav_side"] = max(o["peak_fav_side"], round(side_px, 3))
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
                        done.add(ticker); taken.pop(ticker, None)
                    continue
                won = 1 if result == o["side"] else 0
                pnl_mid = (1 - o["px_mid"]) if won else -o["px_mid"]
                fee = kalshi_fee(o["px_ask"])
                pnl_ask = ((1 - o["px_ask"]) if won else -o["px_ask"]) - fee
                o.update({"result": result, "won": won,
                          "pnl_mid": round(pnl_mid, 4),
                          "pnl_ask_fee": round(pnl_ask, 4)})
                with OBS_PATH.open("a") as f:
                    f.write(json.dumps(o) + "\n")
                score["n"] += 1
                score["wins"] += won
                score["pnl_mid"] += pnl_mid
                score["pnl_ask"] += pnl_ask
                sym = symbol_for(ticker) or "?"
                per_sym.setdefault(sym, [0, 0])
                per_sym[sym][0] += won
                per_sym[sym][1] += 1
                log(f"SETTLE {ticker} {o['side'].upper()} {'WIN' if won else 'LOSS'} "
                    f"pnl_mid={pnl_mid:+.2f}/ct peak={o['peak_fav_side']:.2f} "
                    f"[{o['lead_tier']}]")
                done.add(ticker)
                taken.pop(ticker, None)

            if now - last_beat > 600 and score["n"]:
                wr = 100 * score["wins"] / score["n"]
                by = " ".join(f"{s}:{w}/{n}" for s, (w, n) in sorted(per_sym.items()))
                log(f"SCORE n={score['n']} WR={wr:.0f}% "
                    f"pnl_mid/ct={score['pnl_mid']/score['n']:+.3f} "
                    f"pnl_ask+fee/ct={score['pnl_ask']/score['n']:+.3f}  {by}")
                last_beat = now
        except Exception as e:
            log(f"loop error: {e}")
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
