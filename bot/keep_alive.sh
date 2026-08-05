#!/usr/bin/env bash
# Outer supervisor: if watchdog itself freezes/dies, revive it.
# This is why you shouldn't have to keep saying "keep it running".
set -u
cd /workspace
LOG=bot/keep_alive.log
WD_HB=bot/watchdog.heartbeat
TMUX_CFG=/exec-daemon/tmux.portal.conf
CHECK_SEC="${KEEPALIVE_CHECK_SEC:-20}"
WD_STALE_SEC="${KEEPALIVE_WD_STALE_SEC:-60}"
mkdir -p bot

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

wd_age() {
  python3 - <<'PY' "$WD_HB"
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

wd_pid() {
  pgrep -f 'bash bot/watchdog.sh' | head -1 || true
}

start_watchdog() {
  if ! tmux -f "$TMUX_CFG" has-session -t '=kalshi-watchdog' 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s kalshi-watchdog -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  # kill any stuck watchdog
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

log "keep_alive up check=${CHECK_SEC}s wd_stale=${WD_STALE_SEC}s"
start_watchdog
start_external_monitor

while true; do
  rm -f bot/PAUSED.flag
  age=$(wd_age)
  pid=$(wd_pid)
  if [[ -z "${pid}" || "$age" -ge "$WD_STALE_SEC" ]]; then
    log "WATCHDOG down/stale pid=${pid:-none} age=${age}s — respawn"
    start_watchdog
  fi
  # Also ensure runner exists (belt + suspenders)
  if ! pgrep -f 'python3 -u bot/runner.py' >/dev/null 2>&1; then
    log "runner missing — nudging live session"
    tmux -f "$TMUX_CFG" has-session -t '=kalshi-live' 2>/dev/null || \
      tmux -f "$TMUX_CFG" new-session -d -s kalshi-live -c /workspace -- "${SHELL:-bash}" -l
    tmux -f "$TMUX_CFG" send-keys -t kalshi-live C-c 2>/dev/null || true
    sleep 0.3
    tmux -f "$TMUX_CFG" send-keys -t kalshi-live 'bash bot/start_live.sh' C-m
  fi
  start_external_monitor
  sleep "$CHECK_SEC"
done
