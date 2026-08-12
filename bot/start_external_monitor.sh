#!/usr/bin/env bash
# External monitor — dead-man's switch + webhook alerts.
# Configure one (or more) in secrets/env.sh:
#   export HEALTHCHECKS_PING_URL='https://hc-ping.com/<uuid>'   # recommended
#   export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
#   export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
#   export NTFY_TOPIC='your-private-topic'   # phone: ntfy app subscribe
#   export MONITOR_WEBHOOK_URL='https://...'
set -euo pipefail
cd /workspace
set -a
# shellcheck disable=SC1091
source secrets/env.sh
set +a

export EXTMON_POLL_SEC="${EXTMON_POLL_SEC:-30}"
export EXTMON_RUNNER_STALE_SEC="${EXTMON_RUNNER_STALE_SEC:-90}"
export EXTMON_WD_STALE_SEC="${EXTMON_WD_STALE_SEC:-90}"
export EXTMON_HTTP_PORT="${EXTMON_HTTP_PORT:-9105}"

exec python3 -u bot/external_monitor.py
