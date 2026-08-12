"""Daily P&L consistency analysis for the near-expiry favorite maker strategy.

Strategy: when either side's contract closes at 0.90-0.97 in minutes 11-13,
buy that side at the minute close (maker fill proxy, no fee), hold to
settlement. One trade per market. Reported in EV-per-contract units; dollar
P&L scales linearly with contracts per trade.

Variants: all 9 assets vs excluding BTC+DOGE (where the 5-day sample was
negative). Also reports the systematic buy-NO-at-mid fade for comparison.

Usage: python3 research/daily_pnl.py  (requires data/ from fetch_data.py)
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


def favorite_trades(markets, exclude=()):
    trades = []
    for m in markets:
        if m["series"] in exclude:
            continue
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
            trades.append((day(m), ev))
            break
    return trades


def no_fade_trades(markets):
    trades = []
    for m in markets:
        c = m["by_min"].get(5)
        if c:
            trades.append((day(m), (1 - m["result"]) - (1 - c["close"])))
    return trades


def daily_report(name, trades):
    by_day = defaultdict(list)
    for d, ev in trades:
        by_day[d].append(ev)
    days = sorted(by_day)
    totals = [sum(by_day[d]) for d in days]
    n_days = len(days)
    pos = sum(1 for t in totals if t > 0)
    mean = sum(totals) / n_days
    std = math.sqrt(sum((t - mean) ** 2 for t in totals) / max(n_days - 1, 1))
    # max drawdown of the cumulative curve, in EV-per-contract units
    cum = peak = mdd = 0.0
    for t in totals:
        cum += t
        peak = max(peak, cum)
        mdd = max(mdd, peak - cum)
    half = n_days // 2
    first, second = sum(totals[:half]), sum(totals[half:])
    n_tr = len(trades)
    ev = sum(e for _, e in trades) / n_tr
    print(f"\n### {name}")
    print(f"  trades={n_tr}  EV/contract={ev:+.4f}  trades/day={n_tr/n_days:.0f}")
    print(f"  days={n_days}  positive days={pos} ({100*pos/n_days:.0f}%)")
    print(f"  daily total (per 1 contract/trade): mean={mean:+.2f}  std={std:.2f}  "
          f"sharpe(daily)={mean/std if std else 0:.2f}")
    print(f"  worst day={min(totals):+.2f}  best day={max(totals):+.2f}  max drawdown={mdd:.2f}")
    print(f"  first half total={first:+.2f}  second half total={second:+.2f}")
    print("  daily series: " + " ".join(f"{d}:{t:+.1f}" for d, t in zip(days, totals)))


def main():
    markets = load()
    n_days = len({day(m) for m in markets})
    print(f"loaded {len(markets)} markets over {n_days} days "
          f"({min(day(m) for m in markets)} .. {max(day(m) for m in markets)})")

    daily_report("favorite 0.90-0.97 maker, all 9 assets",
                 favorite_trades(markets))
    daily_report("favorite 0.90-0.97 maker, ex BTC+DOGE",
                 favorite_trades(markets, exclude=("KXBTC15M", "KXDOGE15M")))
    daily_report("buy NO at mid, minute 5 (bullish-bias fade)",
                 no_fade_trades(markets))

    print("\n### per-asset EV over full sample (favorite maker)")
    per = defaultdict(list)
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
            per[m["series"]].append(ev)
            break
    for s, evs in sorted(per.items()):
        n = len(evs)
        mean = sum(evs) / n
        se = math.sqrt(sum((e - mean) ** 2 for e in evs) / (n - 1) / n)
        print(f"  {s:12} n={n:>5}  EV={mean:+.4f} (se {se:.4f})")


if __name__ == "__main__":
    main()
