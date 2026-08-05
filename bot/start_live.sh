#!/usr/bin/env bash
# Strategy #3 — morning sprint pack (keep OG skeleton, fix today's bleed).
# Diagnosis: every big morning loser was mid/soft + bn=flat held to settle
# (ETH −$18, BTC −$21, SOL −$10, DOGE −$7). Soft BN gate only covered
# <85¢ so 85–91¢ tickets skipped it. Kelly stuck on cut_neg_edge after
# those losses. Sprint: extend BN gate, block flat softs, bank winners,
# unstick size — governors / early-tip / metals stay OFF.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
# Unstick from cut_neg_edge: shorter lookback, clip nukes, stronger prior
export RISK_FRACTION=0.20
export RISK_FRAC_MIN=0.16
export RISK_FRAC_MAX=0.28
export EDGE_KELLY_FRAC=0.40
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=12
export EDGE_PRIOR_STRENGTH=20
export EDGE_PRIOR_WR=0.92
# Room under ~$65–72 book; no profit-halt
export HALT_FLOOR=50
export HALT_TRAIL_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# Bank winners earlier — settle was the morning drain, TP/fade printed
export TAKE_PROFIT_ABS=0.98
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.96
export SPIKE_FADE=1
export SPIKE_PEAK=0.93
export SPIKE_GIVEBACK=0.06
export SPIKE_MIN_GAIN=0.03
export EQUITY_HARVEST=0
# #3 band; skip skinny ≥95¢, press fatter mid books
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.95
export MAX_SPREAD=0.20
export WINDOW_SEC=840
export MIN_SECS_LEFT=15
export CONFIRM_POLLS=1
export POLL_SEC=1.25
export MAX_CONCURRENT=6
export MAX_EXPOSURE_FRAC=0.75
# Core printers; SOL demoted (just ate −$10); BTC/DOGE/SOL satellites
export SERIES=KXBNB15M,KXXRP15M,KXETH15M
export SATELLITE_SERIES=KXBTC15M,KXDOGE15M,KXSOL15M
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
# Governors OFF — hot stacks caused the nukes
export SERIES_GOV=0
export SETUP_GOV=0
# Extend soft BN gate through mid favorites (was 0.85 → ETH/BTC nukes skipped it)
export SOFT_ENTRY_MAX=0.92
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=3
# Full size on BN-agreed softs — don't stage-cut the printers
export STAGE_SIZE=0
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.25
# Block bn=flat soft/mid — every big morning loser
export SOFT_BN_FLAT_MULT=0
export MAX_SIZE_MULT=1.35
# Hard ticket ceiling
export TICKET_COST_CAP_FRAC=0.22
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
