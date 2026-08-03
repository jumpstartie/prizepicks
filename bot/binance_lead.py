"""Binance spot lead feed for Kalshi 15m crypto up/down markets.

Polls Binance public market data (no API key) and classifies short-horizon
direction so the Kalshi runner can lean/filter favorites:

  Kalshi YES  ~= underlying UP
  Kalshi NO   ~= underlying DOWN

Primary endpoint defaults to data-api.binance.vision (works where
api.binance.com is geo-blocked). Falls back to api.binance.us.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from collections import deque
from dataclasses import dataclass
from typing import Deque


DEFAULT_BASES = (
    os.environ.get("BINANCE_API_BASE", "https://data-api.binance.vision"),
    "https://api.binance.us",
    "https://api.binance.com",
)

# Kalshi series root -> Binance spot symbol
SERIES_SYMBOLS = {
    "KXXRP15M": "XRPUSDT",
    "KXBNB15M": "BNBUSDT",
    "KXSOL15M": "SOLUSDT",
    "KXBTC15M": "BTCUSDT",
    "KXETH15M": "ETHUSDT",
    "KXDOGE15M": "DOGEUSDT",
}


@dataclass
class LeadSignal:
    symbol: str
    direction: str          # "up" | "down" | "flat"
    ret_pct: float          # fractional return over window (e.g. 0.001 = +0.10%)
    price: float
    window_sec: float
    ts: float
    source: str


def series_root(ticker_or_series: str) -> str:
    # KXXRP15M-26AUG031745-45 -> KXXRP15M
    parts = ticker_or_series.split("-")
    return parts[0] if parts else ticker_or_series


def symbol_for(ticker_or_series: str) -> str | None:
    root = series_root(ticker_or_series)
    return SERIES_SYMBOLS.get(root)


class BinanceLeadFeed:
    """Background sampler of Binance last prices + lean helper."""

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
            else os.environ.get("BINANCE_LEAD_WINDOW_SEC", "20")
        )
        # Move larger than this (fraction) counts as a lean. Default 0.08%.
        self.threshold_pct = float(
            threshold_pct if threshold_pct is not None
            else os.environ.get("BINANCE_LEAD_PCT", "0.0008")
        )
        self.poll_sec = float(
            poll_sec if poll_sec is not None
            else os.environ.get("BINANCE_LEAD_POLL_SEC", "2")
        )
        self.bases = bases
        self._hist: dict[str, Deque[tuple[float, float]]] = {
            s: deque(maxlen=600) for s in self.symbols
        }
        self._last: dict[str, LeadSignal] = {}
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._active_base: str | None = None
        self._last_error: str = ""

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, name="binance-lead", daemon=True
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3)

    def ensure_symbols(self, symbols: list[str] | set[str]) -> list[str]:
        """Add symbols at runtime (e.g. when new series/positions appear)."""
        added: list[str] = []
        with self._lock:
            for sym in symbols:
                if not sym or sym in self._hist:
                    continue
                self.symbols.append(sym)
                self._hist[sym] = deque(maxlen=600)
                added.append(sym)
        return added

    def _fetch_price(self, symbol: str) -> tuple[float, str]:
        last_err: Exception | None = None
        # Prefer last working base
        bases = list(self.bases)
        if self._active_base and self._active_base in bases:
            bases.remove(self._active_base)
            bases.insert(0, self._active_base)
        for base in bases:
            url = f"{base.rstrip('/')}/api/v3/ticker/price?symbol={symbol}"
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "kalshi-lead-bot/1.0"}
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                px = float(data["price"])
                self._active_base = base
                return px, base
            except Exception as e:
                last_err = e
                continue
        raise RuntimeError(f"binance price failed for {symbol}: {last_err}")

    def _loop(self) -> None:
        while not self._stop.is_set():
            now = time.time()
            for sym in self.symbols:
                try:
                    px, src = self._fetch_price(sym)
                    with self._lock:
                        self._hist[sym].append((now, px))
                        self._last[sym] = self._compute_locked(sym, now)
                    self._last_error = ""
                except Exception as e:
                    self._last_error = str(e)
            self._stop.wait(self.poll_sec)

    def _compute_locked(self, symbol: str, now: float | None = None) -> LeadSignal:
        now = now if now is not None else time.time()
        hist = self._hist[symbol]
        if not hist:
            return LeadSignal(symbol, "flat", 0.0, 0.0, self.window_sec, now,
                              self._active_base or "")
        latest_ts, latest_px = hist[-1]
        # oldest price at or before now - window
        cutoff = latest_ts - self.window_sec
        base_px = hist[0][1]
        for ts, px in hist:
            if ts <= cutoff:
                base_px = px
            else:
                break
        if base_px <= 0:
            ret = 0.0
        else:
            ret = (latest_px - base_px) / base_px
        if ret >= self.threshold_pct:
            direction = "up"
        elif ret <= -self.threshold_pct:
            direction = "down"
        else:
            direction = "flat"
        return LeadSignal(
            symbol=symbol,
            direction=direction,
            ret_pct=ret,
            price=latest_px,
            window_sec=self.window_sec,
            ts=latest_ts,
            source=self._active_base or "",
        )

    def signal(self, ticker_or_series: str) -> LeadSignal | None:
        sym = symbol_for(ticker_or_series)
        if not sym:
            return None
        with self._lock:
            if sym in self._last:
                return self._last[sym]
            if self._hist.get(sym):
                return self._compute_locked(sym)
        return None

    def agrees(self, ticker_or_series: str, kalshi_side: str,
               require_lean: bool = False) -> tuple[bool, LeadSignal | None, str]:
        """Return (ok_to_trade, signal, reason).

        kalshi_side: 'yes' (UP) or 'no' (DOWN).
        - filter mode (require_lean=False): block only on strong opposite lean
        - strict mode (require_lean=True): require matching up/down lean
        """
        sig = self.signal(ticker_or_series)
        if sig is None:
            return True, None, "no_symbol"
        if sig.price <= 0:
            return True, sig, "no_data_yet"
        want = "up" if kalshi_side == "yes" else "down"
        if sig.direction == "flat":
            if require_lean:
                return False, sig, "flat_requires_lean"
            return True, sig, "flat_allow"
        if sig.direction == want:
            return True, sig, "agree"
        return False, sig, "disagree"

    def status_line(self) -> str:
        with self._lock:
            parts = []
            for sym in self.symbols:
                sig = self._last.get(sym)
                if not sig:
                    parts.append(f"{sym}=n/a")
                else:
                    parts.append(
                        f"{sym}:{sig.direction}({sig.ret_pct*100:+.3f}%/"
                        f"{sig.window_sec:.0f}s @{sig.price:g})"
                    )
            err = f" err={self._last_error}" if self._last_error else ""
            src = self._active_base or "?"
        return f"binance[{src}] " + " ".join(parts) + err


def lean_enabled() -> bool:
    return os.environ.get("BINANCE_LEAD", "1").lower() in ("1", "true", "yes", "on")


def lean_mode() -> str:
    """filter (default) | strict | off"""
    return os.environ.get("BINANCE_LEAD_MODE", "filter").lower()


if __name__ == "__main__":
    feed = BinanceLeadFeed(symbols=["XRPUSDT", "BNBUSDT", "SOLUSDT"])
    feed.start()
    try:
        for i in range(8):
            time.sleep(2)
            print(feed.status_line())
            for s in ("KXXRP15M", "KXBNB15M", "KXSOL15M"):
                sig = feed.signal(s)
                print(" ", s, sig)
    finally:
        feed.stop()
