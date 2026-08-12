#!/usr/bin/env bash
# Poll for Kalshi credentials, then unhalt + start the live stack toward $60.
# Sources (any one that materializes secrets/env.sh is enough):
#   - cloud-injected KALSHI_API_KEY_ID + KALSHI_PRIVATE_KEY
#   - pre-written secrets/env.sh + secrets/kalshi.key
set -euo pipefail
cd /workspace
LOG=bot/wait_secrets.log
TMUX_CFG=/exec-daemon/tmux.portal.conf

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "$LOG"; }

have_creds() {
  python3 -u bot/materialize_secrets.py >/dev/null 2>&1 || true
  if [[ -f secrets/env.sh && -f secrets/kalshi.key ]]; then
    return 0
  fi
  if [[ -n "${KALSHI_API_KEY_ID:-}" && -n "${KALSHI_PRIVATE_KEY:-}" ]]; then
    return 0
  fi
  if [[ -n "${KALSHI_API_KEY_ID:-}" && -f "${KALSHI_PRIVATE_KEY_PATH:-}" ]]; then
    return 0
  fi
  return 1
}

log "waiting for Kalshi credentials (cash-save target \$60)..."
for i in $(seq 1 720); do
  # Re-read process environment from /proc/1/environ if parent injected secrets later
  if [[ -r /proc/1/environ ]]; then
    while IFS= read -r -d '' kv; do
      case "$kv" in
        KALSHI_API_KEY_ID=*|KALSHI_PRIVATE_KEY=*|KALSHI_PRIVATE_KEY_PATH=*)
          export "$kv"
          ;;
      esac
    done < /proc/1/environ 2>/dev/null || true
  fi
  if have_creds; then
    log "credentials present — restarting engine (unhalt + HALT_CASH_TARGET=60)"
    bash bot/restart_engine.sh
    exit $?
  fi
  if (( i % 12 == 0 )); then
    log "still waiting (${i}/720 ~$((i*10/60))m) — add KALSHI_API_KEY_ID + KALSHI_PRIVATE_KEY"
  fi
  sleep 10
done
log "FATAL: timed out waiting for Kalshi credentials"
exit 1
