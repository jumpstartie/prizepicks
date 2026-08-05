#!/usr/bin/env bash
# Live favorite-maker — overnight mid-TP compound (anti-nuke).
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
# Overnight: trade through chop, but never re-lever to nuke size
export RISK_FRACTION=0.20
export RISK_FRAC_MIN=0.15
export RISK_FRAC_MAX=0.20
export EDGE_KELLY_FRAC=0.35
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=20
export EDGE_PRIOR_STRENGTH=24
export EDGE_PRIOR_WR=0.92
# Hard ticket cost cap — 101-contract ETH was 46% of book; never again
export TICKET_COST_CAP_FRAC=0.22
# Floor under current cash so we can trade; trail locks gains as HW climbs
export HALT_FLOOR=60
export HALT_TRAIL_FRAC=0.65
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# Mid-band TP harvest was the $190 path — TP earlier on mid entries
export TAKE_PROFIT_ABS=0.98
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0.85
export EQUITY_HARVEST=1
export HARVEST_TRIGGER_FRAC=1.25
export HARVEST_MIN_MARK=0.90
export HARVEST_COOLDOWN_SEC=300
export SOFT_SPIKE_TP=0.97
export SPIKE_FADE=1
export SPIKE_PEAK=0.93
export SPIKE_GIVEBACK=0.06
export SPIKE_MIN_GAIN=0.03
# Fat 70–90¢ books; skip skinny rich ≥92¢
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.92
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=1.0
export MAX_CONCURRENT=6
export MAX_EXPOSURE_FRAC=0.75
# Core printers only — metals/SOL/NEAR off
export SERIES=KXBNB15M,KXXRP15M,KXETH15M,KXBTC15M
export SATELLITE_SERIES=KXDOGE15M
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
export PYTH_PRIMARY_SYMBOLS=
export PYTH_CONFIRM=1
export PYTH_HERMES=https://hermes.pyth.network
export SERIES_GOV=1
export SERIES_GOV_N=8
export SERIES_GOV_MIN_SAMPLE=5
export SERIES_GOV_COLD_NET=-4
export SERIES_GOV_COLD_MULT=0.5
export SERIES_GOV_ICE_NET=-9
export SERIES_GOV_ICE_MULT=0.25
export SERIES_GOV_HOT_WR=0.90
export SERIES_GOV_HOT_NET=3
export SERIES_GOV_HOT_MULT=1.15
export SETUP_GOV=1
export SETUP_GOV_N=20
export SETUP_GOV_MIN_SAMPLE=8
export SETUP_GOV_AXES=band,lead,phase
export SETUP_GOV_COLD_NET=-5
export SETUP_GOV_COLD_MULT=0.60
export SETUP_GOV_ICE_NET=-10
export SETUP_GOV_ICE_MULT=0.35
export SETUP_GOV_HOT_WR=0.90
export SETUP_GOV_HOT_NET=4
export SETUP_GOV_HOT_MULT=1.20
export SETUP_GOV_MIN_MULT=0.35
export SETUP_GOV_MAX_MULT=1.20
# Soft/mid can trade (size cut when iced); never hard-skip overnight
export SETUP_GOV_BLOCK_ICE=0
export SETUP_GOV_BLOCK_ICE_AXES=band
export SETUP_GOV_EDGE_EXCLUDE_ICED=1
# Nuke ingredient: lead_flat was "hot" off TP sample — never hot-boost flat
export SETUP_GOV_NO_HOT_KEYS=lead_flat
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
# Soft was the settle-bleed — keep concurrent softs tight
export SOFT_CORR_MAX=2
export STAGE_SIZE=1
export STAGE_SIZE_10M_MULT=0.75
export STAGE_SIZE_5M_MULT=0.85
export EARLY_WINDOW_SEC=720
export EARLY_SIZE_MULT=1.20
export LATE_WINDOW_SEC=180
export LATE_RICH_ENTRY=0.88
export PRIOR_DIR_BIAS=0
export PRIOR_DIR_AGREE_MULT=1.10
export PRIOR_DIR_DISAGREE_MULT=0.50
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.40
# Soft still requires lead agree
export SOFT_BN_FLAT_MULT=0
# Stack cap — nuke hit 1.65
export MAX_SIZE_MULT=1.25
export LOSS_COOLDOWN_LOSSES=2
export LOSS_COOLDOWN_SEC=1200
export LOSS_COOLDOWN_RISK_MULT=0.40
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

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
