import json, time, datetime, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = ["KXBTC15M","KXETH15M","KXSOL15M","KXXRP15M","KXDOGE15M","KXADA15M",
          "KXBCH15M","KXZEC15M","KXNEAR15M","KXTON15M","KXHYPE15M","KXBNB15M"]
N_MARKETS = 96  # ~24 hours of 15m intervals

def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 * (i + 1)); continue
            raise
        except Exception:
            time.sleep(0.8 * (i + 1))
    raise RuntimeError("failed: " + url)

def fetch_markets(series):
    out, cursor = [], ""
    while len(out) < N_MARKETS:
        url = f"{BASE}/markets?series_ticker={series}&status=settled&limit=100"
        if cursor: url += f"&cursor={cursor}"
        d = get(url)
        # keep only binary up/down style markets (one per event)
        out.extend(d["markets"])
        cursor = d.get("cursor")
        if not cursor or not d["markets"]: break
    return out[:N_MARKETS]

def ts(s):
    return int(datetime.datetime.fromisoformat(s.replace("Z","+00:00")).timestamp())

def analyze_market(series, m):
    start, end = ts(m["open_time"]), ts(m["close_time"])
    url = (f"{BASE}/series/{series}/markets/{m['ticker']}/candlesticks"
           f"?start_ts={start}&end_ts={end}&period_interval=1")
    d = get(url)
    candles = d["candlesticks"]
    closes, highs, lows, spreads, vols = [], [], [], [], []
    for c in candles:
        p = c.get("price", {})
        bid, ask = c.get("yes_bid", {}), c.get("yes_ask", {})
        cl = p.get("close_dollars")
        if cl is None:
            b, a = bid.get("close_dollars"), ask.get("close_dollars")
            if b is None or a is None: continue
            cl = (float(b) + float(a)) / 2
        else:
            cl = float(cl)
        hi = float(p.get("high_dollars", cl)); lo = float(p.get("low_dollars", cl))
        closes.append(cl); highs.append(hi); lows.append(lo)
        vols.append(float(c.get("volume_fp", 0)))
        b, a = bid.get("close_dollars"), ask.get("close_dollars")
        if b is not None and a is not None and 0 < float(b) < 1 and 0 < float(a) < 1:
            spreads.append(float(a) - float(b))
    if len(closes) < 5:
        return None
    # 1) 50c crossings on minute closes (with 65/35 debounce bands to skip noise)
    flips, state = 0, None
    for cl in closes:
        s = "H" if cl >= 0.65 else ("L" if cl <= 0.35 else None)
        if s and state and s != state: flips += 1
        if s: state = s
    # 2) full round-trip: touched >=0.80 then later <=0.20, or vice versa (minute hi/lo)
    big = 0
    seen_hi = seen_lo = False
    for hi, lo in zip(highs, lows):
        if seen_hi and lo <= 0.20: big = 1; break
        if seen_lo and hi >= 0.80: big = 1; break
        if hi >= 0.80: seen_hi = True
        if lo <= 0.20: seen_lo = True
    # 3) path length (sum of abs minute-close moves) = raw swing opportunity
    path = sum(abs(closes[i] - closes[i-1]) for i in range(1, len(closes)))
    return dict(flips=flips, big=big, path=path,
                vol=sum(vols), spread=(sum(spreads)/len(spreads) if spreads else None))

def run_series(series):
    try:
        mkts = fetch_markets(series)
    except Exception as e:
        return series, None, str(e)
    res = []
    for m in mkts:
        try:
            r = analyze_market(series, m)
            if r: res.append(r)
        except Exception:
            pass
        time.sleep(0.05)
    return series, res, None

results = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(run_series, s): s for s in SERIES}
    for f in as_completed(futs):
        series, res, err = f.result()
        results[series] = res
        n = len(res) if res else 0
        print(f"done {series}: {n} markets analyzed" + (f" (err {err})" if err else ""), flush=True)

print()
hdr = f"{'series':14}{'n':>4}{'flips/ivl':>11}{'%>=1 flip':>11}{'%80->20':>9}{'path/ivl':>10}{'vol/ivl $':>12}{'avg sprd':>10}"
print(hdr); print("-" * len(hdr))
rows = []
for s, res in results.items():
    if not res: continue
    n = len(res)
    flips = sum(r["flips"] for r in res) / n
    anyflip = 100 * sum(1 for r in res if r["flips"] >= 1) / n
    big = 100 * sum(r["big"] for r in res) / n
    path = sum(r["path"] for r in res) / n
    vol = sum(r["vol"] for r in res) / n
    sp = [r["spread"] for r in res if r["spread"] is not None]
    sp = sum(sp)/len(sp) if sp else float("nan")
    rows.append((flips, f"{s:14}{n:>4}{flips:>11.2f}{anyflip:>10.0f}%{big:>8.0f}%{path:>10.2f}{vol:>12,.0f}{sp:>10.3f}"))
for _, line in sorted(rows, reverse=True):
    print(line)
json.dump({k: v for k, v in results.items() if v}, open("/tmp/kalshi_results.json","w"))
