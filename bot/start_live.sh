#!/usr/bin/env bash
# Strategy #3 — OG day-1 printer restored.
# What went ~20–0 / 52-streak: 70¢+ favorites, 14m window, TP into 99¢,
# BNB/SOL/XRP/ETH core + BTC/DOGE satellites, Binance lead filter.
# Complexity that nuked the book later (setup_gov hot stacks, metals, early-tip)
# stays OFF. Ticket cost cap kept as the one hard lesson.
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
export EDGE_LOOKBACK=30
export EDGE_PNL_CLIP=25
# Floor under current ~$81 book; no profit-halt — run the #3 leg
export HALT_FLOOR=55
export HALT_TRAIL_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# OG printer: ride / TP into 99¢
export TAKE_PROFIT_ABS=0.99
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.97
export SPIKE_FADE=0
export EQUITY_HARVEST=0
# Strategy #3 band
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.97
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=1.5
export MAX_CONCURRENT=6
export MAX_EXPOSURE_FRAC=0.70
# OG universe
export SERIES=KXBNB15M,KXSOL15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M,KXDOGE15M
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
# Governors OFF — they stacked us into the ETH/BTC nukes
export SERIES_GOV=0
export SETUP_GOV=0
# Soft favorites full size (the #3 edge)
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=2
export STAGE_SIZE=1
export STAGE_SIZE_10M_MULT=0.50
export STAGE_SIZE_5M_MULT=0.75
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.25
# OG overnight allowed half-size on flat; not zero (zero starved #3)
export SOFT_BN_FLAT_MULT=0.50
export MAX_SIZE_MULT=1.35
# One guard from the school of hard knocks
export TICKET_COST_CAP_FRAC=0.25
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
