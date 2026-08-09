#!/usr/bin/env bash
# Mid-band EV printer — larger returns at ~50–70% WR.
#
# Thesis (book-proven shape):
#   Buy 45–65¢ favorites with lead edge, bank TP / pre-settle,
#   skip skinny rich chalk ≥70¢ (high WR, low EV).
#   Soft BN flat half-size; ticket cap on; no settle-ride nukes.
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

# Unhalt + reanchor HW for this leg
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
hw = float(st.get("high_water") or 0)
if hw > eq + 1e-9:
    st["high_water"] = eq
    changed = True
    print(f"midband deploy: reanchor HW ${hw:.2f} -> ${eq:.2f}")
if changed:
    p.write_text(json.dumps(st, indent=2))
print(f"midband deploy: trading (cash=${cash:.2f} equity=${eq:.2f})")
PY
rm -f bot/PAUSED.flag bot/SAVE_BANKROLL.flag bot/profit_target_hit.flag

export MODE=live
export START_EQUITY=20
export EDGE_SIZING=1
export RISK_FRACTION=0.20
export RISK_FRAC_MIN=0.15
export RISK_FRAC_MAX=0.25
export EDGE_KELLY_FRAC=0.35
export EDGE_LOOKBACK=20
export EDGE_PNL_CLIP=20
export EDGE_PRIOR_STRENGTH=16
export EDGE_PRIOR_WR=0.60
# Floor under ~$50–70 book; no trail / cash sprint
export HALT_DISABLED=0
export HALT_FLOOR=30
export HALT_TRAIL_FRAC=0
export HALT_EQUITY_FRAC=0
export HALT_LOSS_BUFFER=1
export HALT_PROFIT=0
export HALT_CASH_TARGET=0
export HALT_CONFIRM_POLLS=2
export STOP_LOSS_PCT=0
export LOGNORMAL_GATE=0
# BANK the edge — don't ride soft mid-band to binary settle
export TAKE_PROFIT_ABS=0.92
export TAKE_PROFIT_MULT=0
export TAKE_PROFIT_CAP=0.97
export TAKE_PROFIT_MIN_ENTRY=0
export SOFT_SPIKE_TP=0.88
export SPIKE_FADE=1
export SPIKE_PEAK=0.88
export SPIKE_GIVEBACK=0.05
export SPIKE_MIN_GAIN=0.04
export PRE_SETTLE_EXIT_SECS=75
export PRE_SETTLE_MAX_ENTRY=0.70
export EQUITY_HARVEST=0
# MID-BAND ONLY — the EV window for 50–70% WR
export PRICE_LO=0.45
export PRICE_HI=0.70
export SKIP_ENTRY_RICH=0.70
export MAX_SPREAD=0.18
export WINDOW_SEC=840
export MIN_SECS_LEFT=30
export MAX_SECS_LEFT=0
export CONFIRM_POLLS=1
export POLL_SEC=1.25
export MAX_CONCURRENT=4
export MAX_EXPOSURE_FRAC=0.60
# Core printers (keep universe tight while testing mid-band)
export SERIES=KXBNB15M,KXXRP15M,KXBTC15M
export SATELLITE_SERIES=KXSOL15M,KXETH15M
export SATELLITE_SIZE_MULT=0.5
export METALS_SERIES=
export METALS_SESSION=0
export SERIES_GOV=0
export SETUP_GOV=0
# Entire band is "soft" vs old 85¢ definition — size full inside band;
# SOFT_ENTRY_MAX just above PRICE_HI so BN gates still apply
export SOFT_ENTRY_MAX=0.70
export SOFT_ENTRY_SIZE_MULT=1.0
export SOFT_ENTRY_EARLY_SECS=360
export SOFT_ENTRY_EARLY_MULT=0.75
export SOFT_CORR_MAX=2
export STAGE_SIZE=1
export STAGE_SIZE_10M_MULT=0.65
export STAGE_SIZE_5M_MULT=0.85
export SOFT_BINANCE_STRICT=1
export SOFT_BN_AGREE_MULT=1.30
export SOFT_BN_FLAT_MULT=0.50
export MAX_SIZE_MULT=1.25
export TICKET_COST_CAP_FRAC=0.18
export LOSS_COOLDOWN_LOSSES=2
export LOSS_COOLDOWN_SEC=600
export LOSS_COOLDOWN_RISK_MULT=0.55
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
