"""Fetch minute-level candlestick history for Kalshi 15-minute crypto markets.

Writes one JSON-lines file per series to data/<series>.jsonl. Each line is one
settled market with its settlement result and per-minute price/bid/ask closes,
aligned by absolute minute timestamp so markets can be joined across assets.

Usage: python3 research/fetch_data.py [n_markets_per_series]
"""
import json
import math
import sys
import time
import datetime
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = [
    "KXBTC15M", "KXETH15M", "KXSOL15M", "KXXRP15M", "KXDOGE15M",
    "KXZEC15M", "KXNEAR15M", "KXHYPE15M", "KXBNB15M",
]
N_MARKETS = int(sys.argv[1]) if len(sys.argv) > 1 else 480  # ~5 days of 15m intervals
OUT_DIR = Path(__file__).resolve().parent.parent / "data"


def get(url: str, tries: int = 5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 * (i + 1))
                continue
            raise
        except Exception:
            time.sleep(0.8 * (i + 1))
    raise RuntimeError(f"failed after {tries} tries: {url}")


def ts(iso: str) -> int:
    return int(datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def fetch_markets(series: str, n: int):
    out, cursor = [], ""
    while len(out) < n:
        url = f"{BASE}/markets?series_ticker={series}&status=settled&limit=100"
        if cursor:
            url += f"&cursor={cursor}"
        d = get(url)
        out.extend(d["markets"])
        cursor = d.get("cursor")
        if not cursor or not d["markets"]:
            break
    return out[:n]


def fetch_candles(series: str, m: dict):
    url = (
        f"{BASE}/series/{series}/markets/{m['ticker']}/candlesticks"
        f"?start_ts={ts(m['open_time'])}&end_ts={ts(m['close_time'])}&period_interval=1"
    )
    d = get(url)
    minutes = []
    for c in d["candlesticks"]:
        p = c.get("price", {})
        bid = c.get("yes_bid", {}).get("close_dollars")
        ask = c.get("yes_ask", {}).get("close_dollars")
        close = p.get("close_dollars")
        if close is None:
            if bid is None or ask is None:
                continue
            close = (float(bid) + float(ask)) / 2
        minutes.append({
            "t": c["end_period_ts"],
            "close": float(close),
            "high": float(p.get("high_dollars", close)),
            "low": float(p.get("low_dollars", close)),
            "bid": float(bid) if bid is not None else None,
            "ask": float(ask) if ask is not None else None,
            "vol": float(c.get("volume_fp", 0)),
        })
    return minutes


def run_series(series: str):
    rows = []
    for m in fetch_markets(series, N_MARKETS):
        if m.get("result") not in ("yes", "no"):
            continue
        try:
            minutes = fetch_candles(series, m)
        except Exception:
            continue
        if len(minutes) < 5:
            continue
        rows.append({
            "ticker": m["ticker"],
            "open_ts": ts(m["open_time"]),
            "close_ts": ts(m["close_time"]),
            "result": 1 if m["result"] == "yes" else 0,
            "volume": float(m.get("volume_fp", 0)),
            "minutes": minutes,
        })
        time.sleep(0.04)
    return series, rows


def main():
    OUT_DIR.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(run_series, s): s for s in SERIES}
        for f in as_completed(futs):
            series, rows = f.result()
            path = OUT_DIR / f"{series}.jsonl"
            with open(path, "w") as fh:
                for r in rows:
                    fh.write(json.dumps(r) + "\n")
            print(f"{series}: wrote {len(rows)} markets -> {path}", flush=True)


if __name__ == "__main__":
    main()
