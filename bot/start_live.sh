#!/usr/bin/env bash
# ANTI-NUKE core printer — BNB/XRP/BTC.
#
# Today's nukes were ALL soft/mid + bn=flat held to settle
# (BTC 91–92¢ skipped the soft BN gate at 90¢; ETH/SOL rode flat to −$18/−$10).
# TP/fade were green. Fix:
#   1) BN gate covers the whole tradable band (<95¢)
#   2) block bn=flat entries (agree-only)
#   3) flatten soft/mid before binary settle
#   4) tighter ticket cap
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
export RISK_FRAC_MIN=0.14
export RISK_FRAC_MAX=0.25
export EDGE_KELLY_FRAC=0.35
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=12
export EDGE_PRIOR_STRENGTH=20
export EDGE_PRIOR_WR=0.93
export HALT_FLOOR=45
export HALT_TRAIL_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# Bank winners — do not ride soft/mid to settle
export TAKE_PROFIT_ABS=0.97
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.95
export SPIKE_FADE=1
export SPIKE_PEAK=0.92
export SPIKE_GIVEBACK=0.05
export SPIKE_MIN_GAIN=0.03
# Flatten soft/mid in the last minute — never binary-settle the nuke band
export PRE_SETTLE_EXIT_SECS=60
export PRE_SETTLE_MAX_ENTRY=0.95
export EQUITY_HARVEST=0
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.95
export MAX_SPREAD=0.18
export WINDOW_SEC=840
export MIN_SECS_LEFT=20
export CONFIRM_POLLS=1
export POLL_SEC=1.25
export MAX_CONCURRENT=4
export MAX_EXPOSURE_FRAC=0.65
export SERIES=KXBNB15M,KXXRP15M,KXBTC15M
export SATELLITE_SERIES=
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
export SERIES_GOV=0
export SETUP_GOV=0
# Gate covers ALL tradable entries (skip-rich is 95¢) so 91–92¢ can't bypass BN
export SOFT_ENTRY_MAX=0.95
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=2
export STAGE_SIZE=0
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.20
# Block bn=flat — every big loser today
export SOFT_BN_FLAT_MULT=0
export MAX_SIZE_MULT=1.20
# One loss can't be a nuke
export TICKET_COST_CAP_FRAC=0.15
export LOSS_COOLDOWN_LOSSES=2
export LOSS_COOLDOWN_SEC=300
export LOSS_COOLDOWN_RISK_MULT=0.50
export BINANCE_LEAD=1
export BINANCE_WS=1
export COINBASE_CONFIRM=1
export BINANCE_LEAD_WINDOW_SEC=15
export BINANCE_LEAD_PCT=0.0008
export BINANCE_FAST_WINDOW_SEC=4
export BINANCE_FAST_PCT=0.0004
export TAKER_FLOW=1
export TAKER_FLOW_WINDOW_SEC=4
export TAKER_FLOW_VETO_IMB=0.35
export RISK_VETO=1
export RISK_VETO_SYMBOLS=BTCUSDT,ETHUSDT
export RISK_VETO_PCT=0.0012
export RISK_VETO_WINDOW_SEC=15
export MULTI_VENUE=1
export MULTI_VENUE_MIN_AGREE=2
export MULTI_VENUE_WINDOW_SEC=4
export MULTI_VENUE_PCT=0.0003
export MULTI_VENUE_STRICT=0
export OKX_CONFIRM=1
export KRAKEN_CONFIRM=1
export PYTH_CONFIRM=1
export PRIOR_DIR_BIAS=0
export EARLY_WINDOW_SEC=0
export LATE_WINDOW_SEC=0

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
