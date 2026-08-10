#!/usr/bin/env bash
# LIVE sniper — spends real SOL. Requires secrets/sniper.env + Phantom key.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
if [[ ! -f secrets/sniper.env && ! -f secrets/phantom.key ]]; then
  echo "Missing secrets. Copy sniper/secrets.env.example → secrets/sniper.env and add PHANTOM_PRIVATE_KEY."
  exit 1
fi
if [[ -f secrets/sniper.env ]]; then
  set -a
  # shellcheck disable=SC1091
  source secrets/sniper.env
  set +a
fi
export SNIPER_MODE=live
echo "WARNING: live mode will buy tokens with real SOL from your Phantom keypair."
python3 -u sniper/connect_wallet.py
exec python3 -u sniper/runner.py --mode live --connect-wallet "$@"
