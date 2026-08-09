"""Optional Axiom Trade helpers (auth tokens / SDK) for Pulse-style feeds.

Primary discovery uses Pump.fun public API so the sniper works without Axiom.
When AXIOM_ACCESS_TOKEN (+ refresh) are set, we try the community SDK for
balance checks and new-token websocket hints.
"""

from __future__ import annotations

import os
from typing import Any, Optional


class AxiomBridge:
    def __init__(
        self,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ):
        self.access_token = access_token or os.getenv("AXIOM_ACCESS_TOKEN") or ""
        self.refresh_token = refresh_token or os.getenv("AXIOM_REFRESH_TOKEN") or ""
        self._client = None

    @property
    def enabled(self) -> bool:
        return bool(self.access_token)

    def client(self):
        if self._client is not None:
            return self._client
        if not self.enabled:
            return None
        try:
            from axiomtradeapi import AxiomTradeClient  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "axiomtradeapi not installed. pip install axiomtradeapi"
            ) from e
        self._client = AxiomTradeClient(
            auth_token=self.access_token,
            refresh_token=self.refresh_token or None,
        )
        return self._client

    def get_balance(self, wallet: str) -> Optional[dict[str, Any]]:
        c = self.client()
        if not c:
            return None
        return c.GetBalance(wallet)
