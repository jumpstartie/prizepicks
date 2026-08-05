#!/usr/bin/env bash
# Night-shift watchdog: keep favorite-maker powering through.
# CRITICAL: never block the restart loop on Kalshi API calls (timeout-wrapped).
# Touches bot/watchdog.heartbeat every cycle so keep_alive.sh can revive US.
set -u
cd /workspace
LOG=bot/watchdog.log
WD_HB=bot/watchdog.heartbeat
PAUSE_FLAG=bot/PAUSED.flag
STATE=bot/state_live.json
HB_FILE=bot/runner.heartbeat
RUNNER_LOG=bot/runner_live.log
TMUX_CFG=/exec-daemon/tmux.portal.conf
EARLY_WATCH="${EARLY_WATCH:-0}"
OBSERVER_WATCH="${OBSERVER_WATCH:-1}"
CHECK_SEC="${WATCHDOG_CHECK_SEC:-8}"
STALE_SEC="${WATCHDOG_STALE_SEC:-75}"
UNHALT_BUFFER="${WATCHDOG_UNHALT_BUFFER:-3}"
API_TIMEOUT="${WATCHDOG_API_TIMEOUT:-12}"
mkdir -p bot

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

touch_wd_hb() {
  # FIRST thing every loop — proves watchdog itself is alive
  date +%s.%N > "$WD_HB" 2>/dev/null || date +%s > "$WD_HB"
}

exact_python() {
  local frag="$1"
  python3 - <<'PY' "$frag"
import os, sys
frag = sys.argv[1]
for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue
    try:
        parts = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
    except Exception:
        continue
    args = [p.decode() for p in parts if p]
    if len(args) >= 3 and args[0].endswith("python3") and args[1] == "-u" and args[2] == frag:
        print(pid)
        break
PY
}

hb_age_sec() {
  python3 - <<'PY' "$HB_FILE" "$RUNNER_LOG"
import re, time, sys
from pathlib import Path
hb, logp = Path(sys.argv[1]), Path(sys.argv[2])
now = time.time()
if hb.exists():
    try:
        ts = float(hb.read_text().strip().split()[0])
        print(int(max(0, now - ts))); raise SystemExit
    except Exception:
        pass
if logp.exists():
    try:
        data = logp.read_bytes()[-8192:].decode(errors="ignore")
        matches = list(re.finditer(r"\[(\d{2}):(\d{2}):(\d{2})\]", data))
        if matches:
            import datetime as dt
            h, m, s = map(int, matches[-1].groups())
            today = dt.datetime.now()
            ts = today.replace(hour=h, minute=m, second=s, microsecond=0).timestamp()
            if ts - now > 3600:
                ts -= 86400
            print(int(max(0, now - ts))); raise SystemExit
    except Exception:
        pass
print(99999)
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
    tmux -f "$TMUX_CFG" send-keys -t "$name" C-c 2>/dev/null || true
    sleep 0.4
    tmux -f "$TMUX_CFG" send-keys -t "$name" "$cmd" C-m
    sleep 2
    pid=$(exact_python "$frag" || true)
    if [[ -z "${pid}" ]]; then
      log "WARN $name still down after restart"
    else
      log "OK $name pid=$pid"
    fi
  fi
}

maybe_kill_stale_runner() {
  local pid age
  pid=$(exact_python "bot/runner.py" || true)
  [[ -z "${pid}" ]] && return 0
  age=$(hb_age_sec)
  if [[ "$age" -ge "$STALE_SEC" ]]; then
    log "STALE runner pid=$pid heartbeat_age=${age}s ≥ ${STALE_SEC}s — force restart"
    kill -9 "$pid" 2>/dev/null || true
    sleep 0.5
    rm -f "$HB_FILE"
  fi
}

