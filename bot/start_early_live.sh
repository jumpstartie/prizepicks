#!/usr/bin/env bash
# Early-tip LIVE — OPTIONAL sleeve. Default DISARMED for overnight so it
# cannot drain the shared book under the favorite-maker floor again.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export EARLY_SERIES="${EARLY_SERIES:-KXBTC15M,KXETH15M,KXXRP15M,KXBNB15M,KXDOGE15M}"
export EARLY_SECS="${EARLY_SECS:-180}"
export EARLY_FAV_MAX="${EARLY_FAV_MAX:-0.68}"
export EARLY_STRONG_PCT="${EARLY_STRONG_PCT:-0.0008}"
export EARLY_MV_MIN_AGREE="${EARLY_MV_MIN_AGREE:-2}"
export EARLY_ENTRY_MAX="${EARLY_ENTRY_MAX:-0.72}"
export EARLY_STAKE_FRAC="${EARLY_STAKE_FRAC:-0.05}"
export EARLY_STAKE_CAP="${EARLY_STAKE_CAP:-8}"
export EARLY_MAX_OPEN="${EARLY_MAX_OPEN:-1}"
export EARLY_POLL_SEC="${EARLY_POLL_SEC:-2}"
# Overnight default: DISARMED. Set EARLY_FORCE_ARM=1 only when intentionally live.
export EARLY_FORCE_ARM="${EARLY_FORCE_ARM:-0}"
export EARLY_ARM_WINS="${EARLY_ARM_WINS:-5}"
export EARLY_ARM_MAX_LOSSES="${EARLY_ARM_MAX_LOSSES:-0}"
export EARLY_DAY_STOP_LOSS="${EARLY_DAY_STOP_LOSS:-10}"
export EARLY_DISARM_LOSSES_IN_10="${EARLY_DISARM_LOSSES_IN_10:-3}"

exec python3 -u bot/early_tip_live.py
