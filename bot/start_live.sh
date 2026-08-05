#!/usr/bin/env bash
# RTP-20 + 80% merge — printer exits + lognormal/venue/time gates.
#
# EVIDENCE (live book):
#   core flat + TP/fade     → +$183 @ 100% WR   (THE printer)
#   soft/mid + flat + settle → −$266            (THE nuke)
#   cost ≥ $15 tickets      → −$41             (size tails)
#   agree-only (no flat)    → only 19 trades   (starves streak)
#   setup_gov / ETH / SOL / metals → expectancy killers
#
# MERGE (80%+ WR intent):
#   • Keep RTP-20 exits (TP / fade / pre-settle) + core + 15% ticket
#   • Lognormal digital gate: model_prob≥0.65 & edge≥0.03
#   • Confirm≥2 · secs_left ∈ [180,780] · favorites that model also likes
#   • Flat still allowed at ×0.50 (printer fuel); disagree still blocked
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
export RISK_FRAC_MIN=0.15
export RISK_FRAC_MAX=0.24
export EDGE_KELLY_FRAC=0.35
export EDGE_LOOKBACK=12
export EDGE_PNL_CLIP=12
export EDGE_PRIOR_STRENGTH=20
export EDGE_PRIOR_WR=0.93
# Static pad under ~$57–65 book; trail locks gains once HW climbs on flat cash
export HALT_FLOOR=42
export HALT_TRAIL_FRAC=0.65
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# BANK — the whole edge vs settle
export TAKE_PROFIT_ABS=0.97
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.99
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.95
export SPIKE_FADE=1
export SPIKE_PEAK=0.92
export SPIKE_GIVEBACK=0.05
export SPIKE_MIN_GAIN=0.03
# Never binary-settle the soft/mid band
export PRE_SETTLE_EXIT_SECS=60
export PRE_SETTLE_MAX_ENTRY=0.95
export EQUITY_HARVEST=0
# Fat 70–94¢ books; skip skinny ≥95¢
export PRICE_LO=0.70
export PRICE_HI=0.999
export SKIP_ENTRY_RICH=0.95
export MAX_SPREAD=0.18
export WINDOW_SEC=840
# 80% merge: mid-window favorites only (3–13m left)
export MIN_SECS_LEFT=180
export MAX_SECS_LEFT=780
export CONFIRM_POLLS=2
export POLL_SEC=1.25
# Driftless lognormal digital — favorites the model also likes
export LOGNORMAL_GATE=1
export LOGNORMAL_MIN_EDGE=0.03
export LOGNORMAL_MIN_PROB=0.65
export LOGNORMAL_SIGMA_MODE=realized
export LOGNORMAL_SIGMA=0.80
export LOGNORMAL_SIGMA_FLOOR=0.40
export LOGNORMAL_STRICT=0
# Keep flat×0.50 printer path; do not require hard venue agree (starves)
export LOGNORMAL_REQUIRE_AGREE=0
export MAX_CONCURRENT=3
export MAX_EXPOSURE_FRAC=0.60
export SERIES=KXBNB15M,KXXRP15M,KXBTC15M
export SATELLITE_SERIES=
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
export SERIES_GOV=0
export SETUP_GOV=0
# BN gate on all tradable (<95¢) so 91–92¢ can't bypass
export SOFT_ENTRY_MAX=0.95
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=300
export SOFT_ENTRY_EARLY_MULT=1.0
export SOFT_CORR_MAX=2
export STAGE_SIZE=0
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.20
# ALLOW flat at half size — counterfactual printer; pre-settle blocks the nuke
export SOFT_BN_FLAT_MULT=0.50
export MAX_SIZE_MULT=1.20
# Size tails (cost≥$15) were net negative — hard cap
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
