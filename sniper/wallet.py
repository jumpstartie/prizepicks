"""Load a Phantom-exported Solana keypair from secrets (never commit keys)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import base58
from solders.keypair import Keypair
import httpx


class WalletError(RuntimeError):
    pass


def _read_secret_file(path: Path) -> str:
    if not path.exists():
        raise WalletError(f"key file not found: {path}")
    return path.read_text().strip()


def load_keypair(
    private_key: Optional[str] = None,
    key_file: Optional[str] = None,
) -> Keypair:
    """
    Accepts:
      - base58 secret string (Phantom export)
      - JSON byte array [..] (Solana CLI id.json style)
      - path via key_file / PHANTOM_PRIVATE_KEY_FILE
    """
    raw = (private_key or os.getenv("PHANTOM_PRIVATE_KEY") or "").strip()
    file_path = key_file or os.getenv("PHANTOM_PRIVATE_KEY_FILE") or ""
    if not raw and file_path:
        raw = _read_secret_file(Path(file_path))
    if not raw:
        # convenience default path
        default = Path("secrets/phantom.key")
        if default.exists():
            raw = _read_secret_file(default)
    if not raw:
        raise WalletError(
            "No Phantom key configured. Export from Phantom → Security → Export Private Key, "
            "then set PHANTOM_PRIVATE_KEY in secrets/sniper.env or write secrets/phantom.key"
        )

    if raw.startswith("["):
        arr = json.loads(raw)
        return Keypair.from_bytes(bytes(arr))

    # strip quotes / whitespace
    raw = raw.strip().strip('"').strip("'")
    try:
        return Keypair.from_base58_string(raw)
    except Exception:
        # sometimes people paste 64-byte hex
        try:
            return Keypair.from_bytes(bytes.fromhex(raw))
        except Exception as e:
            raise WalletError(f"could not parse private key: {e}") from e


async def get_sol_balance(rpc_url: str, pubkey: str) -> float:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [pubkey],
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(rpc_url, json=payload, timeout=20.0)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise WalletError(str(data["error"]))
        lamports = int((data.get("result") or {}).get("value") or 0)
        return lamports / 1_000_000_000


def pubkey_str(kp: Keypair) -> str:
    return str(kp.pubkey())


def resolve_public_key(keypair: Optional[Keypair] = None) -> str:
    """Prefer loaded keypair pubkey; else PHANTOM_PUBLIC_KEY from env."""
    if keypair is not None:
        return str(keypair.pubkey())
    pub = (os.getenv("PHANTOM_PUBLIC_KEY") or "").strip()
    if not pub:
        raise WalletError(
            "No wallet address. Set PHANTOM_PUBLIC_KEY or provide a Phantom private key."
        )
    # validate format
    from solders.pubkey import Pubkey

    try:
        return str(Pubkey.from_string(pub))
    except Exception as e:
        raise WalletError(f"invalid PHANTOM_PUBLIC_KEY: {e}") from e
