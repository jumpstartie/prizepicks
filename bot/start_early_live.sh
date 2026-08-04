#!/usr/bin/env bash
# Early-tip LIVE — Binance-lead speed play in first ~3m while book is cheap.
# Runs standalone; does not touch favorite-maker state.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export EARLY_SERIES="${EARLY_SERIES:-KXBTC15M,KXETH15M,KXXRP15M,KXBNB15M,KXDOGE15M,KXSOL15M,KXNEAR15M}"
export EARLY_SECS="${EARLY_SECS:-180}"
export EARLY_FAV_MAX="${EARLY_FAV_MAX:-0.68}"
export EARLY_STRONG_PCT="${EARLY_STRONG_PCT:-0.0008}"
export EARLY_MV_MIN_AGREE="${EARLY_MV_MIN_AGREE:-2}"
export EARLY_ENTRY_MAX="${EARLY_ENTRY_MAX:-0.72}"
export EARLY_STAKE_FRAC="${EARLY_STAKE_FRAC:-0.08}"
export EARLY_STAKE_CAP="${EARLY_STAKE_CAP:-12}"
export EARLY_MAX_OPEN="${EARLY_MAX_OPEN:-2}"
export EARLY_POLL_SEC="${EARLY_POLL_SEC:-2}"
# User override: arm now (paper was 4-0; originally waiting for 5-0).
export EARLY_ARM_WINS="${EARLY_ARM_WINS:-0}"
export EARLY_ARM_MAX_LOSSES="${EARLY_ARM_MAX_LOSSES:-0}"
export EARLY_DAY_STOP_LOSS="${EARLY_DAY_STOP_LOSS:-15}"

exec python3 -u bot/early_tip_live.py
