"""Paper + live trade execution (PumpPortal local tx + Phantom keypair)."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

import httpx
from solders.commitment_config import CommitmentLevel
from solders.keypair import Keypair
from solders.rpc.config import RpcSendTransactionConfig
from solders.rpc.requests import SendVersionedTransaction
from solders.transaction import VersionedTransaction

PUMPPORTAL_TRADE_LOCAL = "https://pumpportal.fun/api/trade-local"


@dataclass
class Position:
    mint: str
    symbol: str
    side: str = "long"
    entry_mcap_usd: float = 0.0
    entry_sol: float = 0.0
    qty_tokens: float = 0.0
    opened_at: float = field(default_factory=time.time)
    tx: str = ""
    paper: bool = True
    quality_score: float = 0.0
    twitter: str = ""
    website: str = ""
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class Trader:
    def __init__(
        self,
        *,
        mode: str = "paper",
        keypair: Optional[Keypair] = None,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        buy_sol: float = 0.0015,
        slippage_pct: float = 5.0,
        priority_fee_sol: float = 0.00005,
        state_path: Path = Path("sniper/state.json"),
        trades_path: Path = Path("sniper/trades.jsonl"),
    ):
        self.mode = (mode or "paper").lower()
        self.keypair = keypair
        self.rpc_url = rpc_url
        self.buy_sol = float(buy_sol)
        self.slippage_pct = float(slippage_pct)
        self.priority_fee_sol = float(priority_fee_sol)
        self.state_path = state_path
        self.trades_path = trades_path
        self.positions: dict[str, Position] = {}
        self.paper_cash_sol = 1.0
        self._load()

    @property
    def live(self) -> bool:
        return self.mode == "live"

    def _load(self) -> None:
        if not self.state_path.exists():
            return
        try:
            data = json.loads(self.state_path.read_text())
            self.paper_cash_sol = float(data.get("paper_cash_sol", self.paper_cash_sol))
            for mint, raw in (data.get("positions") or {}).items():
                self.positions[mint] = Position(**raw)
        except Exception:
            pass

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "mode": self.mode,
            "paper_cash_sol": self.paper_cash_sol,
            "positions": {m: p.as_dict() for m, p in self.positions.items()},
            "updated_at": time.time(),
        }
        self.state_path.write_text(json.dumps(payload, indent=2))

    def _log_trade(self, event: dict[str, Any]) -> None:
        self.trades_path.parent.mkdir(parents=True, exist_ok=True)
        event = {**event, "ts": time.time(), "mode": self.mode}
        with self.trades_path.open("a") as f:
            f.write(json.dumps(event) + "\n")

    async def buy(
        self,
        client: httpx.AsyncClient,
        coin: dict[str, Any],
        *,
        quality_score: float,
        amount_sol: Optional[float] = None,
    ) -> Position:
        mint = str(coin["mint"])
        symbol = str(coin.get("symbol") or "?")
        mcap = float(coin.get("usd_market_cap") or 0)
        sol = float(amount_sol if amount_sol is not None else self.buy_sol)

        if mint in self.positions:
            raise RuntimeError(f"already open: {symbol}")

        if not self.live:
            if sol > self.paper_cash_sol:
                raise RuntimeError("paper cash insufficient")
            self.paper_cash_sol -= sol
            pos = Position(
                mint=mint,
                symbol=symbol,
                entry_mcap_usd=mcap,
                entry_sol=sol,
                qty_tokens=sol,  # abstract units
                paper=True,
                quality_score=quality_score,
                twitter=str(coin.get("twitter") or ""),
                website=str(coin.get("website") or ""),
                notes="paper_buy",
            )
            self.positions[mint] = pos
            self._log_trade(
                {
                    "event": "buy",
                    "mint": mint,
                    "symbol": symbol,
                    "sol": sol,
                    "mcap": mcap,
                    "quality": quality_score,
                    "paper": True,
                }
            )
            self.save()
            return pos

        if not self.keypair:
            raise RuntimeError("live mode requires Phantom keypair")

        sig = await self._pumpportal_trade(
            client,
            action="buy",
            mint=mint,
            amount=sol,
            denominated_in_sol=True,
        )
        pos = Position(
            mint=mint,
            symbol=symbol,
            entry_mcap_usd=mcap,
            entry_sol=sol,
            qty_tokens=0.0,
            paper=False,
            quality_score=quality_score,
            twitter=str(coin.get("twitter") or ""),
            website=str(coin.get("website") or ""),
            tx=sig,
            notes="live_buy",
        )
        self.positions[mint] = pos
        self._log_trade(
            {
                "event": "buy",
                "mint": mint,
                "symbol": symbol,
                "sol": sol,
                "mcap": mcap,
                "quality": quality_score,
                "tx": sig,
                "paper": False,
            }
        )
        self.save()
        return pos

    async def sell(
        self,
        client: httpx.AsyncClient,
        mint: str,
        *,
        reason: str,
        mark_mcap_usd: float = 0.0,
        pct: str = "100%",
    ) -> Optional[Position]:
        pos = self.positions.get(mint)
        if not pos:
            return None

        pnl_x = (mark_mcap_usd / pos.entry_mcap_usd) if pos.entry_mcap_usd > 0 and mark_mcap_usd > 0 else 0.0
        if not self.live or pos.paper:
            proceeds = pos.entry_sol * (pnl_x if pnl_x > 0 else 1.0)
            self.paper_cash_sol += proceeds
            self._log_trade(
                {
                    "event": "sell",
                    "mint": mint,
                    "symbol": pos.symbol,
                    "reason": reason,
                    "entry_mcap": pos.entry_mcap_usd,
                    "exit_mcap": mark_mcap_usd,
                    "pnl_x": pnl_x,
                    "proceeds_sol": proceeds,
                    "paper": True,
                }
            )
            del self.positions[mint]
            self.save()
            return pos

        sig = await self._pumpportal_trade(
            client,
            action="sell",
            mint=mint,
            amount=pct,
            denominated_in_sol=False,
        )
        self._log_trade(
            {
                "event": "sell",
                "mint": mint,
                "symbol": pos.symbol,
                "reason": reason,
                "entry_mcap": pos.entry_mcap_usd,
                "exit_mcap": mark_mcap_usd,
                "pnl_x": pnl_x,
                "tx": sig,
                "paper": False,
            }
        )
        del self.positions[mint]
        self.save()
        return pos

    async def _pumpportal_trade(
        self,
        client: httpx.AsyncClient,
        *,
        action: str,
        mint: str,
        amount: Any,
        denominated_in_sol: bool,
    ) -> str:
        assert self.keypair is not None
        pub = str(self.keypair.pubkey())
        # PumpPortal is picky: stringified amount/fees and pool=pump work more
        # reliably for bonding-curve micros than floats + pool=auto.
        amt = amount if isinstance(amount, str) else str(amount)
        form = {
            "publicKey": pub,
            "action": action,
            "mint": mint,
            "amount": amt,
            "denominatedInSol": "true" if denominated_in_sol else "false",
            "slippage": str(int(self.slippage_pct)),
            "priorityFee": str(self.priority_fee_sol),
            "pool": "pump",
        }
        r = await client.post(PUMPPORTAL_TRADE_LOCAL, data=form, timeout=40.0)
        if r.status_code != 200:
            # one retry on auto pool (migrated / raydium coins)
            if form["pool"] == "pump":
                form["pool"] = "auto"
                r = await client.post(PUMPPORTAL_TRADE_LOCAL, data=form, timeout=40.0)
            if r.status_code != 200:
                raise RuntimeError(
                    f"pumpportal trade-local {r.status_code}: {r.text[:300]} form={form}"
                )
        tx = VersionedTransaction(
            VersionedTransaction.from_bytes(r.content).message,
            [self.keypair],
        )
        commitment = CommitmentLevel.Confirmed
        config = RpcSendTransactionConfig(preflight_commitment=commitment)
        payload = SendVersionedTransaction(tx, config).to_json()
        rpc = await client.post(
            self.rpc_url,
            headers={"Content-Type": "application/json"},
            content=payload,
            timeout=40.0,
        )
        rpc.raise_for_status()
        body = rpc.json()
        if body.get("error"):
            raise RuntimeError(f"rpc send error: {body['error']}")
        sig = body.get("result")
        if not sig:
            raise RuntimeError(f"no signature in rpc response: {body}")
        return str(sig)
