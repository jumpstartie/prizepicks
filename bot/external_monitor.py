"""External monitoring for the Kalshi live stack.

Two layers:
  1. Local health → bot/health.json + optional :9105/healthz
  2. Dead-man's switch → ping HEALTHCHECKS_PING_URL / MONITOR_PING_URL every
     cycle when healthy. If this VM dies or the monitor dies, the EXTERNAL
     service (healthchecks.io, cronitor, betterstack, etc.) alerts you.

Optional push alerts on state change:
  DISCORD_WEBHOOK_URL / SLACK_WEBHOOK_URL / MONITOR_WEBHOOK_URL / NTFY_TOPIC

This process does not replace keep_alive/watchdog — it tells YOU when those fail.
"""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BOT = Path(__file__).resolve().parent
ROOT = BOT.parent
HEALTH_PATH = BOT / "health.json"
ALERT_LOG = BOT / "external_monitor.log"
RUNNER_HB = BOT / "runner.heartbeat"
WD_HB = BOT / "watchdog.heartbeat"
PAUSE_FLAG = BOT / "PAUSED.flag"
STATE = BOT / "state_live.json"

POLL_SEC = float(os.environ.get("EXTMON_POLL_SEC", "30"))
RUNNER_STALE = float(os.environ.get("EXTMON_RUNNER_STALE_SEC", "90"))
WD_STALE = float(os.environ.get("EXTMON_WD_STALE_SEC", "90"))
HTTP_PORT = int(os.environ.get("EXTMON_HTTP_PORT", "9105"))

PING_URL = (
    os.environ.get("HEALTHCHECKS_PING_URL", "").strip()
    or os.environ.get("MONITOR_PING_URL", "").strip()
)
PING_FAIL_SUFFIX = os.environ.get("HEALTHCHECKS_FAIL_SUFFIX", "/fail")

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
GENERIC_WEBHOOK = os.environ.get("MONITOR_WEBHOOK_URL", "").strip()
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "").strip()
NTFY_BASE = os.environ.get("NTFY_BASE", "https://ntfy.sh").rstrip("/")

