#!/usr/bin/env bash
# Live favorite-maker launch (post +$50 pause config).
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
export RISK_FRAC_MIN=0.10
export RISK_FRAC_MAX=0.25
export HALT_FLOOR=50
export HALT_LOSS_BUFFER=1
# +$50 from start_equity (reset to flat bankroll when resuming a #3 leg)
export HALT_PROFIT=50
export STOP_LOSS_PCT=0
export TAKE_PROFIT_ABS=0.995
export TAKE_PROFIT_MULT=0
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.999
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=3
export MAX_CONCURRENT=6
export MAX_EXPOSURE_FRAC=0.70
export SERIES=KXBNB15M,KXSOL15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M,KXDOGE15M
export SATELLITE_SIZE_MULT=0.5
# Strategy #3: full size on soft favorites (no soft cut)
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export BINANCE_LEAD=1
export BINANCE_WS=1
export COINBASE_CONFIRM=1

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
