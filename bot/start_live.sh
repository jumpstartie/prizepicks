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
export EDGE_KELLY_FRAC=0.33
export HALT_FLOOR=70
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export STOP_LOSS_PCT=0
export TAKE_PROFIT_ABS=0.98
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
# Soft/mid favorites (<88¢) ride to settle; TP only on richer entries
export TAKE_PROFIT_MIN_ENTRY=0.88
export PRICE_LO=0.70
export PRICE_HI=0.999
# Skip thin-margin rich favorites — redeploy into fatter 70–90¢ books
export SKIP_ENTRY_RICH=0.95
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=1.0
export MAX_CONCURRENT=8
export MAX_EXPOSURE_FRAC=0.85
# Core names full size; BTC/DOGE/NEAR half-size satellites (more boards, less dead time)
export SERIES=KXBNB15M,KXSOL15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M,KXDOGE15M,KXNEAR15M
export SATELLITE_SIZE_MULT=0.5
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
# Soft corr was the #2 skip reason — allow one more soft favorite
export SOFT_CORR_MAX=3
# Stage only applies to soft <85¢ in code
export STAGE_SIZE=1
export STAGE_SIZE_10M_MULT=0.50
export STAGE_SIZE_5M_MULT=0.75
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.50
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
# Taker-flow filter: flatten ret leans that disagree with aggressor tape
export TAKER_FLOW=1
export TAKER_FLOW_WINDOW_SEC=4
export TAKER_FLOW_VETO_IMB=0.35
# Block soft alt entries when BTC/ETH violently opposes
export RISK_VETO=1
export RISK_VETO_SYMBOLS=BTCUSDT,ETHUSDT
export RISK_VETO_PCT=0.0012
export RISK_VETO_WINDOW_SEC=15

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
