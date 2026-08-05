#!/usr/bin/env bash
# HOT STREAK — day-1 / day-2 printer, not the nuke stack.
#
# What actually made the money (from live book):
#   soft/mid + take_profit  ≈ +$260
#   soft/mid + settle       ≈ −$230  (the drain)
# Best coins: XRP / BNB / BTC. SOL & metals & NEAR were net drains.
# ETH printed day-1 then became the nuke magnet — satellite only.
#
# Playbook: press 70–90¢ favorites, BANK via TP/spike-fade, half-size
# on bn=flat (don't block — flat+TP was the streak). No governors,
# no early-tip, no metals. Tight ticket cap so one settle can't end the day.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
export RISK_FRACTION=0.20
export RISK_FRAC_MIN=0.16
export RISK_FRAC_MAX=0.28
export EDGE_KELLY_FRAC=0.40
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=12
export EDGE_PRIOR_STRENGTH=20
export EDGE_PRIOR_WR=0.93
# ~$72 book → room to trade; trail off so we don't self-halt mid-sprint
export HALT_FLOOR=48
export HALT_TRAIL_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# BANK winners — this is the whole edge vs riding to settle
export TAKE_PROFIT_ABS=0.97
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.95
export SPIKE_FADE=1
export SPIKE_PEAK=0.92
export SPIKE_GIVEBACK=0.05
export SPIKE_MIN_GAIN=0.03
export EQUITY_HARVEST=0
# Fat mid books; skip skinny ≥95¢
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.95
export MAX_SPREAD=0.18
export WINDOW_SEC=840
export MIN_SECS_LEFT=20
export CONFIRM_POLLS=1
export POLL_SEC=1.25
export MAX_CONCURRENT=5
export MAX_EXPOSURE_FRAC=0.70
# Printers only. Drop SOL/NEAR/metals. ETH satellite after nukes.
export SERIES=KXBNB15M,KXXRP15M,KXBTC15M
export SATELLITE_SERIES=KXDOGE15M,KXETH15M
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
export SERIES_GOV=0
export SETUP_GOV=0
# Soft/mid through 90¢ — day-1 money band
export SOFT_ENTRY_MAX=0.90
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=3
export STAGE_SIZE=0
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.25
# Half-size on flat (do NOT block — flat+TP printed the streak)
export SOFT_BN_FLAT_MULT=0.50
export MAX_SIZE_MULT=1.25
# One bad settle ≤ ~20% of book
export TICKET_COST_CAP_FRAC=0.20
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
