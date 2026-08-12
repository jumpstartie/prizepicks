#!/usr/bin/env python3
"""Write gitignored secrets/ files from KALSHI_* env vars (cloud secret injection)."""

from __future__ import annotations

import os
from pathlib import Path


def _normalize_pem(pem: str) -> str:
    pem = pem.strip()
    if not pem:
        return ""
    # Secret stores often inject literal \n instead of real newlines.
    if "-----BEGIN" in pem and "\n" not in pem and "\\n" in pem:
        pem = pem.replace("\\n", "\n")
    elif "\\n" in pem and pem.count("\n") < 2:
        pem = pem.replace("\\n", "\n")
    return pem if pem.endswith("\n") else pem + "\n"


def main() -> None:
    secrets = Path("secrets")
    secrets.mkdir(exist_ok=True)

    key_id = (os.environ.get("KALSHI_API_KEY_ID") or "").strip()
    pem = _normalize_pem(os.environ.get("KALSHI_PRIVATE_KEY") or "")
    path = (os.environ.get("KALSHI_PRIVATE_KEY_PATH") or "").strip()

    if pem:
        key_path = secrets / "kalshi.key"
        key_path.write_text(pem)
        key_path.chmod(0o600)
        path = str(key_path.resolve())
        os.environ["KALSHI_PRIVATE_KEY_PATH"] = path
        print(f"materialized {key_path}")

    if key_id and path:
        env_path = secrets / "env.sh"
        env_path.write_text(
            f"export KALSHI_API_KEY_ID='{key_id}'\n"
            f"export KALSHI_PRIVATE_KEY_PATH={path}\n"
        )
        env_path.chmod(0o600)
        print(f"materialized {env_path}")


if __name__ == "__main__":
    main()
