"""Day-by-day and per-asset consistency check for the two candidate edges:

  A) near-expiry favorite as maker: when either side trades 0.90-0.97 in
     minutes 11-13, buy that side at the last close (mid proxy), hold to settle
  B) systematic bullish-bias fade: buy NO at mid at minute 5 of every interval

Usage: python3 research/consistency.py  (requires data/ from fetch_data.py)
"""
import json
import math
import datetime
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load():
    markets = []
    for f in sorted(DATA_DIR.glob("*.jsonl")):
        for line in open(f):
            m = json.loads(line)
            m["series"] = f.stem
            m["by_min"] = {(c["t"] - m["open_ts"]) // 60 - 1: c for c in m["minutes"]}
            markets.append(m)
    return markets


def day(m):
    return datetime.datetime.fromtimestamp(m["open_ts"], datetime.timezone.utc).strftime("%m-%d")


def summarize(label, groups):
    for key, evs in sorted(groups.items()):
        print(f"  {key}: n={len(evs):>4}  EV={sum(evs)/len(evs):+.4f}  total={sum(evs):+.2f}")
    print()


def main():
    markets = load()

    print("=== A) favorite 0.90-0.97 maker, minutes 11-13 ===")
    by_day, by_asset, all_evs = defaultdict(list), defaultdict(list), []
    for m in markets:
        for idx in (11, 12, 13):
            c = m["by_min"].get(idx)
            if not c:
                continue
            p = c["close"]
            if 0.90 <= p < 0.97:
                ev = m["result"] - p
            elif 0.90 <= 1 - p <= 0.97:
                ev = (1 - m["result"]) - (1 - p)
            else:
                continue
            by_day[day(m)].append(ev)
            by_asset[m["series"]].append(ev)
            all_evs.append(ev)
            break
    n = len(all_evs)
    mean = sum(all_evs) / n
    se = math.sqrt(sum((e - mean) ** 2 for e in all_evs) / (n - 1) / n)
    print(f"  overall n={n}  EV={mean:+.4f} (se {se:.4f})\n")
    summarize("day", by_day)
    summarize("asset", by_asset)

    print("=== B) always buy NO at mid, minute 5, maker ===")
    by_day2, all2 = defaultdict(list), []
    for m in markets:
        c = m["by_min"].get(5)
        if not c:
            continue
        ev = (1 - m["result"]) - (1 - c["close"])
        all2.append(ev)
        by_day2[day(m)].append(ev)
    n = len(all2)
    mean = sum(all2) / n
    se = math.sqrt(sum((e - mean) ** 2 for e in all2) / (n - 1) / n)
    print(f"  overall n={n}  EV={mean:+.4f} (se {se:.4f})")
    print("  NOTE: same-window trades across assets are correlated (shared crypto")
    print("  beta), so the true standard error is larger than shown.\n")
    summarize("day", by_day2)


if __name__ == "__main__":
    main()
