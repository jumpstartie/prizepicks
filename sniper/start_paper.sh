#!/usr/bin/env bash
# Paper-trade the community-quality Pump.fun sniper (no real SOL).
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONUNBUFFERED=1
if [[ -f secrets/sniper.env ]]; then
  set -a
  # shellcheck disable=SC1091
  source secrets/sniper.env
  set +a
fi
export SNIPER_MODE=paper
mkdir -p sniper
exec python3 -u sniper/runner.py --mode paper "$@"
