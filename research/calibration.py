"""Calibration study: does a Kalshi 15m crypto contract priced at X cents
actually settle yes X% of the time? Broken down by minutes remaining.

A persistent gap between market price and realized settle rate, larger than
fees + half-spread, is tradable edge.

Usage: python3 research/calibration.py
"""
import json
import math
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def taker_fee(p: float) -> float:
    """Kalshi taker fee per contract, rounded up to the cent."""
    return math.ceil(7 * p * (1 - p)) / 100


def load_all():
    rows = []
    for f in sorted(DATA_DIR.glob("*.jsonl")):
        series = f.stem
        for line in open(f):
            m = json.loads(line)
            m["series"] = series
            rows.append(m)
    return rows


def main():
    markets = load_all()
    print(f"loaded {len(markets)} markets from {len(set(m['series'] for m in markets))} series\n")

    # observation = (minute index, close, ask, result)
    # minute index i means the candle ending i+1 minutes after open; ~14-i minutes remain
    time_buckets = [(0, 4, "12-15 min left"), (5, 9, "6-10 min left"), (10, 13, "1-5 min left")]
    price_buckets = [(0.02, 0.10), (0.10, 0.20), (0.20, 0.35), (0.35, 0.50),
                     (0.50, 0.65), (0.65, 0.80), (0.80, 0.90), (0.90, 0.98)]

    stats = defaultdict(lambda: {"n": 0, "price": 0.0, "ask": 0.0, "win": 0})
    for m in markets:
        base = m["open_ts"]
        for c in m["minutes"]:
            idx = (c["t"] - base) // 60 - 1
            for lo_i, hi_i, tlabel in time_buckets:
                if lo_i <= idx <= hi_i:
                    break
            else:
                continue
            p = c["close"]
            for lo, hi in price_buckets:
                if lo <= p < hi:
                    key = (tlabel, lo, hi)
                    s = stats[key]
                    s["n"] += 1
                    s["price"] += p
                    s["ask"] += c["ask"] if c["ask"] is not None else p
                    s["win"] += m["result"]
                    break

    print(f"{'time':>14} {'price bucket':>13} {'n':>7} {'avg price':>10} {'settle%':>9} "
          f"{'gap':>7} {'EV@ask-fee':>11}")
    for lo_i, hi_i, tlabel in time_buckets:
        for lo, hi in price_buckets:
            s = stats.get((tlabel, lo, hi))
            if not s or s["n"] < 200:
                continue
            n = s["n"]
            avg_p = s["price"] / n
            avg_ask = s["ask"] / n
            rate = s["win"] / n
            gap = rate - avg_p
            ev = rate - avg_ask - taker_fee(avg_ask)
            # binomial standard error for the settle rate
            se = math.sqrt(rate * (1 - rate) / n)
            flag = " *" if abs(gap) > 2 * se and abs(gap) > 0.01 else ""
            print(f"{tlabel:>14} {f'{lo:.2f}-{hi:.2f}':>13} {n:>7} {avg_p:>10.3f} "
                  f"{100*rate:>8.1f}% {gap:>+7.3f} {ev:>+11.4f}{flag}")
        print()


if __name__ == "__main__":
    main()
