#!/usr/bin/env bash
# Hard restart the full live stack (runner + watchdog + keep_alive + extmon).
# Use after freezes, bad deploys, or when the user says "restart the engine".
set -euo pipefail
cd /workspace
TMUX_CFG=/exec-daemon/tmux.portal.conf
LOG=bot/restart_engine.log

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

kill_exact_python() {
  local frag="$1"
  python3 - <<'PY' "$frag"
import os, signal, sys
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
        os.kill(int(pid), signal.SIGKILL)
        print(pid)
PY
}

kill_bash_script() {
  local script="$1"
  pgrep -f "bash ${script}" | while read -r pid; do
    kill -9 "$pid" 2>/dev/null || true
    echo "$pid"
  done
}

ensure_tmux() {
  local name="$1"
  if ! tmux -f "$TMUX_CFG" has-session -t "=$name" 2>/dev/null; then
    tmux -f "$TMUX_CFG" new-session -d -s "$name" -c /workspace -- "${SHELL:-bash}" -l
  fi
}

log "=== FULL ENGINE RESTART ==="
rm -f bot/PAUSED.flag bot/SAVE_BANKROLL.flag bot/profit_target_hit.flag
# Clear prior halt locks so a fresh climb can run
python3 - <<'PY' || true
import json
from pathlib import Path
p = Path("bot/state_live.json")
if p.exists():
    st = json.loads(p.read_text())
    if st.get("halted") or st.get("halt_reason"):
        st["halted"] = False
        st["halt_reason"] = ""
        p.write_text(json.dumps(st, indent=2))
        print("cleared halted/halt_reason for fresh run")
PY

log "stopping keep_alive / watchdog / runner / extmon"
kill_bash_script "bot/keep_alive.sh" || true
kill_bash_script "bot/watchdog.sh" || true
kill_exact_python "bot/external_monitor.py" || true
kill_exact_python "bot/runner.py" || true
sleep 1
# second pass
kill_bash_script "bot/keep_alive.sh" || true
kill_bash_script "bot/watchdog.sh" || true
kill_exact_python "bot/runner.py" || true
kill_exact_python "bot/external_monitor.py" || true
rm -f bot/runner.heartbeat bot/watchdog.heartbeat
sleep 1

for s in kalshi-keepalive kalshi-watchdog kalshi-live kalshi-extmon; do
  ensure_tmux "$s"
done

log "starting keep_alive (spawns watchdog + nudges runner + extmon)"
tmux -f "$TMUX_CFG" send-keys -t kalshi-keepalive C-c 2>/dev/null || true
sleep 0.3
tmux -f "$TMUX_CFG" send-keys -t kalshi-keepalive \
  'bash bot/keep_alive.sh 2>&1 | tee -a bot/keep_alive.log' C-m

# Direct runner start in parallel so we don't wait on watchdog alone
sleep 2
tmux -f "$TMUX_CFG" send-keys -t kalshi-live C-c 2>/dev/null || true
sleep 0.3
tmux -f "$TMUX_CFG" send-keys -t kalshi-live 'bash bot/start_live.sh' C-m

for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 2
  if pgrep -f 'python3 -u bot/runner.py' >/dev/null \
     && pgrep -f 'bash bot/watchdog.sh' >/dev/null \
     && pgrep -f 'bash bot/keep_alive.sh' >/dev/null; then
    log "OK stack up after ${i}*2s"
    pgrep -af 'keep_alive|watchdog.sh|runner.py|external_monitor' | grep -v pgrep || true
    exit 0
  fi
  log "waiting for stack... $i"
done
log "WARN stack incomplete — check tmux sessions"
pgrep -af 'keep_alive|watchdog|runner|external_monitor' | grep -v pgrep || true
exit 1
