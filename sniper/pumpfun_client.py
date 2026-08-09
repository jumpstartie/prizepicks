"""Pump.fun public frontend API client for new / active coins."""

from __future__ import annotations

from typing import Any, Optional

import httpx

BASE = "https://frontend-api-v3.pump.fun"


class PumpFunClient:
    def __init__(self, client: httpx.AsyncClient, base: str = BASE):
        self.client = client
        self.base = base.rstrip("/")

    async def list_coins(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        sort: str = "created_timestamp",
        order: str = "DESC",
        include_nsfw: bool = False,
    ) -> list[dict[str, Any]]:
        params = {
            "limit": limit,
            "offset": offset,
            "sort": sort,
            "order": order,
            "includeNsfw": str(include_nsfw).lower(),
        }
        r = await self.client.get(f"{self.base}/coins", params=params, timeout=20.0)
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []

    async def get_coin(self, mint: str, *, sync: bool = False) -> Optional[dict[str, Any]]:
        r = await self.client.get(
            f"{self.base}/coins/{mint}",
            params={"sync": str(sync).lower()},
            timeout=20.0,
        )
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    async def newest(self, limit: int = 40) -> list[dict[str, Any]]:
        return await self.list_coins(limit=limit, sort="created_timestamp", order="DESC")

    async def hottest(self, limit: int = 40) -> list[dict[str, Any]]:
        return await self.list_coins(limit=limit, sort="last_trade_timestamp", order="DESC")