# API helpers MUST be timeout-wrapped — a hung Kalshi call froze us for ~7h.
maybe_unhalt() {
  timeout "$API_TIMEOUT" python3 - <<'PY' "$STATE" "$UNHALT_BUFFER" || echo "UNHALT_TIMEOUT"
import json, os, sys
from pathlib import Path
state_path = Path(sys.argv[1])
buf = float(sys.argv[2])
if not state_path.exists():
    raise SystemExit(0)
st = json.loads(state_path.read_text())
if not st.get("halted"):
    raise SystemExit(0)
floor = float(os.environ.get("HALT_FLOOR", "60"))
hw = float(st.get("high_water") or 0)
trail = float(os.environ.get("HALT_TRAIL_FRAC", "0.65"))
eff = max(floor, trail * hw) if hw > 0 else floor
cash = float(st.get("cash") or 0)
try:
    sys.path.insert(0, "/workspace")
    from bot.kalshi_client import KalshiClient
    c = KalshiClient()
    cash = float(c.balance().get("balance_dollars") or cash)
    pos = [p for p in c.get_positions()
           if abs(float(p.get("position_fp") or 0)) > 0 and "15M" in p.get("ticker", "")]
except Exception:
    pos = ["?"]
if pos:
    print(f"HALTED cash=${cash:.2f} floor=${eff:.2f} open={len(pos)} — wait flat")
    raise SystemExit(0)
if cash >= eff + buf:
    st["halted"] = False
    if hw > cash * 1.15:
        st["high_water"] = cash
        print(f"UNHALT cash=${cash:.2f} — cleared + HW→${cash:.2f}")
    else:
        print(f"UNHALT cash=${cash:.2f} floor=${eff:.2f}")
    state_path.write_text(json.dumps(st, indent=2))
else:
    print(f"HALTED cash=${cash:.2f} < ${eff+buf:.2f}")
PY
}

heartbeat() {
  timeout "$API_TIMEOUT" python3 - <<'PY' "$STATE" || echo "HB_TIMEOUT"
import json, sys
from pathlib import Path
try:
    sys.path.insert(0, "/workspace")
    from bot.kalshi_client import KalshiClient
    c = KalshiClient()
    b = c.balance()
    cash = float(b.get("balance_dollars") or 0)
    pv = b.get("portfolio_value")
    pos = [p for p in c.get_positions()
           if abs(float(p.get("position_fp") or 0)) > 0 and "15M" in p.get("ticker", "")]
    err = None
except Exception as e:
    cash = -1; pv = "?"; pos = []; err = e
st = {}
p = Path(sys.argv[1])
if p.exists():
    st = json.loads(p.read_text())
msg = f"HB cash=${cash:.2f} pv={pv} open={len(pos)} halted={st.get('halted')} hw={st.get('high_water')}"
if err:
    msg += f" err={err}"
print(msg)
PY
}

rm -f "$PAUSE_FLAG"
log "watchdog up check=${CHECK_SEC}s stale=${STALE_SEC}s api_timeout=${API_TIMEOUT}s early=${EARLY_WATCH}"
export HALT_FLOOR="${HALT_FLOOR:-60}"
export HALT_TRAIL_FRAC="${HALT_TRAIL_FRAC:-0.65}"

while true; do
  touch_wd_hb

  if [[ -f "$PAUSE_FLAG" ]]; then
    log "PAUSED — rm $PAUSE_FLAG to resume"
    sleep "$CHECK_SEC"
    continue
  fi

  # Restarts FIRST (never wait on API before ensuring runner lives)
  maybe_kill_stale_runner
  ensure_tmux kalshi-live 'bash bot/start_live.sh' 'bot/runner.py'

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

  out=$(maybe_unhalt 2>&1 || true)
  [[ -n "$out" && "$out" != "" ]] && log "$out"

  age=$(hb_age_sec)
  log "$(heartbeat 2>&1 || true) runner_hb_age=${age}s"
  touch_wd_hb
  sleep "$CHECK_SEC"
done
