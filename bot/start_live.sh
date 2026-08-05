#!/usr/bin/env bash
# RTP-20 printer replay — the pattern that 2×–8×’d the live book.
#
# EVIDENCE (live book):
#   core flat + TP/fade     → +$199 @ 100% WR   (THE printer)
#   $20 → $79 in 52-win streak; peak ~$161 (~8×)
#   soft/mid + flat + settle → −$263            (THE nuke)
#   lognormal 0.65/0.03 merge → 0 fills (starved)
#
# REPLAY:
#   • Core BNB/XRP/BTC · 70–94¢ · bn=flat ×0.50 allowed
#   • Bank: TP 97¢ / soft spike / fade / pre-settle @60s
#   • Ticket ≤15% · concurrent 3 · $20 floor stop
#   • Lognormal OFF · confirm=1 · full window (frequency)
#   • Governors / early-tip / metals / satellites OFF
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
# User risk box: hard stop at $20; trail locks climbs on flat cash
export HALT_FLOOR=20
export HALT_TRAIL_FRAC=0.65
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
# Lock the book once flat cash clears $105 (writes bot/SAVE_BANKROLL.flag)
export HALT_CASH_TARGET=105
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
# Printer frequency — day-1 style
export MIN_SECS_LEFT=25
export MAX_SECS_LEFT=0
export CONFIRM_POLLS=1
export POLL_SEC=1.25
# Lognormal overlay OFF (starved the printer)
export LOGNORMAL_GATE=0
export LOGNORMAL_MIN_EDGE=0.03
export LOGNORMAL_MIN_PROB=0.65
export LOGNORMAL_SIGMA_MODE=realized
export LOGNORMAL_SIGMA=0.80
export LOGNORMAL_SIGMA_FLOOR=0.40
export LOGNORMAL_STRICT=0
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
# ALLOW flat at half size — the 2× engine; pre-settle blocks the nuke
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
