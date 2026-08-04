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
# RATCHET: press Kelly while hot; trailing floor locks gains as HW climbs
export RISK_FRAC_MAX=0.30
export EDGE_KELLY_FRAC=0.40
# Overnight compound: shorter edge window + clip the -$88 outlier so Kelly
# can press again instead of staying stuck on cut_neg_edge @13%.
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=20
# Hard ticket cost cap — the 101-contract ETH nuke must not repeat
export TICKET_COST_CAP_FRAC=0.28
# Static floor is the launch pad; 0.70×HW ratchet takes over as book grows
export HALT_FLOOR=95
# Trailing floor: ratchets to 70% of realized (flat) high-water — protection
# grows with the book but always leaves ~30% drawdown room to keep trading
export HALT_TRAIL_FRAC=0.70
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export STOP_LOSS_PCT=0
export TAKE_PROFIT_ABS=0.98
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
# Soft/mid favorites (<88¢) ride to settle; TP only on richer entries
export TAKE_PROFIT_MIN_ENTRY=0.88
# Whale harvest: marked-equity spike ≥1.25× flat baseline → sell winners ≥90¢
# into strength, so the trailing floor ratchets on spikes instead of missing them
export EQUITY_HARVEST=1
export HARVEST_TRIGGER_FRAC=1.25
export HARVEST_MIN_MARK=0.90
export HARVEST_COOLDOWN_SEC=300
# But lock near-certain soft spikes at 97¢, and sell if a ≥93¢ peak fades 6¢+
export SOFT_SPIKE_TP=0.97
export SPIKE_FADE=1
export SPIKE_PEAK=0.93
export SPIKE_GIVEBACK=0.06
export SPIKE_MIN_GAIN=0.03
# RATCHET band: soft 70–85¢ back on, but ONLY with lead agreement —
# every big loser today was soft + bn=flat; those stay blocked below.
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
# Core = day-1 printers (ETH/XRP/BNB + BTC). No metals — gold/silver drained the book.
export SERIES=KXBNB15M,KXXRP15M,KXETH15M,KXBTC15M
# Satellites: DOGE only (SOL/NEAR/metals removed)
export SATELLITE_SERIES=KXDOGE15M
export SATELLITE_SIZE_MULT=0.5
# Metals sleeve OFF — keep empty so runner ignores KXGOLD/KXSILVER
export METALS_SERIES=
export METALS_SESSION=0
export PYTH_PRIMARY_SYMBOLS=
# Pyth still votes on crypto soft confirms
export PYTH_CONFIRM=1
export PYTH_HERMES=https://hermes.pyth.network
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
# Quant notch: setup-level size from recent band/lead/phase/asset performance
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
export SETUP_GOV_HOT_MULT=1.30
export SETUP_GOV_MIN_MULT=0.35
export SETUP_GOV_MAX_MULT=1.45
# Overnight: do NOT hard-skip iced soft/mid — ice mult still cuts size ×0.35,
# but hard-block was starving the book of the exact pocket that compounded to ~$190.
export SETUP_GOV_BLOCK_ICE=0
export SETUP_GOV_BLOCK_ICE_AXES=band
export SETUP_GOV_EDGE_EXCLUDE_ICED=1
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
# 0 = soft entries REQUIRE lead agreement (flat tape soft was the bleed)
export SOFT_BN_FLAT_MULT=0
# Stack cap: room for hot setup × BN agree without going nuclear
export MAX_SIZE_MULT=1.65
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
# Pyth/Hermes also votes on crypto soft confirms (metals use it as primary above)
# PYTH_CONFIRM already set with METALS_* block

exec python3 -u bot/runner.py >> bot/runner_live.log 2>&1
