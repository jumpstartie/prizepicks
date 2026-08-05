"""Strategy backtests on Kalshi 15m crypto minute data.

Tests, with realistic execution assumptions:
  1. Sample drift check (base settle rates per asset)
  2. Cross-asset lead-lag: trade an asset whose contract lags the consensus
     of the other 8 (all intervals share the same 15-minute clock)
  3. Momentum: follow a fast contract move
  4. Near-expiry favorite: buy the leading side in the last minutes

Execution models:
  taker: buy yes at ask / buy no at (1 - bid), pay Kalshi fee ceil(7*p*(1-p))/100
  maker: fill at last close (mid proxy), no fee. Optimistic: assumes your
         resting order gets filled without adverse selection.

One trade max per market per strategy (first qualifying minute).

Usage: python3 research/strategies.py
"""
import json
import math
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def taker_fee(p: float) -> float:
    return math.ceil(7 * p * (1 - p)) / 100


def load():
    markets = []
    for f in sorted(DATA_DIR.glob("*.jsonl")):
        for line in open(f):
            m = json.loads(line)
            m["series"] = f.stem
            by_min = {}
            for c in m["minutes"]:
                idx = (c["t"] - m["open_ts"]) // 60 - 1
                by_min[idx] = c
            m["by_min"] = by_min
            markets.append(m)
    return markets


def report(name, trades):
    if not trades:
        print(f"{name:44} no trades")
        return
    n = len(trades)
    evs = [t["ev"] for t in trades]
    mean = sum(evs) / n
    var = sum((e - mean) ** 2 for e in evs) / max(n - 1, 1)
    se = math.sqrt(var / n)
    wins = sum(1 for t in trades if t["win"])
    print(f"{name:44} n={n:>5}  EV/contract={mean:+.4f} (se {se:.4f})  "
          f"win%={100*wins/n:5.1f}  avg entry={sum(t['p'] for t in trades)/n:.3f}")


def make_trade(side, entry, result, maker):
    win = result if side == "yes" else 1 - result
    fee = 0.0 if maker else taker_fee(entry)
    return {"p": entry, "win": win, "ev": win - entry - fee}


def main():
    markets = load()
    by_open = defaultdict(dict)
    for m in markets:
        by_open[m["open_ts"]][m["series"]] = m

    print("=== 1. sample drift check: settle rate of UP per asset ===")
    per = defaultdict(lambda: [0, 0])
    for m in markets:
        per[m["series"]][0] += m["result"]
        per[m["series"]][1] += 1
    for s, (w, n) in sorted(per.items()):
        print(f"  {s:12} up settled {100*w/n:5.1f}%  (n={n})")
    tot_w = sum(w for w, _ in per.values()); tot_n = sum(n for _, n in per.values())
    print(f"  {'ALL':12} up settled {100*tot_w/tot_n:5.1f}%")

    print("\n=== 2. cross-asset lead-lag (consensus of other assets vs this one) ===")
    for thresh in (0.15, 0.25):
        for maker in (False, True):
            trades = []
            for open_ts, group in by_open.items():
                if len(group) < 5:
                    continue
                for series, m in group.items():
                    done = False
                    for idx in range(3, 12):
                        if done:
                            break
                        c = m["by_min"].get(idx)
                        if not c:
                            continue
                        others = [g["by_min"][idx]["close"] for s2, g in group.items()
                                  if s2 != series and idx in g["by_min"]]
                        if len(others) < 4:
                            continue
                        consensus = sum(others) / len(others)
                        signal = consensus - c["close"]
                        if signal > thresh and c["ask"] is not None:
                            entry = c["close"] if maker else c["ask"]
                            if 0.02 < entry < 0.95:
                                trades.append(make_trade("yes", entry, m["result"], maker))
                                done = True
                        elif signal < -thresh and c["bid"] is not None:
                            entry = (1 - c["close"]) if maker else (1 - c["bid"])
                            if 0.02 < entry < 0.95:
                                trades.append(make_trade("no", entry, m["result"], maker))
                                done = True
            report(f"lead-lag |signal|>{thresh} {'maker' if maker else 'taker'}", trades)

    print("\n=== 3. momentum: contract moved >= delta over last 3 minutes ===")
    for delta in (0.25, 0.35):
        for maker in (False, True):
            trades = []
            for m in markets:
                done = False
                for idx in range(4, 12):
                    if done:
                        break
                    c, c3 = m["by_min"].get(idx), m["by_min"].get(idx - 3)
                    if not c or not c3:
                        continue
                    move = c["close"] - c3["close"]
                    if move > delta and c["ask"] is not None:
                        entry = c["close"] if maker else c["ask"]
                        if 0.05 < entry < 0.93:
                            trades.append(make_trade("yes", entry, m["result"], maker))
                            done = True
                    elif move < -delta and c["bid"] is not None:
                        entry = (1 - c["close"]) if maker else (1 - c["bid"])
                        if 0.05 < entry < 0.93:
                            trades.append(make_trade("no", entry, m["result"], maker))
                            done = True
            report(f"momentum 3-min move>{delta} {'maker' if maker else 'taker'}", trades)

    print("\n=== 4. near-expiry favorite: buy leading side, minutes 11-13 ===")
    for lo, hi in ((0.80, 0.90), (0.90, 0.97)):
        for maker in (False, True):
            trades = []
            for m in markets:
                done = False
                for idx in (11, 12, 13):
                    if done:
                        break
                    c = m["by_min"].get(idx)
                    if not c:
                        continue
                    p = c["close"]
                    if lo <= p < hi and c["ask"] is not None:
                        entry = p if maker else c["ask"]
                        trades.append(make_trade("yes", entry, m["result"], maker))
                        done = True
                    elif lo <= (1 - p) <= hi and c["bid"] is not None:
                        entry = (1 - p) if maker else (1 - c["bid"])
                        trades.append(make_trade("no", entry, m["result"], maker))
                        done = True
            report(f"favorite {lo:.2f}-{hi:.2f} last-3-min {'maker' if maker else 'taker'}", trades)


if __name__ == "__main__":
    main()
