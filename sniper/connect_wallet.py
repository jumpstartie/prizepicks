#!/usr/bin/env python3
"""Verify Phantom wallet (public address and/or private key) + SOL balance."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))

from runner import load_env_file
from wallet import WalletError, get_sol_balance, load_keypair, resolve_public_key


async def main() -> None:
    load_env_file(REPO / "secrets" / "sniper.env")
    rpc = os.getenv("SOLANA_RPC_URL") or "https://api.mainnet-beta.solana.com"

    keypair = None
    signing = False
    try:
        keypair = load_keypair()
        signing = True
    except WalletError:
        pass

    pub = resolve_public_key(keypair)
    if keypair is not None and str(keypair.pubkey()) != pub:
        configured = (os.getenv("PHANTOM_PUBLIC_KEY") or "").strip()
        if configured and configured != str(keypair.pubkey()):
            print("WARNING: PHANTOM_PUBLIC_KEY does not match private key pubkey")
            print("  public_env:", configured)
            print("  key_pubkey:", keypair.pubkey())

    bal = await get_sol_balance(rpc, pub)
    print("pubkey:", pub)
    print("balance_sol:", round(bal, 6))
    print("signing_ready:", signing)
    print("mode_hint:", "live-capable" if signing else "watch/paper-only (no private key)")
    print("rpc:", rpc)

    if bal < 0.05:
        print()
        print("NOTE: balance is low for live snipes. Fund this Phantom address first.")
    if not signing:
        print()
        print("To enable live buys: export private key in Phantom → write secrets/phantom.key")
        print("(do not paste the private key in chat)")
    else:
        print()
        print("Ready for tiny live tests after paper scan looks good.")


if __name__ == "__main__":
    asyncio.run(main())