_last_health: dict = {}
_last_status: str | None = None


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with ALERT_LOG.open("a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _cmdline(pid: str) -> list[str]:
    try:
        parts = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")
        return [p.decode(errors="replace") for p in parts if p]
    except Exception:
        return []


def runner_pids() -> list[int]:
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        args = _cmdline(pid)
        if len(args) >= 3 and args[0].endswith("python3") and args[1] == "-u" and args[2] == "bot/runner.py":
            out.append(int(pid))
    return out


def script_pids(script: str) -> list[int]:
    out = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        args = _cmdline(pid)
        joined = " ".join(args)
        if "extglob" in joined:
            continue
        if args and args[0].endswith("bash") and any(script in a for a in args):
            out.append(int(pid))
    return out


def _hb_age(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        ts = float(path.read_text().strip().split()[0])
        return max(0.0, time.time() - ts)
    except Exception:
        return None


def collect_health() -> dict:
    issues: list[str] = []
    r_pids = runner_pids()
    w_pids = script_pids("bot/watchdog.sh")
    k_pids = script_pids("bot/keep_alive.sh")
    runner_age = _hb_age(RUNNER_HB)
    wd_age = _hb_age(WD_HB)

    if not r_pids:
        issues.append("runner_process_missing")
    elif runner_age is None:
        issues.append("runner_heartbeat_missing")
    elif runner_age > RUNNER_STALE:
        issues.append(f"runner_heartbeat_stale_{int(runner_age)}s")

    if not w_pids:
        issues.append("watchdog_process_missing")
    elif wd_age is None:
        issues.append("watchdog_heartbeat_missing")
    elif wd_age > WD_STALE:
        issues.append(f"watchdog_heartbeat_stale_{int(wd_age)}s")

    if not k_pids:
        issues.append("keep_alive_process_missing")

    if PAUSE_FLAG.exists():
        issues.append("paused_flag_set")

    halted = False
    cash = None
    hw = None
    try:
        st = json.loads(STATE.read_text())
        halted = bool(st.get("halted"))
        cash = st.get("cash")
        hw = st.get("high_water")
        if halted:
            issues.append("runner_halted")
    except Exception:
        issues.append("state_unreadable")

    try:
        import sys
        sys.path.insert(0, str(ROOT))
        from bot.kalshi_client import KalshiClient
        cash = float(KalshiClient().balance().get("balance_dollars") or cash or 0)
    except Exception as e:
        issues.append(f"balance_error:{type(e).__name__}")

    status = "ok" if not issues else "down"
    return {
        "ts": now_iso(),
        "status": status,
        "ok": status == "ok",
        "issues": issues,
        "cash": cash,
        "high_water": hw,
        "halted": halted,
        "runner_pids": r_pids,
        "watchdog_pids": w_pids,
        "keep_alive_pids": k_pids,
        "runner_hb_age_s": None if runner_age is None else round(runner_age, 1),
        "watchdog_hb_age_s": None if wd_age is None else round(wd_age, 1),
        "ping_configured": bool(PING_URL),
        "webhook_configured": bool(
            DISCORD_WEBHOOK or SLACK_WEBHOOK or GENERIC_WEBHOOK or NTFY_TOPIC
        ),
    }


def _http_post(url: str, data: bytes, headers: dict, timeout: float = 10) -> None:
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        r.read()


def ping_success() -> None:
    if not PING_URL:
        return
    try:
        urllib.request.urlopen(PING_URL, timeout=10).read()
    except Exception as e:
        log(f"ping success error: {e}")


def ping_fail(reason: str) -> None:
    if not PING_URL:
        return
    try:
        fail_url = PING_URL.rstrip("/") + PING_FAIL_SUFFIX
        urllib.request.urlopen(fail_url, timeout=10).read()
    except Exception:
        try:
            _http_post(PING_URL, reason.encode()[:500], {"Content-Type": "text/plain"})
        except Exception as e:
            log(f"ping fail error: {e}")


def push_alert(title: str, body: str) -> None:
    text = f"{title}\n{body}"
    if DISCORD_WEBHOOK:
        try:
            payload = json.dumps({"content": f"**{title}**\n```{body[:1800]}```"}).encode()
            _http_post(DISCORD_WEBHOOK, payload, {"Content-Type": "application/json"})
        except Exception as e:
            log(f"discord webhook error: {e}")
    if SLACK_WEBHOOK:
        try:
            payload = json.dumps({"text": text[:3000]}).encode()
            _http_post(SLACK_WEBHOOK, payload, {"Content-Type": "application/json"})
        except Exception as e:
            log(f"slack webhook error: {e}")
    if GENERIC_WEBHOOK:
        try:
            payload = json.dumps({"title": title, "body": body, "ts": now_iso()}).encode()
            _http_post(GENERIC_WEBHOOK, payload, {"Content-Type": "application/json"})
        except Exception as e:
            log(f"webhook error: {e}")
    if NTFY_TOPIC:
        try:
            _http_post(
                f"{NTFY_BASE}/{NTFY_TOPIC}",
                text.encode(),
                {"Title": title, "Content-Type": "text/plain",
                 "Priority": "high", "Tags": "warning,kalshi"},
            )
        except Exception as e:
            log(f"ntfy error: {e}")


def start_http_server() -> None:
    if HTTP_PORT <= 0:
        return

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            return

        def do_GET(self):
            if self.path in ("/healthz", "/health", "/"):
                body = json.dumps(_last_health or {"status": "starting"}).encode()
                code = 200 if (_last_health or {}).get("ok") else 503
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

    try:
        srv = HTTPServer(("0.0.0.0", HTTP_PORT), Handler)
    except OSError as e:
        log(f"http bind :{HTTP_PORT} failed: {e}")
        return
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    log(f"http health on 0.0.0.0:{HTTP_PORT}/healthz")


def main() -> None:
    global _last_health, _last_status
    start_http_server()
    has_push = bool(DISCORD_WEBHOOK or SLACK_WEBHOOK or GENERIC_WEBHOOK or NTFY_TOPIC)
    log(
        f"external monitor up poll={POLL_SEC}s "
        f"ping={'ON' if PING_URL else 'OFF'} "
        f"webhook={'ON' if has_push else 'OFF'} http={HTTP_PORT}"
    )
    if not PING_URL and not has_push:
        log("WARN: set HEALTHCHECKS_PING_URL (dead-man's switch) and/or "
            "DISCORD_WEBHOOK_URL / NTFY_TOPIC for phone alerts")

    while True:
        try:
            h = collect_health()
            _last_health = h
            HEALTH_PATH.write_text(json.dumps(h, indent=2))
            status = h["status"]
            if status == "ok":
                ping_success()
            else:
                ping_fail(",".join(h["issues"])[:200])

            if _last_status is None:
                _last_status = status
                log(f"initial status={status} cash={h.get('cash')} issues={h['issues']}")
            elif status != _last_status:
                title = f"Kalshi bot {status.upper()}"
                body = (
                    f"cash={h.get('cash')} halted={h.get('halted')}\n"
                    f"issues={h['issues']}\n"
                    f"runner_hb={h.get('runner_hb_age_s')} wd_hb={h.get('watchdog_hb_age_s')}\n"
                    f"ts={h['ts']}"
                )
                log(f"TRANSITION {_last_status} → {status}: {body}")
                push_alert(title, body)
                _last_status = status
            else:
                log(
                    f"status={status} cash={h.get('cash')} "
                    f"rhb={h.get('runner_hb_age_s')} whb={h.get('watchdog_hb_age_s')} "
                    f"issues={h['issues'] or '-'}"
                )
        except Exception as e:
            log(f"loop error: {e}")
            ping_fail(str(e)[:200])
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
