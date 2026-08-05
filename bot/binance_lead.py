"""Fast lead feed for Kalshi 15m crypto up/down markets.

Primary: Binance trade WebSocket (data-stream.binance.vision)
Confirm: Coinbase spot REST (same-direction check)
Fallback: Binance REST poller

Extras:
  - Taker-flow imbalance from WS aggressor flags (filters fake ret leans)
  - BTC/ETH risk veto on soft alt entries when majors dump/pump hard

Kalshi YES ~= underlying UP; Kalshi NO ~= underlying DOWN.
Threshold is vol-adjusted so quiet tapes don't spam false leans.

Hist ticks: (ts, px, qty, taker_sign) with taker_sign +1 buy / -1 sell / 0 unknown.
"""
from __future__ import annotations

import json
import math
import os
import threading
import time
import urllib.request
from collections import deque
from dataclasses import dataclass
from typing import Deque

Tick = tuple[float, float, float, int]  # ts, px, qty, taker_sign


DEFAULT_BASES = (
    os.environ.get("BINANCE_API_BASE", "https://data-api.binance.vision"),
    "https://api.binance.us",
    "https://api.binance.com",
)
WS_URL = os.environ.get(
    "BINANCE_WS_URL", "wss://data-stream.binance.vision/stream"
)

SERIES_SYMBOLS = {
    "KXXRP15M": "XRPUSDT",
    "KXBNB15M": "BNBUSDT",
    "KXSOL15M": "SOLUSDT",
    "KXBTC15M": "BTCUSDT",
    "KXETH15M": "ETHUSDT",
    "KXDOGE15M": "DOGEUSDT",
    "KXNEAR15M": "NEARUSDT",
    "KXZEC15M": "ZECUSDT",
    # Kalshi metals 15m — Pyth-settled; no Binance spot XAU/XAG
    "KXGOLD15M": "XAUUSD",
    "KXSILVER15M": "XAGUSD",
}
COINBASE_PRODUCT = {
    "XRPUSDT": "XRP-USD",
    "BNBUSDT": "BNB-USD",
    "SOLUSDT": "SOL-USD",
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "DOGEUSDT": "DOGE-USD",
    "NEARUSDT": "NEAR-USD",
    "ZECUSDT": "ZEC-USD",
    "XAUUSD": "XAU-USD",
    "XAGUSD": "XAG-USD",
}
OKX_INST = {
    "XRPUSDT": "XRP-USDT",
    "BNBUSDT": "BNB-USDT",
    "SOLUSDT": "SOL-USDT",
    "BTCUSDT": "BTC-USDT",
    "ETHUSDT": "ETH-USDT",
    "DOGEUSDT": "DOGE-USDT",
    "NEARUSDT": "NEAR-USDT",
    "ZECUSDT": "ZEC-USDT",
}
# Kraken public ticker pair codes
KRAKEN_PAIR = {
    "BTCUSDT": "XBTUSD",
    "ETHUSDT": "ETHUSD",
    "SOLUSDT": "SOLUSD",
    "BNBUSDT": "BNBUSD",
    "XRPUSDT": "XRPUSD",
    "DOGEUSDT": "DOGEUSD",
    "NEARUSDT": "NEARUSD",
}
# Pyth Hermes price-feed ids — crypto + Metal.XAU/XAG (Kalshi metals settle)
PYTH_IDS = {
    "BTCUSDT": "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43",
    "ETHUSDT": "ff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace",
    "SOLUSDT": "ef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d",
    "BNBUSDT": "2f95862b045670cd22bee3114c39763a4a08beeb663b145d283c31d7d1101c4f",
    "XRPUSDT": "ec5d399846a9209f3fe5881d70aae9268c94339ff9817e8d18ff19fa05eea1c8",
    "DOGEUSDT": "dcef50dd0a4cd2dcc17e45df1676dcb336a11a61c69df7a0299b0150c672d25c",
    "NEARUSDT": "c415de8d2eba7db216527dff4b60e8f3a5311c740dadb233e13e12547e226750",
    # Metal.XAU/USD / Metal.XAG/USD — resolved live 2026-08-04
    "XAUUSD": "765d2ba906dbc32ca17cc11f5310a89e9ee1f6420508c63861f2f8ba4ee34bb2",
    "XAGUSD": "f2fb02c32b055c805e7238d628e5e9dadef274376114eb1f012337cabe93871e",
}
# No Binance spot book — Hermes is the primary lean hist for these symbols.
PYTH_PRIMARY_SYMBOLS = frozenset(
    s.strip().upper()
    for s in os.environ.get("PYTH_PRIMARY_SYMBOLS", "XAUUSD,XAGUSD").split(",")
    if s.strip()
)
PYTH_HERMES = os.environ.get("PYTH_HERMES", "https://hermes.pyth.network")
# Always keep majors subscribed for cross-asset risk veto.
RISK_VETO_SYMBOLS = tuple(
    s.strip().upper()
    for s in os.environ.get("RISK_VETO_SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
    if s.strip()
)


@dataclass
class LeadSignal:
    symbol: str
    direction: str          # "up" | "down" | "flat"
    ret_pct: float
    price: float
    window_sec: float
    ts: float
    source: str
    vol: float = 0.0
    threshold: float = 0.0
    confirmed: bool | None = None  # Coinbase same-way confirm
    flow_imb: float = 0.0          # taker buy-sell imbalance in [-1, 1]
    flow_qty: float = 0.0          # base-asset qty in flow window


def series_root(ticker_or_series: str) -> str:
    parts = ticker_or_series.split("-")
    return parts[0] if parts else ticker_or_series


def symbol_for(ticker_or_series: str) -> str | None:
    return SERIES_SYMBOLS.get(series_root(ticker_or_series))


def is_binance_symbol(symbol: str) -> bool:
    """True if symbol has a Binance spot trade stream (crypto USDT pairs)."""
    return bool(symbol) and symbol not in PYTH_PRIMARY_SYMBOLS and symbol.endswith("USDT")


class BinanceLeadFeed:
    """Binance trade stream + vol-adjusted lean + optional Coinbase confirm."""

    def __init__(
        self,
        symbols: list[str] | None = None,
        window_sec: float | None = None,
        threshold_pct: float | None = None,
        poll_sec: float | None = None,
        bases: tuple[str, ...] = DEFAULT_BASES,
    ):
        self.symbols = symbols or sorted(set(SERIES_SYMBOLS.values()))
        self.window_sec = float(
            window_sec if window_sec is not None
            else os.environ.get("BINANCE_LEAD_WINDOW_SEC", "15")
        )
        # Aggressive short window for soft-entry gates / fast veto.
        self.fast_window_sec = float(os.environ.get("BINANCE_FAST_WINDOW_SEC", "4"))
        self.base_threshold = float(
            threshold_pct if threshold_pct is not None
            else os.environ.get("BINANCE_LEAD_PCT", "0.0008")
        )
        self.fast_threshold = float(
            os.environ.get("BINANCE_FAST_PCT", "0.0004")
        )
        self.vol_mult = float(os.environ.get("BINANCE_LEAD_VOL_MULT", "1.25"))
        self.poll_sec = float(
            poll_sec if poll_sec is not None
            else os.environ.get("BINANCE_LEAD_POLL_SEC", "2")
        )
        self.confirm = os.environ.get("COINBASE_CONFIRM", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.use_ws = os.environ.get("BINANCE_WS", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.taker_flow = os.environ.get("TAKER_FLOW", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.flow_window_sec = float(
            os.environ.get("TAKER_FLOW_WINDOW_SEC", str(self.fast_window_sec))
        )
        # |imb| above this opposing a ret lean → flatten the lean
        self.flow_veto_imb = float(os.environ.get("TAKER_FLOW_VETO_IMB", "0.35"))
        self.flow_min_qty = float(os.environ.get("TAKER_FLOW_MIN_QTY", "0"))
        self.risk_veto_enabled = os.environ.get("RISK_VETO", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.risk_veto_pct = float(os.environ.get("RISK_VETO_PCT", "0.0012"))
        self.risk_veto_window = float(os.environ.get("RISK_VETO_WINDOW_SEC", "15"))
        # Multi-venue confirm: Binance + OKX + Kraken (+ Coinbase) votes
        self.multi_venue = os.environ.get("MULTI_VENUE", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.multi_venue_min = int(os.environ.get("MULTI_VENUE_MIN_AGREE", "2"))
        self.multi_venue_window = float(
            os.environ.get("MULTI_VENUE_WINDOW_SEC", str(self.fast_window_sec))
        )
        self.multi_venue_pct = float(os.environ.get("MULTI_VENUE_PCT", "0.0003"))
        # If BN leans but venues can't confirm → half-size (0) or block (1)
        self.multi_venue_strict = os.environ.get("MULTI_VENUE_STRICT", "0").lower() in (
            "1", "true", "yes", "on"
        )
        self.okx_enabled = os.environ.get("OKX_CONFIRM", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.kraken_enabled = os.environ.get("KRAKEN_CONFIRM", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.pyth_enabled = os.environ.get("PYTH_CONFIRM", "1").lower() in (
            "1", "true", "yes", "on"
        )
        self.bases = bases
        # Always subscribe majors used for risk veto
        for maj in RISK_VETO_SYMBOLS:
            if maj not in self.symbols:
                self.symbols.append(maj)
        self._hist: dict[str, Deque[Tick]] = {
            s: deque(maxlen=5000) for s in self.symbols
        }
        self._cb_hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._okx_hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._kraken_hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._pyth_hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._last: dict[str, LeadSignal] = {}
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []
        self._active_base: str | None = None
        self._last_error: str = ""
        self._ws_ok = False
        self._okx_ok = False
        self._kraken_ok = False
        self._pyth_ok = False

    # --- lifecycle ---------------------------------------------------------
    def start(self) -> None:
        if self._threads:
            return
        self._stop.clear()
        if self.use_ws:
            t = threading.Thread(target=self._ws_loop, name="binance-ws", daemon=True)
            t.start()
            self._threads.append(t)
        # REST sampler always runs as backup / bootstrap
        t2 = threading.Thread(target=self._rest_loop, name="binance-rest", daemon=True)
        t2.start()
        self._threads.append(t2)
        if self.confirm:
            t3 = threading.Thread(target=self._coinbase_loop, name="coinbase", daemon=True)
            t3.start()
            self._threads.append(t3)
        if self.multi_venue and self.okx_enabled:
            t4 = threading.Thread(target=self._okx_loop, name="okx", daemon=True)
            t4.start()
            self._threads.append(t4)
        if self.multi_venue and self.kraken_enabled:
            t5 = threading.Thread(target=self._kraken_loop, name="kraken", daemon=True)
            t5.start()
            self._threads.append(t5)
        # Hermes: crypto multi-venue voter + required primary lean for metals
        if self.pyth_enabled or any(s in PYTH_IDS for s in self.symbols):
            t6 = threading.Thread(target=self._pyth_loop, name="pyth", daemon=True)
            t6.start()
            self._threads.append(t6)

    def stop(self) -> None:
        self._stop.set()
        for t in self._threads:
            t.join(timeout=3)
        self._threads.clear()

    def ensure_symbols(self, symbols: list[str] | set[str]) -> list[str]:
        added: list[str] = []
        with self._lock:
            for sym in symbols:
                if not sym or sym in self._hist:
                    continue
                self.symbols.append(sym)
                self._hist[sym] = deque(maxlen=5000)
                self._cb_hist[sym] = deque(maxlen=600)
                self._okx_hist[sym] = deque(maxlen=600)
                self._kraken_hist[sym] = deque(maxlen=600)
                self._pyth_hist[sym] = deque(maxlen=600)
                added.append(sym)
        return added

    # --- feeds -------------------------------------------------------------
    def _push(self, symbol: str, ts: float, px: float, source: str,
              qty: float = 0.0, taker_sign: int = 0) -> None:
        with self._lock:
            if symbol not in self._hist:
                self._hist[symbol] = deque(maxlen=5000)
                if symbol not in self.symbols:
                    self.symbols.append(symbol)
            self._hist[symbol].append((ts, px, float(qty or 0.0), int(taker_sign)))
            self._active_base = source
            self._last[symbol] = self._compute_locked(symbol, ts)

    def _ws_loop(self) -> None:
        try:
            import websocket  # type: ignore
        except Exception as e:
            self._last_error = f"websocket import: {e}"
            return
        while not self._stop.is_set():
            bn_syms = [s for s in list(self.symbols) if is_binance_symbol(s)]
            if not bn_syms:
                self._stop.wait(5)
                continue
            streams = "/".join(f"{s.lower()}@trade" for s in bn_syms)
            url = f"{WS_URL}?streams={streams}"
            ws = None
            try:
                ws = websocket.create_connection(url, timeout=10)
                ws.settimeout(15)
                self._ws_ok = True
                self._last_error = ""
                while not self._stop.is_set():
                    raw = ws.recv()
                    if not raw:
                        break
                    msg = json.loads(raw)
                    data = msg.get("data") or msg
                    if data.get("e") != "trade":
                        continue
                    sym = data.get("s")
                    px = float(data["p"])
                    qty = float(data.get("q") or 0.0)
                    # m=True → buyer is maker → seller was aggressor (taker sell)
                    is_buyer_maker = bool(data.get("m"))
                    taker_sign = -1 if is_buyer_maker else 1
                    ts = float(data.get("T") or data.get("E") or time.time() * 1000) / 1000.0
                    if sym:
                        self._push(sym, ts, px, "binance-ws",
                                   qty=qty, taker_sign=taker_sign)
            except Exception as e:
                self._ws_ok = False
                self._last_error = f"ws: {e}"
                self._stop.wait(2)
            finally:
                try:
                    if ws is not None:
                        ws.close()
                except Exception:
                    pass

    def _fetch_binance_price(self, symbol: str) -> tuple[float, str]:
        last_err: Exception | None = None
        bases = list(self.bases)
        if self._active_base and self._active_base in bases:
            bases.remove(self._active_base)
            bases.insert(0, self._active_base)
        for base in bases:
            if not base.startswith("http"):
                continue
            url = f"{base.rstrip('/')}/api/v3/ticker/price?symbol={symbol}"
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "kalshi-lead-bot/1.0"}
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                return float(data["price"]), base
            except Exception as e:
                last_err = e
        raise RuntimeError(f"binance price failed for {symbol}: {last_err}")

    def _rest_loop(self) -> None:
        while not self._stop.is_set():
            # If WS is healthy, REST can be slower backup
            wait = self.poll_sec if not self._ws_ok else max(self.poll_sec, 5.0)
            for sym in list(self.symbols):
                if not is_binance_symbol(sym):
                    continue
                try:
                    px, src = self._fetch_binance_price(sym)
                    self._push(sym, time.time(), px, src)
                    self._last_error = ""
                except Exception as e:
                    if not self._ws_ok:
                        self._last_error = str(e)
            self._stop.wait(wait)

    def _coinbase_loop(self) -> None:
        while not self._stop.is_set():
            for sym in list(self.symbols):
                product = COINBASE_PRODUCT.get(sym)
                if not product:
                    continue
                url = f"https://api.coinbase.com/v2/prices/{product}/spot"
                try:
                    req = urllib.request.Request(
                        url, headers={"User-Agent": "kalshi-lead-bot/1.0"}
                    )
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                    px = float(data["data"]["amount"])
                    now = time.time()
                    with self._lock:
                        self._cb_hist[sym].append((now, px))
                        if sym in self._last:
                            # refresh confirm flag
                            self._last[sym] = self._compute_locked(sym, now)
                except Exception:
                    pass
            self._stop.wait(max(2.0, self.poll_sec))

    def _okx_loop(self) -> None:
        while not self._stop.is_set():
            for sym in list(self.symbols):
                inst = OKX_INST.get(sym)
                if not inst:
                    continue
                url = f"https://www.okx.com/api/v5/market/ticker?instId={inst}"
                try:
                    req = urllib.request.Request(
                        url, headers={"User-Agent": "kalshi-lead-bot/1.0"}
                    )
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                    rows = data.get("data") or []
                    if not rows:
                        continue
                    px = float(rows[0]["last"])
                    now = time.time()
                    with self._lock:
                        if sym not in self._okx_hist:
                            self._okx_hist[sym] = deque(maxlen=600)
                        self._okx_hist[sym].append((now, px))
                        self._okx_ok = True
                except Exception as e:
                    self._okx_ok = False
                    self._last_error = f"okx: {e}"
            self._stop.wait(max(2.0, self.poll_sec))

    def _kraken_loop(self) -> None:
        while not self._stop.is_set():
            for sym in list(self.symbols):
                pair = KRAKEN_PAIR.get(sym)
                if not pair:
                    continue
                url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
                try:
                    req = urllib.request.Request(
                        url, headers={"User-Agent": "kalshi-lead-bot/1.0"}
                    )
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                    if data.get("error"):
                        continue
                    result = data.get("result") or {}
                    if not result:
                        continue
                    row = next(iter(result.values()))
                    px = float(row["c"][0])  # last trade close
                    now = time.time()
                    with self._lock:
                        if sym not in self._kraken_hist:
                            self._kraken_hist[sym] = deque(maxlen=600)
                        self._kraken_hist[sym].append((now, px))
                        self._kraken_ok = True
                except Exception as e:
                    self._kraken_ok = False
                    self._last_error = f"kraken: {e}"
            self._stop.wait(max(2.0, self.poll_sec))

    def _pyth_loop(self) -> None:
        """Batch-poll Pyth Hermes for all mapped symbols in one request."""
        while not self._stop.is_set():
            id_syms = [(PYTH_IDS[s], s) for s in list(self.symbols) if s in PYTH_IDS]
            if not id_syms:
                self._stop.wait(10)
                continue
            q = "&".join(f"ids%5B%5D={i}" for i, _ in id_syms)
            url = f"{PYTH_HERMES}/v2/updates/price/latest?{q}"
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "kalshi-lead-bot/1.0",
                                  "Accept": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode())
                by_id = {
                    (i or "").lower().removeprefix("0x"): s for i, s in id_syms
                }
                primary_pushes: list[tuple[str, float, float]] = []
                with self._lock:
                    for p in data.get("parsed") or []:
                        pid = (p.get("id") or "").lower().removeprefix("0x")
                        sym = by_id.get(pid)
                        if not sym:
                            continue
                        pr = p.get("price") or {}
                        try:
                            px = float(pr["price"]) * (10 ** int(pr["expo"]))
                            ts = float(pr.get("publish_time") or time.time())
                        except (KeyError, TypeError, ValueError):
                            continue
                        if sym not in self._pyth_hist:
                            self._pyth_hist[sym] = deque(maxlen=600)
                        h = self._pyth_hist[sym]
                        # de-dupe identical publish times
                        if not h or h[-1][0] != ts:
                            h.append((ts, px))
                            if sym in PYTH_PRIMARY_SYMBOLS:
                                primary_pushes.append((sym, ts, px))
                    self._pyth_ok = True
                # Primary lean for metals: Hermes → _hist (outside lock via _push)
                for sym, ts, px in primary_pushes:
                    self._push(sym, ts, px, "hermes")
            except Exception as e:
                self._pyth_ok = False
                self._last_error = f"pyth: {e}"
            self._stop.wait(max(1.0, min(self.poll_sec, 2.0)))

    # --- signal math -------------------------------------------------------
    def _vol_locked(self, hist: Deque[Tick]) -> float:
        """Short-horizon realized vol from 1s returns (fraction)."""
        if len(hist) < 8:
            return 0.0
        # sample last ~window prices roughly evenly
        pts = list(hist)[-120:]
        rets = []
        for i in range(1, len(pts)):
            p0, p1 = pts[i - 1][1], pts[i][1]
            if p0 > 0 and p1 > 0:
                rets.append((p1 - p0) / p0)
        if len(rets) < 5:
            return 0.0
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / max(1, len(rets) - 1)
        # scale to window: sigma_1 * sqrt(n_steps in window)
        step = max(1e-6, (pts[-1][0] - pts[0][0]) / max(1, len(pts) - 1))
        n_steps = max(1.0, self.window_sec / step)
        return math.sqrt(var) * math.sqrt(n_steps)

    def _ret_over(self, hist: Deque, window: float, now: float) -> tuple[float, float]:
        """Return (ret, latest_px). hist entries are (ts, px, ...) or (ts, px)."""
        if not hist:
            return 0.0, 0.0
        latest_ts, latest_px = hist[-1][0], hist[-1][1]
        cutoff = latest_ts - window
        base_px = hist[0][1]
        for pt in hist:
            ts, px = pt[0], pt[1]
            if ts <= cutoff:
                base_px = px
            else:
                break
        if base_px <= 0:
            return 0.0, latest_px
        return (latest_px - base_px) / base_px, latest_px

    def _flow_over(self, hist: Deque[Tick], window: float) -> tuple[float, float]:
        """Taker imbalance in [-1, 1] and total qty over window."""
        if not hist:
            return 0.0, 0.0
        latest_ts = hist[-1][0]
        cutoff = latest_ts - window
        buy = sell = 0.0
        for ts, _px, qty, sign in hist:
            if ts < cutoff or qty <= 0 or sign == 0:
                continue
            if sign > 0:
                buy += qty
            else:
                sell += qty
        tot = buy + sell
        if tot <= 0:
            return 0.0, 0.0
        return (buy - sell) / tot, tot

    def _compute_locked(
        self,
        symbol: str,
        now: float | None = None,
        window_sec: float | None = None,
        base_threshold: float | None = None,
    ) -> LeadSignal:
        now = now if now is not None else time.time()
        window = self.window_sec if window_sec is None else float(window_sec)
        base_thr = self.base_threshold if base_threshold is None else float(base_threshold)
        hist = self._hist.get(symbol) or deque()
        if not hist:
            return LeadSignal(symbol, "flat", 0.0, 0.0, window, now, "")
        ret, latest_px = self._ret_over(hist, window, now)
        vol = self._vol_locked(hist)
        # Short windows: scale vol term down so threshold stays aggressive.
        vol_scale = 0.25 if window >= 10 else 0.15
        thresh = max(base_thr, self.vol_mult * vol * vol_scale)
        thresh = max(base_thr, thresh)
        if ret >= thresh:
            direction = "up"
        elif ret <= -thresh:
            direction = "down"
        else:
            direction = "flat"

        flow_win = min(window, self.flow_window_sec) if window <= 10 else self.flow_window_sec
        flow_imb, flow_qty = self._flow_over(hist, flow_win)
        # Taker flow veto: price lean without matching aggressors → treat flat
        if (
            self.taker_flow
            and direction != "flat"
            and flow_qty >= self.flow_min_qty
            and abs(flow_imb) >= self.flow_veto_imb
        ):
            if direction == "up" and flow_imb <= -self.flow_veto_imb:
                direction = "flat"
            elif direction == "down" and flow_imb >= self.flow_veto_imb:
                direction = "flat"

        # Taker-flow only applies to Binance trade hist; metals Hermes ticks
        # have taker_sign=0 so flow_qty stays 0 and this is a no-op.
        confirmed: bool | None = None
        if self.confirm and direction != "flat":
            cb = self._cb_hist.get(symbol)
            if cb and len(cb) >= 2:
                cb_ret, _ = self._ret_over(cb, window, now)
                if direction == "up":
                    confirmed = cb_ret > 0
                else:
                    confirmed = cb_ret < 0

        if symbol in PYTH_PRIMARY_SYMBOLS:
            src = "hermes"
        else:
            src = "binance-ws" if self._ws_ok else (self._active_base or "")
        return LeadSignal(
            symbol=symbol,
            direction=direction,
            ret_pct=ret,
            price=latest_px,
            window_sec=window,
            ts=hist[-1][0],
            source=src,
            vol=vol,
            threshold=thresh,
            confirmed=confirmed,
            flow_imb=flow_imb,
            flow_qty=flow_qty,
        )

    def signal(self, ticker_or_series: str,
               window_sec: float | None = None,
               base_threshold: float | None = None) -> LeadSignal | None:
        sym = symbol_for(ticker_or_series)
        if not sym:
            return None
        with self._lock:
            # Default cached 15s signal; recompute when a custom window is requested.
            if window_sec is None and base_threshold is None and sym in self._last:
                return self._last[sym]
            if self._hist.get(sym):
                return self._compute_locked(
                    sym, window_sec=window_sec, base_threshold=base_threshold,
                )
        return None

    def signal_fast(self, ticker_or_series: str) -> LeadSignal | None:
        """Aggressive short-horizon lean for soft-entry decisions."""
        return self.signal(
            ticker_or_series,
            window_sec=self.fast_window_sec,
            base_threshold=self.fast_threshold,
        )

    def agrees(self, ticker_or_series: str, kalshi_side: str,
               require_lean: bool = False,
               require_confirm: bool = False,
               window_sec: float | None = None,
               base_threshold: float | None = None,
               block_disagree_only: bool = False) -> tuple[bool, LeadSignal | None, str]:
        sig = self.signal(
            ticker_or_series, window_sec=window_sec, base_threshold=base_threshold,
        )
        if sig is None:
            return True, None, "no_symbol"
        if sig.price <= 0:
            return True, sig, "no_data_yet"
        want = "up" if kalshi_side == "yes" else "down"
        if sig.direction == "flat":
            if block_disagree_only:
                return True, sig, "flat_allow_aggressive"
            if require_lean:
                return False, sig, "flat_requires_lean"
            return True, sig, "flat_allow"
        if sig.direction != want:
            return False, sig, "disagree"
        if require_confirm or (
            self.confirm and os.environ.get("COINBASE_CONFIRM_STRICT", "0")
            .lower() in ("1", "true", "yes", "on")
        ):
            if sig.confirmed is False:
                return False, sig, "coinbase_disagree"
        return True, sig, "agree" if sig.confirmed is not False else "agree_unconfirmed"

    def risk_veto(self, ticker_or_series: str,
                  kalshi_side: str) -> tuple[bool, str]:
        """Block soft alt entries when BTC/ETH tape violently opposes.

        Returns (allow, reason). Majors themselves are never vetoed here.
        """
        if not self.risk_veto_enabled:
            return True, ""
        sym = symbol_for(ticker_or_series)
        if not sym or sym in RISK_VETO_SYMBOLS:
            return True, ""
        # Metals are a different risk factor — don't veto gold on a BTC dump.
        if sym in PYTH_PRIMARY_SYMBOLS:
            return True, ""
        want = "up" if kalshi_side == "yes" else "down"
        with self._lock:
            for maj in RISK_VETO_SYMBOLS:
                hist = self._hist.get(maj)
                if not hist:
                    continue
                ret, _ = self._ret_over(hist, self.risk_veto_window, time.time())
                if want == "up" and ret <= -self.risk_veto_pct:
                    return False, (
                        f"risk_veto:{maj}{ret*100:+.3f}%/"
                        f"{self.risk_veto_window:.0f}s vs {want}"
                    )
                if want == "down" and ret >= self.risk_veto_pct:
                    return False, (
                        f"risk_veto:{maj}{ret*100:+.3f}%/"
                        f"{self.risk_veto_window:.0f}s vs {want}"
                    )
        return True, ""

    def _dir_from_ret(self, ret: float, thresh: float) -> str:
        if ret >= thresh:
            return "up"
        if ret <= -thresh:
            return "down"
        return "flat"

    def venue_votes(self, ticker_or_series: str,
                     window_sec: float | None = None,
                     thresh: float | None = None) -> list[tuple[str, str, float]]:
        """Return [(venue, direction, ret)] for Binance/OKX/Kraken/Coinbase."""
        sym = symbol_for(ticker_or_series)
        if not sym:
            return []
        window = self.multi_venue_window if window_sec is None else float(window_sec)
        thr = self.multi_venue_pct if thresh is None else float(thresh)
        now = time.time()
        out: list[tuple[str, str, float]] = []
        with self._lock:
            # Primary hist: Binance for crypto, Hermes for metals
            primary = self._hist.get(sym)
            if primary and len(primary) >= 2:
                ret, _ = self._ret_over(primary, window, now)
                tag = "hermes" if sym in PYTH_PRIMARY_SYMBOLS else "bn"
                out.append((tag, self._dir_from_ret(ret, thr), ret))
            if self.okx_enabled and sym not in PYTH_PRIMARY_SYMBOLS:
                hx = self._okx_hist.get(sym)
                if hx and len(hx) >= 2:
                    ret, _ = self._ret_over(hx, window, now)
                    out.append(("okx", self._dir_from_ret(ret, thr), ret))
            if self.kraken_enabled and sym not in PYTH_PRIMARY_SYMBOLS:
                hx = self._kraken_hist.get(sym)
                if hx and len(hx) >= 2:
                    ret, _ = self._ret_over(hx, window, now)
                    out.append(("kraken", self._dir_from_ret(ret, thr), ret))
            if self.confirm:
                hx = self._cb_hist.get(sym)
                if hx and len(hx) >= 2:
                    ret, _ = self._ret_over(hx, window, now)
                    out.append(("cb", self._dir_from_ret(ret, thr), ret))
            # Separate pyth voter for crypto only (metals already voted as hermes)
            if self.pyth_enabled and sym not in PYTH_PRIMARY_SYMBOLS:
                hx = self._pyth_hist.get(sym)
                if hx and len(hx) >= 2:
                    ret, _ = self._ret_over(hx, window, now)
                    out.append(("pyth", self._dir_from_ret(ret, thr), ret))
        return out

    def multi_venue_confirm(
        self, ticker_or_series: str, kalshi_side: str,
    ) -> tuple[str, int, int, str]:
        """Multi-venue vote for soft full-size.

        Returns (status, agree_n, venue_n, detail) where status is:
          confirmed | weak | unavailable
        """
        if not self.multi_venue:
            return "confirmed", 0, 0, "multi_off"
        want = "up" if kalshi_side == "yes" else "down"
        votes = self.venue_votes(ticker_or_series)
        if not votes:
            return "unavailable", 0, 0, "no_votes"
        agree = sum(1 for _v, d, _r in votes if d == want)
        against = sum(1 for _v, d, _r in votes if d not in ("flat", want))
        detail = ",".join(
            f"{v}:{d}{r*100:+.3f}%" for v, d, r in votes
        )
        # Need enough same-way votes; any hard against without enough agrees → weak
        if agree >= self.multi_venue_min:
            return "confirmed", agree, len(votes), detail
        if against > 0 and agree < self.multi_venue_min:
            return "weak", agree, len(votes), detail
        return "weak", agree, len(votes), detail

    def status_line(self) -> str:
        with self._lock:
            parts = []
            for sym in self.symbols:
                sig = self._last.get(sym)
                if not sig:
                    parts.append(f"{sym}=n/a")
                else:
                    conf = ""
                    if sig.confirmed is True:
                        conf = "|cb✓"
                    elif sig.confirmed is False:
                        conf = "|cb×"
                    flow = ""
                    if self.taker_flow and abs(sig.flow_imb) >= 0.01:
                        flow = f"|f{sig.flow_imb:+.2f}"
                    parts.append(
                        f"{sym}:{sig.direction}({sig.ret_pct*100:+.3f}%/"
                        f"{sig.window_sec:.0f}s thr={sig.threshold*100:.3f}%"
                        f"{conf}{flow} @{sig.price:g})"
                    )
            err = f" err={self._last_error}" if self._last_error else ""
            src = "ws" if self._ws_ok else (self._active_base or "?")
            extras = []
            if self.taker_flow:
                extras.append(f"flow@{self.flow_window_sec:.0f}s≥{self.flow_veto_imb:g}")
            if self.risk_veto_enabled:
                extras.append(
                    f"veto={'/'.join(RISK_VETO_SYMBOLS)}@{self.risk_veto_pct*100:.2f}%"
                )
            if self.multi_venue:
                extras.append(
                    f"multi≥{self.multi_venue_min}"
                    f"(okx={'Y' if self._okx_ok else 'n'}"
                    f"/kraken={'Y' if self._kraken_ok else 'n'}"
                    f"/pyth={'Y' if self._pyth_ok else 'n'})"
                )
            extra = (" " + " ".join(extras)) if extras else ""
        return f"binance[{src}] " + " ".join(parts) + extra + err


def lean_enabled() -> bool:
    return os.environ.get("BINANCE_LEAD", "1").lower() in ("1", "true", "yes", "on")


def lean_mode() -> str:
    return os.environ.get("BINANCE_LEAD_MODE", "filter").lower()


if __name__ == "__main__":
    feed = BinanceLeadFeed(symbols=["XRPUSDT", "BNBUSDT", "SOLUSDT"])
    feed.start()
    try:
        for _ in range(10):
            time.sleep(2)
            print(feed.status_line())
    finally:
        feed.stop()
