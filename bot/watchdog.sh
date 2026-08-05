#!/usr/bin/env bash
# Keep favorite-maker + early-tip alive until manually stopped.
# Does NOT restart a process that is merely halted (settling) — only if PID gone.
set -u
cd /workspace
LOG=bot/watchdog.log
mkdir -p bot

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

ensure_tmux() {
  local name="$1" cmd="$2"
  if ! tmux -f /exec-daemon/tmux.portal.conf has-session -t "=$name" 2>/dev/null; then
    tmux -f /exec-daemon/tmux.portal.conf new-session -d -s "$name" -c /workspace -- "${SHELL:-bash}" -l
    sleep 0.3
  fi
  # If the python child is missing, start the command in that session.
  if ! pgrep -f "$3" >/dev/null 2>&1; then
    log "RESTART $name → $cmd"
    tmux -f /exec-daemon/tmux.portal.conf send-keys -t "$name" C-c
    sleep 0.4
    tmux -f /exec-daemon/tmux.portal.conf send-keys -t "$name" "$cmd" C-m
  fi
}

log "watchdog up — keep running until stop"
while true; do
  ensure_tmux kalshi-live \
    'bash bot/start_live.sh 2>&1 | tee -a bot/runner_live.log' \
    'python3 -u bot/runner.py'

  ensure_tmux kalshi-early \
    'bash bot/start_early_live.sh 2>&1 | tee -a bot/early_tip_live.log' \
    'python3 -u bot/early_tip_live.py'

  ensure_tmux kalshi-observer \
    'set -a; source secrets/env.sh; set +a; python3 -u bot/early_tip_observer.py 2>&1 | tee -a bot/observer.log' \
    'python3 -u bot/early_tip_observer.py'

  sleep 30
done
