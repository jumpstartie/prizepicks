"""Minimal Kalshi REST client: public market data + optional authenticated trading.

Auth requires:
  KALSHI_API_KEY_ID   - key id from kalshi.com/account/profile
  KALSHI_PRIVATE_KEY  - PEM string, OR
  KALSHI_PRIVATE_KEY_PATH - path to PEM file

Hosts:
  public/prod shared: https://api.elections.kalshi.com/trade-api/v2
  prod trading:       https://external-api.kalshi.com/trade-api/v2
  demo trading:       https://external-api.demo.kalshi.co/trade-api/v2
"""
from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Optional

PUBLIC_BASE = "https://api.elections.kalshi.com/trade-api/v2"
PROD_BASE = "https://external-api.kalshi.com/trade-api/v2"
DEMO_BASE = "https://external-api.demo.kalshi.co/trade-api/v2"


class KalshiClient:
    def __init__(self, demo: bool = False):
        self.demo = demo
        self.public_base = PUBLIC_BASE
        self.trade_base = DEMO_BASE if demo else PROD_BASE
        self.key_id = os.environ.get("KALSHI_API_KEY_ID", "").strip()
        self._private_key = None
        pem = os.environ.get("KALSHI_PRIVATE_KEY", "").strip()
        path = os.environ.get("KALSHI_PRIVATE_KEY_PATH", "").strip()
        if pem or path:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.backends import default_backend
            raw = pem.encode() if pem else open(path, "rb").read()
            # support literal \n in env vars
            if pem and "\\n" in pem:
                raw = pem.replace("\\n", "\n").encode()
            self._private_key = serialization.load_pem_private_key(
                raw, password=None, backend=default_backend()
            )

    @property
    def can_trade(self) -> bool:
        return bool(self.key_id and self._private_key)

    def _sign(self, timestamp_ms: str, method: str, path: str) -> str:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        path_no_query = path.split("?", 1)[0]
        msg = f"{timestamp_ms}{method}{path_no_query}".encode()
        sig = self._private_key.sign(
            msg,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.DIGEST_LENGTH),
            hashes.SHA256(),
        )
        return base64.b64encode(sig).decode()

    def _request(self, method: str, base: str, path: str, body: Optional[dict] = None,
                 auth: bool = False, tries: int = 4) -> Any:
        url = base + path
        data = None if body is None else json.dumps(body).encode()
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if auth:
            if not self.can_trade:
                raise RuntimeError("trading requires KALSHI_API_KEY_ID + private key")
            # path for signing includes /trade-api/v2 prefix
            sign_path = "/trade-api/v2" + path.split("?", 1)[0]
            ts = str(int(time.time() * 1000))
            headers.update({
                "KALSHI-ACCESS-KEY": self.key_id,
                "KALSHI-ACCESS-TIMESTAMP": ts,
                "KALSHI-ACCESS-SIGNATURE": self._sign(ts, method, sign_path),
            })
        for i in range(tries):
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(1.5 * (i + 1))
                    continue
                detail = e.read().decode(errors="replace")
                raise RuntimeError(f"HTTP {e.code} {method} {path}: {detail}") from e
            except Exception:
                time.sleep(0.8 * (i + 1))
        raise RuntimeError(f"failed {method} {path}")

    # ---- public market data ----
    def open_markets(self, series: str) -> list[dict]:
        q = urllib.parse.urlencode({"series_ticker": series, "status": "open", "limit": 10})
        d = self._request("GET", self.public_base, f"/markets?{q}")
        return d.get("markets", [])

    def market(self, ticker: str) -> dict:
        d = self._request("GET", self.public_base, f"/markets/{ticker}")
        return d.get("market", d)

    def balance(self) -> dict:
        return self._request("GET", self.trade_base, "/portfolio/balance", auth=True)

    def get_order(self, order_id: str) -> dict:
        d = self._request("GET", self.trade_base, f"/portfolio/orders/{order_id}", auth=True)
        return d.get("order", d)

    def get_positions(self, ticker: Optional[str] = None) -> list[dict]:
        q = {"limit": 200, "count_filter": "position,total_traded"}
        if ticker:
            q["ticker"] = ticker
        path = "/portfolio/positions?" + urllib.parse.urlencode(q)
        d = self._request("GET", self.trade_base, path, auth=True)
        return d.get("market_positions", [])

    def create_order(self, ticker: str, side: str, count: float, price: float,
                     post_only: bool = True, client_order_id: Optional[str] = None,
                     expiration_ts: Optional[int] = None) -> dict:
        """V2 create order. side is 'bid' (buy YES) or 'ask' (sell YES / buy NO)."""
        body = {
            "ticker": ticker,
            "side": side,
            "count": f"{count:.2f}",
            "price": f"{price:.4f}",
            "time_in_force": "good_till_canceled",
            "self_trade_prevention_type": "taker_at_cross",
            "post_only": post_only,
            "client_order_id": client_order_id or str(uuid.uuid4()),
            "exchange_index": -1,
        }
        if expiration_ts:
            body["expiration_time"] = int(expiration_ts)
        return self._request("POST", self.trade_base, "/portfolio/events/orders",
                             body=body, auth=True)

    def cancel_order(self, order_id: str, market_ticker: Optional[str] = None) -> dict:
        path = f"/portfolio/events/orders/{order_id}?exchange_index=-1"
        if market_ticker:
            path += "&market_ticker=" + urllib.parse.quote(market_ticker)
        return self._request("DELETE", self.trade_base, path, auth=True)
