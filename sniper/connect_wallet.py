#!/usr/bin/env python3
"""Verify Phantom key loads and print public address + SOL balance."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))

from runner import load_env_file
from wallet import get_sol_balance, load_keypair, pubkey_str


async def main() -> None:
    load_env_file(REPO / "secrets" / "sniper.env")
    rpc = os.getenv("SOLANA_RPC_URL") or "https://api.mainnet-beta.solana.com"
    kp = load_keypair()
    pub = pubkey_str(kp)
    bal = await get_sol_balance(rpc, pub)
    print("pubkey:", pub)
    print("balance_sol:", round(bal, 6))
    print("rpc:", rpc)
    print("phantom_ok: true")
    print()
    print("Next:")
    print("  1) Fund this address from Phantom (small test amount, e.g. 0.2–0.5 SOL)")
    print("  2) Keep SNIPER_MODE=paper until a dry scan looks good: bash sniper/start_paper.sh --once")
    print("  3) Live test: SNIPER_MODE=live BUY_SOL=0.02 bash sniper/start_live.sh")


if __name__ == "__main__":
    asyncio.run(main())
