#!/usr/bin/env bash
# Strategy #3 — OG day-1 printer (restored for today).
#
# What printed the $44+ / ~20–0 / 52-streak day-1 path:
#   70¢+ favorites, 14m window, TP into 99¢,
#   BNB/SOL/XRP/ETH core + BTC/DOGE satellites, Binance lead filter,
#   soft favorites FULL size, BN flat half-size (not zero).
#
# Complexity that nuked the book later stays OFF:
#   setup_gov hot stacks, metals, early-tip FORCE, lognormal gate,
#   pre-settle / spike-fade overlays, cash-sprint save locks.
# Ticket cost cap kept as the one hard lesson.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

# Unhalt + reanchor HW for today's #3 leg (no cash-save lock)
python3 - <<'PY'
import json
from pathlib import Path
p = Path("bot/state_live.json")
if not p.exists():
    raise SystemExit(0)
st = json.loads(p.read_text())
cash = float(st.get("cash") or 0)
eq = float(st.get("equity") or cash)
changed = False
if st.get("halted"):
    st["halted"] = False
    st["halt_reason"] = ""
    changed = True
# Reanchor high-water so an old peak can't trail-lock mid-leg
hw = float(st.get("high_water") or 0)
if hw > eq + 1e-9:
    st["high_water"] = eq
    changed = True
    print(f"og3 deploy: reanchor HW ${hw:.2f} -> ${eq:.2f}")
if changed:
    p.write_text(json.dumps(st, indent=2))
print(f"og3 deploy: trading (cash=${cash:.2f} equity=${eq:.2f})")
PY
rm -f bot/PAUSED.flag bot/SAVE_BANKROLL.flag bot/profit_target_hit.flag

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
export RISK_FRACTION=0.18
export RISK_FRAC_MIN=0.13
export RISK_FRAC_MAX=0.25
export EDGE_KELLY_FRAC=0.33
export EDGE_LOOKBACK=30
export EDGE_PNL_CLIP=25
# Floor under today's ~$40 book (OG used $55 under ~$81); no trail / cash sprint
export HALT_DISABLED=0
export HALT_FLOOR=25
export HALT_TRAIL_FRAC=0
export HALT_EQUITY_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CASH_TARGET=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
# OG overlays OFF — pure #3 exits
export LOGNORMAL_GATE=0
export PRE_SETTLE_EXIT_SECS=0
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
export MAX_SECS_LEFT=0
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
