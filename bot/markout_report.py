#!/usr/bin/env python3
"""Markout / edge attribution report from bot trade logs.

Usage:
  python3 bot/markout_report.py
  python3 bot/markout_report.py bot/trades_live.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "bot/trades_live.jsonl")
    rows = load_rows(path)
    print(f"file={path}  rows={len(rows)}")
    print("events:", dict(Counter(r.get("event") for r in rows)))

    settles = [r for r in rows if r.get("event") == "settle" and r.get("filled")]
    fills = [r for r in rows if r.get("event") == "fill"]
    signals = [r for r in rows if r.get("event") == "signal"]
    blocks = [r for r in rows if r.get("event") == "binance_block"]
    cancels = [r for r in rows if r.get("event") == "binance_cancel"]
    intel = [r for r in rows if r.get("event") == "binance_intel"]
    skips = [r for r in rows if r.get("event") == "skip_mispricing"]

    print(f"\n=== fills / settles ===")
    print(f"signals={len(signals)} fills={len(fills)} settles={len(settles)}")
    if settles:
        wins = [r for r in settles if r.get("won") or r.get("pnl", 0) > 0]
        losses = [r for r in settles if not (r.get("won") or r.get("pnl", 0) > 0)]
        pnl = sum(float(r.get("pnl") or 0) for r in settles)
        wr = len(wins) / len(settles)
        avg_win = (sum(float(r["pnl"]) for r in wins) / len(wins)) if wins else 0
        avg_loss = (sum(float(r["pnl"]) for r in losses) / len(losses)) if losses else 0
        print(f"W/L={len(wins)}/{len(losses)} wr={100*wr:.1f}% pnl=${pnl:+.4f}")
        print(f"avg_win=${avg_win:+.4f} avg_loss=${avg_loss:+.4f}")
        mos = [float(r["markout_per_contract"]) for r in settles
               if r.get("markout_per_contract") is not None]
        if mos:
            print(f"avg markout/contract={sum(mos)/len(mos):+.4f}")

    print(f"\n=== edge sizing snapshot (from signals) ===")
    risked = [r for r in signals if r.get("risk_frac") is not None]
    if risked:
        print(f"n={len(risked)} mean_risk={100*sum(r['risk_frac'] for r in risked)/len(risked):.1f}% "
              f"min={100*min(r['risk_frac'] for r in risked):.1f}% "
              f"max={100*max(r['risk_frac'] for r in risked):.1f}%")
        print("reasons:", dict(Counter(r.get("edge_reason") or "?" for r in risked)))

    print(f"\n=== binance lead attribution ===")
    print(f"intel={len(intel)} blocks={len(blocks)} cancels={len(cancels)} "
          f"mispricing_skips={len(skips)}")

    # Settles with binance_dir at entry
    by_bn: dict[str, list[float]] = defaultdict(list)
    for r in settles:
        key = r.get("binance_dir") or "n/a"
        if r.get("pnl") is not None:
            by_bn[key].append(float(r["pnl"]))
    if by_bn:
        print("settle pnl by binance_dir at entry:")
        for k, vals in sorted(by_bn.items()):
            print(f"  {k:8s} n={len(vals):3d} sum=${sum(vals):+.3f} "
                  f"avg=${sum(vals)/len(vals):+.4f}")

    # Agree vs disagree: if binance_dir matches side
    agree = []
    disagree = []
    flat = []
    for r in settles:
        d = r.get("binance_dir") or "flat"
        side = r.get("side")
        want = "up" if side == "yes" else "down"
        pnl = float(r.get("pnl") or 0)
        if d == "flat" or d == "":
            flat.append(pnl)
        elif d == want:
            agree.append(pnl)
        else:
            disagree.append(pnl)
    for name, vals in (("agree", agree), ("disagree", disagree), ("flat/n/a", flat)):
        if vals:
            print(f"  {name:10s} n={len(vals)} sum=${sum(vals):+.3f} "
                  f"avg=${sum(vals)/len(vals):+.4f}")

    print(f"\n=== by series ===")
    by_s: dict[str, list[float]] = defaultdict(list)
    for r in settles:
        root = (r.get("ticker") or "?").split("-")[0]
        by_s[root].append(float(r.get("pnl") or 0))
    for s, vals in sorted(by_s.items()):
        w = sum(1 for v in vals if v > 0)
        print(f"  {s}: n={len(vals)} W={w} pnl=${sum(vals):+.4f}")

    # Fill rate
    print(f"\n=== execution ===")
    sig_tickers = {r.get("ticker") for r in signals}
    fill_tickers = {r.get("ticker") for r in fills}
    if sig_tickers:
        print(f"signal→fill rate≈{100*len(fill_tickers & sig_tickers)/len(sig_tickers):.0f}% "
              f"({len(fill_tickers & sig_tickers)}/{len(sig_tickers)})")


if __name__ == "__main__":
    main()
