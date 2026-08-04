#!/usr/bin/env bash
# Live favorite-maker — overnight #3 + profitability upgrades 1-5.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
export RISK_FRACTION=0.18
export RISK_FRAC_MIN=0.13
export RISK_FRAC_MAX=0.25
export HALT_FLOOR=50
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export STOP_LOSS_PCT=0
export TAKE_PROFIT_ABS=0.995
export TAKE_PROFIT_MULT=0
export PRICE_LO=0.70
export PRICE_HI=0.999
# Skip junk rich favorites (1–3¢ books)
export SKIP_ENTRY_RICH=0.97
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=1.5
export MAX_CONCURRENT=6
export MAX_EXPOSURE_FRAC=0.70
# Core names full size; BTC half-size satellite; DOGE dropped
export SERIES=KXBNB15M,KXSOL15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M
export SATELLITE_SIZE_MULT=0.5
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=2
# Stage only applies to soft <85¢ in code
export STAGE_SIZE=1
export STAGE_SIZE_10M_MULT=0.50
export STAGE_SIZE_5M_MULT=0.75
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.25
export SOFT_BN_FLAT_MULT=0.50
export LOSS_COOLDOWN_LOSSES=2
export LOSS_COOLDOWN_SEC=900
export LOSS_COOLDOWN_RISK_MULT=0.50
export BINANCE_LEAD=1
export BINANCE_WS=1
export COINBASE_CONFIRM=1
export BINANCE_LEAD_WINDOW_SEC=15
export BINANCE_LEAD_PCT=0.0008
export BINANCE_FAST_WINDOW_SEC=4
export BINANCE_FAST_PCT=0.0004

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
