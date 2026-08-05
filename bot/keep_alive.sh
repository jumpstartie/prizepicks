#!/usr/bin/env bash
# Outer supervisor: revive watchdog + runner even after VM sleep / freezes.
# Cursor cloud VMs suspend when idle — wall-clock jumps are the smoking gun.
set -u
cd /workspace
LOG=bot/keep_alive.log
WD_HB=bot/watchdog.heartbeat
RUN_HB=bot/runner.heartbeat
TMUX_CFG=/exec-daemon/tmux.portal.conf
CHECK_SEC="${KEEPALIVE_CHECK_SEC:-15}"
WD_STALE_SEC="${KEEPALIVE_WD_STALE_SEC:-45}"
RUN_STALE_SEC="${KEEPALIVE_RUN_STALE_SEC:-90}"
# If wall clock advances more than this between loops, we slept/froze.
JUMP_SEC="${KEEPALIVE_JUMP_SEC:-90}"
mkdir -p bot

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

hb_age() {
  python3 - <<'PY' "$1"
import time, sys
from pathlib import Path
p = Path(sys.argv[1])
if not p.exists():
    print(99999); raise SystemExit
try:
    ts = float(p.read_text().strip().split()[0])
    print(int(max(0, time.time() - ts)))
except Exception:
    print(99999)
PY
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

wd_pid() {
  pgrep -f 'bash bot/watchdog.sh' | head -1 || true
}

kill_runner() {
  local pid
  pid=$(exact_python "bot/runner.py" || true)
  if [[ -n "${pid}" ]]; then
    log "KILL runner pid=$pid"
    kill -9 "$pid" 2>/dev/null || true
    sleep 0.4
  fi
  rm -f "$RUN_HB"
}

start_watchdog() {
  if ! tmux -f "$TMUX_CFG" has-session -t '=kalshi-watchdog' 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s kalshi-watchdog -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  local pid
  pid=$(wd_pid)
  if [[ -n "${pid}" ]]; then
    kill -9 "$pid" 2>/dev/null || true
    sleep 0.5
  fi
  rm -f bot/PAUSED.flag
  tmux -f "$TMUX_CFG" send-keys -t kalshi-watchdog C-c 2>/dev/null || true
  sleep 0.3
  tmux -f "$TMUX_CFG" send-keys -t kalshi-watchdog \
    'EARLY_WATCH=0 OBSERVER_WATCH=1 bash bot/watchdog.sh' C-m
  log "started watchdog"
}

start_runner() {
  if ! tmux -f "$TMUX_CFG" has-session -t '=kalshi-live' 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s kalshi-live -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  tmux -f "$TMUX_CFG" send-keys -t kalshi-live C-c 2>/dev/null || true
  sleep 0.3
  tmux -f "$TMUX_CFG" send-keys -t kalshi-live 'bash bot/start_live.sh' C-m
  log "started runner via start_live.sh"
}

start_external_monitor() {
  if ! tmux -f "$TMUX_CFG" has-session -t '=kalshi-extmon' 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s kalshi-extmon -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  if ! pgrep -f 'python3 -u bot/external_monitor.py' >/dev/null 2>&1; then
    log "RESTART external monitor"
    tmux -f "$TMUX_CFG" send-keys -t kalshi-extmon C-c 2>/dev/null || true
    sleep 0.3
    tmux -f "$TMUX_CFG" send-keys -t kalshi-extmon \
      'bash bot/start_external_monitor.sh 2>&1 | tee -a bot/external_monitor.log' C-m
  fi
}

freeze_recover() {
  local jump="$1"
  log "FREEZE RECOVERY wall_jump=${jump}s — hard restart runner+watchdog"
  kill_runner
  start_watchdog
  sleep 1
  # watchdog will also start runner; nudge immediately
  if [[ -z "$(exact_python bot/runner.py || true)" ]]; then
    start_runner
  fi
}

log "keep_alive up check=${CHECK_SEC}s wd_stale=${WD_STALE_SEC}s run_stale=${RUN_STALE_SEC}s jump=${JUMP_SEC}s"
start_watchdog
start_external_monitor
LAST_WALL=$(date +%s)

while true; do
  rm -f bot/PAUSED.flag
  NOW=$(date +%s)
  JUMP=$((NOW - LAST_WALL))
  if [[ "$JUMP" -ge "$JUMP_SEC" ]]; then
    freeze_recover "$JUMP"
    LAST_WALL=$(date +%s)
    sleep "$CHECK_SEC"
    continue
  fi
  LAST_WALL=$NOW

  age=$(hb_age "$WD_HB")
  pid=$(wd_pid)
  if [[ -z "${pid}" || "$age" -ge "$WD_STALE_SEC" ]]; then
    log "WATCHDOG down/stale pid=${pid:-none} age=${age}s — respawn"
    start_watchdog
  fi

  # Belt+suspenders: keep_alive watches runner HB itself (don't trust watchdog alone)
  run_pid=$(exact_python "bot/runner.py" || true)
  run_age=$(hb_age "$RUN_HB")
  if [[ -z "${run_pid}" ]]; then
    log "runner missing — starting"
    start_runner
  elif [[ "$run_age" -ge "$RUN_STALE_SEC" ]]; then
    log "STALE runner pid=${run_pid} hb_age=${run_age}s — force restart"
    kill_runner
    start_runner
  fi

  start_external_monitor
  sleep "$CHECK_SEC"
done
