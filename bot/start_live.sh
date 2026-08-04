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
# Raised from 70 after banking the morning run (protect ~$120 book)
export HALT_FLOOR=100
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
# Core = best WR names (ETH 28-0, XRP 94%, BNB 96%); SOL demoted after 4-5 −$17 chop
export SERIES=KXBNB15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M,KXSOL15M,KXDOGE15M,KXNEAR15M
export SATELLITE_SIZE_MULT=0.5
# Per-series safety governor: auto-cut cold series, boost hot ones
export SERIES_GOV=1
export SERIES_GOV_N=8
export SERIES_GOV_MIN_SAMPLE=5
export SERIES_GOV_COLD_NET=-4
export SERIES_GOV_COLD_MULT=0.5
export SERIES_GOV_ICE_NET=-9
export SERIES_GOV_ICE_MULT=0.25
export SERIES_GOV_HOT_WR=0.90
export SERIES_GOV_HOT_NET=3
export SERIES_GOV_HOT_MULT=1.25
export SOFT_ENTRY_MAX=0.85
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
# Soft corr was the #2 skip reason — allow one more soft favorite
export SOFT_CORR_MAX=3
# Stage only applies to soft <85¢ in code
export STAGE_SIZE=1
# Early tipped favorites were our best WR pocket — don't cut them in half
export STAGE_SIZE_10M_MULT=0.75
export STAGE_SIZE_5M_MULT=0.85
# Time-phase: boost first 3m soft+BN-agree; block late rich; prior-dir OFF (≈coinflip)
export EARLY_WINDOW_SEC=720
export EARLY_SIZE_MULT=1.25
export LATE_WINDOW_SEC=180
export LATE_RICH_ENTRY=0.88
export PRIOR_DIR_BIAS=0
export PRIOR_DIR_AGREE_MULT=1.10
export PRIOR_DIR_DISAGREE_MULT=0.50
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
# Multi-venue confirm: Binance + OKX + Kraken (+ Coinbase) — need ≥2 same-way for full soft size
export MULTI_VENUE=1
export MULTI_VENUE_MIN_AGREE=2
export MULTI_VENUE_WINDOW_SEC=4
export MULTI_VENUE_PCT=0.0003
export MULTI_VENUE_STRICT=0
export OKX_CONFIRM=1
export KRAKEN_CONFIRM=1

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
