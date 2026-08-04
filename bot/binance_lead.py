"""Fast lead feed for Kalshi 15m crypto up/down markets.

Primary: Binance trade WebSocket (data-stream.binance.vision)
Confirm: Coinbase spot REST (same-direction check)
Fallback: Binance REST poller

Kalshi YES ~= underlying UP; Kalshi NO ~= underlying DOWN.
Threshold is vol-adjusted so quiet tapes don't spam false leans.
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
}
COINBASE_PRODUCT = {
    "XRPUSDT": "XRP-USD",
    "BNBUSDT": "BNB-USD",
    "SOLUSDT": "SOL-USD",
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "DOGEUSDT": "DOGE-USD",
}


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


def series_root(ticker_or_series: str) -> str:
    parts = ticker_or_series.split("-")
    return parts[0] if parts else ticker_or_series


def symbol_for(ticker_or_series: str) -> str | None:
    return SERIES_SYMBOLS.get(series_root(ticker_or_series))


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
        self.bases = bases
        self._hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=5000) for s in self.symbols
        }
        self._cb_hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._last: dict[str, LeadSignal] = {}
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []
        self._active_base: str | None = None
        self._last_error: str = ""
        self._ws_ok = False

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
                added.append(sym)
        return added

    # --- feeds -------------------------------------------------------------
    def _push(self, symbol: str, ts: float, px: float, source: str) -> None:
        with self._lock:
            if symbol not in self._hist:
                self._hist[symbol] = deque(maxlen=5000)
                if symbol not in self.symbols:
                    self.symbols.append(symbol)
            self._hist[symbol].append((ts, px))
            self._active_base = source
            self._last[symbol] = self._compute_locked(symbol, ts)

    def _ws_loop(self) -> None:
        try:
            import websocket  # type: ignore
        except Exception as e:
            self._last_error = f"websocket import: {e}"
            return
        while not self._stop.is_set():
            streams = "/".join(f"{s.lower()}@trade" for s in list(self.symbols))
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
                    ts = float(data.get("T") or data.get("E") or time.time() * 1000) / 1000.0
                    if sym:
                        self._push(sym, ts, px, "binance-ws")
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

    # --- signal math -------------------------------------------------------
    def _vol_locked(self, hist: Deque[tuple[float, float]]) -> float:
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

    def _ret_over(self, hist: Deque[tuple[float, float]],
                  window: float, now: float) -> tuple[float, float]:
        if not hist:
            return 0.0, 0.0
        latest_ts, latest_px = hist[-1]
        cutoff = latest_ts - window
        base_px = hist[0][1]
        for ts, px in hist:
            if ts <= cutoff:
                base_px = px
            else:
                break
        if base_px <= 0:
            return 0.0, latest_px
        return (latest_px - base_px) / base_px, latest_px

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

        confirmed: bool | None = None
        if self.confirm and direction != "flat":
            cb = self._cb_hist.get(symbol)
            if cb and len(cb) >= 2:
                cb_ret, _ = self._ret_over(cb, window, now)
                if direction == "up":
                    confirmed = cb_ret > 0
                else:
                    confirmed = cb_ret < 0

        return LeadSignal(
            symbol=symbol,
            direction=direction,
            ret_pct=ret,
            price=latest_px,
            window_sec=window,
            ts=hist[-1][0],
            source=("binance-ws" if self._ws_ok else (self._active_base or "")),
            vol=vol,
            threshold=thresh,
            confirmed=confirmed,
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
                    parts.append(
                        f"{sym}:{sig.direction}({sig.ret_pct*100:+.3f}%/"
                        f"{sig.window_sec:.0f}s thr={sig.threshold*100:.3f}%"
                        f"{conf} @{sig.price:g})"
                    )
            err = f" err={self._last_error}" if self._last_error else ""
            src = "ws" if self._ws_ok else (self._active_base or "?")
        return f"binance[{src}] " + " ".join(parts) + err


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
