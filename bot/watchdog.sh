#!/usr/bin/env bash
# Night-shift watchdog: keep favorite-maker powering through.
# - Respects bot/PAUSED.flag (no restarts while paused)
# - Restarts dead PIDs every 10s
# - Auto-unhalts when flat + cash above floor+buffer (halt was the overnight "break")
# - Early-tip optional (EARLY_WATCH=0 by default overnight)
# - Heartbeats cash/halt/open to bot/watchdog.log
set -u
cd /workspace
LOG=bot/watchdog.log
PAUSE_FLAG=bot/PAUSED.flag
STATE=bot/state_live.json
TMUX_CFG=/exec-daemon/tmux.portal.conf
EARLY_WATCH="${EARLY_WATCH:-0}"
OBSERVER_WATCH="${OBSERVER_WATCH:-1}"
CHECK_SEC="${WATCHDOG_CHECK_SEC:-10}"
UNHALT_BUFFER="${WATCHDOG_UNHALT_BUFFER:-3}"   # cash must clear floor by this
mkdir -p bot

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

exact_python() {
  # $1 = script path fragment e.g. bot/runner.py
  python3 - <<'PY' "$1"
import os, sys
frag = sys.argv[1]
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        parts = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
    except Exception:
        continue
    if len(parts) >= 2 and parts[0].endswith(b"python3") and frag.encode() in b" ".join(parts):
        # exact: python3 -u bot/runner.py
        args = [p.decode() for p in parts if p]
        if args[:3] == ["python3", "-u", frag] or (len(args) >= 2 and args[0].endswith("python3") and frag in args):
            print(pid)
            break
PY
}

ensure_tmux() {
  local name="$1" cmd="$2" frag="$3"
  if [[ -f "$PAUSE_FLAG" ]]; then
    return 0
  fi
  if ! tmux -f "$TMUX_CFG" has-session -t "=$name" 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s "$name" -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  local pid
  pid=$(exact_python "$frag" || true)
  if [[ -z "${pid}" ]]; then
    log "RESTART $name (no PID for $frag)"
    tmux -f "$TMUX_CFG" send-keys -t "$name" C-c
    sleep 0.5
    tmux -f "$TMUX_CFG" send-keys -t "$name" "$cmd" C-m
    sleep 1.5
    pid=$(exact_python "$frag" || true)
    if [[ -z "${pid}" ]]; then
      log "WARN $name still down after restart"
    else
      log "OK $name pid=$pid"
    fi
  fi
}

maybe_unhalt() {
  # If favorite-maker is halted but cash recovered above floor, clear halt so
  # the night shift keeps trading instead of "settling only" forever.
  python3 - <<'PY' "$STATE" "$UNHALT_BUFFER"
import json, os, sys
from pathlib import Path
state_path = Path(sys.argv[1])
buf = float(sys.argv[2])
if not state_path.exists():
    raise SystemExit(0)
st = json.loads(state_path.read_text())
if not st.get("halted"):
    raise SystemExit(0)
# floor from env if present else state/static
floor = float(os.environ.get("HALT_FLOOR", "60"))
hw = float(st.get("high_water") or 0)
trail = float(os.environ.get("HALT_TRAIL_FRAC", "0.65"))
eff = max(floor, trail * hw) if hw > 0 else floor
cash = float(st.get("cash") or 0)
# live balance preferred
try:
    sys.path.insert(0, "/workspace")
    from bot.kalshi_client import KalshiClient
    b = KalshiClient().balance()
    cash = float(b.get("balance_dollars") or cash)
    pos = [p for p in KalshiClient().get_positions()
           if abs(float(p.get("position_fp") or 0)) > 0 and "15M" in p.get("ticker", "")]
except Exception:
    pos = ["?"]
if pos:
    print(f"HALTED cash=${cash:.2f} floor=${eff:.2f} open={len(pos)} — wait flat")
    raise SystemExit(0)
if cash >= eff + buf:
    st["halted"] = False
    # Re-anchor HW to cash so a stale ATH trail floor can't re-halt instantly
    if hw > cash * 1.15:
        st["high_water"] = cash
        print(f"UNHALT cash=${cash:.2f} floor=${eff:.2f} — cleared halt + reanchor HW ${hw:.2f}→${cash:.2f}")
    else:
        print(f"UNHALT cash=${cash:.2f} floor=${eff:.2f} — cleared halt")
    state_path.write_text(json.dumps(st, indent=2))
else:
    print(f"HALTED cash=${cash:.2f} < floor+buf ${eff+buf:.2f} — stay halted")
PY
}

heartbeat() {
  python3 - <<'PY' "$STATE"
import json, sys
from pathlib import Path
try:
    sys.path.insert(0, "/workspace")
    from bot.kalshi_client import KalshiClient
    b = KalshiClient().balance()
    cash = float(b.get("balance_dollars") or 0)
    pv = b.get("portfolio_value")
    pos = [p for p in KalshiClient().get_positions()
           if abs(float(p.get("position_fp") or 0)) > 0 and "15M" in p.get("ticker", "")]
except Exception as e:
    cash = -1; pv = "?"; pos = []; err = e
else:
    err = None
st = {}
p = Path(sys.argv[1])
if p.exists():
    st = json.loads(p.read_text())
print(f"HB cash=${cash:.2f} pv={pv} open={len(pos)} halted={st.get('halted')} hw={st.get('high_water')}"
      + (f" err={err}" if err else ""))
PY
}

log "watchdog up check=${CHECK_SEC}s early=${EARLY_WATCH} observer=${OBSERVER_WATCH} pause_flag=$PAUSE_FLAG"
# Export floor knobs for unhalt helper (match start_live.sh)
export HALT_FLOOR="${HALT_FLOOR:-60}"
export HALT_TRAIL_FRAC="${HALT_TRAIL_FRAC:-0.65}"

while true; do
  if [[ -f "$PAUSE_FLAG" ]]; then
    log "PAUSED — not restarting (rm $PAUSE_FLAG to resume)"
    heartbeat || true
    sleep "$CHECK_SEC"
    continue
  fi

  # Unhalt before ensuring process so a live runner can trade again
  out=$(maybe_unhalt 2>&1 || true)
  [[ -n "$out" ]] && log "$out"

  ensure_tmux kalshi-live \
    'bash bot/start_live.sh' \
    'bot/runner.py'

  if [[ "$EARLY_WATCH" == "1" ]]; then
    ensure_tmux kalshi-early \
      'bash bot/start_early_live.sh 2>&1 | tee -a bot/early_tip_live.log' \
      'bot/early_tip_live.py'
  fi

  if [[ "$OBSERVER_WATCH" == "1" ]]; then
    ensure_tmux kalshi-observer \
      'set -a; source secrets/env.sh; set +a; python3 -u bot/early_tip_observer.py 2>&1 | tee -a bot/observer.log' \
      'bot/early_tip_observer.py'
  fi

  heartbeat || true
  sleep "$CHECK_SEC"
done
