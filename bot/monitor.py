"""Trade journal + watchdog for the live 15m bot.

Runs beside runner.py (own tmux session). Every poll it:
  1. Journals each newly closed trade to bot/trade_journal.jsonl with
     context (entry band, window phase, BN state, size tag, exit reason).
  2. Flags recurring mistake patterns to bot/trade_journal_alerts.log:
       - 3+ losses in same series within 2h        → series_chop
       - 2+ losses in same 3m phase within 2h      → phase_leak
       - loss on a boosted (>1x) ticket             → boost_loss
       - loss where BN disagreed/warned at entry    → bn_ignored
       - single loss > JOURNAL_BIG_LOSS dollars     → big_loss
  3. Watchdog: notes if runner.py is not running or log is stale.

Facts only — sizing reactions stay in runner (series governor etc.).
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

BOT = Path(__file__).resolve().parent
STATE = BOT / "state_live.json"
RUNNER_LOG = BOT / "runner_live.log"
JOURNAL = BOT / "trade_journal.jsonl"
ALERTS = BOT / "trade_journal_alerts.log"
SEEN = BOT / ".journal_seen.json"

POLL_SEC = float(os.environ.get("JOURNAL_POLL_SEC", "60"))
BIG_LOSS = float(os.environ.get("JOURNAL_BIG_LOSS", "8"))
WINDOW_LEN = 900.0


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def phase_of(secs_left) -> str:
    if secs_left is None:
        return "?"
    into = WINDOW_LEN - float(secs_left)
    for lo, hi, name in ((0, 180, "0-3m"), (180, 360, "3-6m"), (360, 540, "6-9m"),
                         (540, 720, "9-12m")):
        if lo <= into < hi:
            return name
    return "12-15m"


def key_of(c: dict) -> str:
    return f"{c.get('ticker')}|{c.get('opened_ts')}"


def entry_band(entry) -> str:
    e = float(entry or 0)
    if e < 0.75:
        return "70-75"
    if e < 0.80:
        return "75-80"
    if e < 0.85:
        return "80-85"
    if e < 0.90:
        return "85-90"
    if e < 0.95:
        return "90-95"
    return "95+"


def journal_row(c: dict) -> dict:
    pnl = float(c.get("pnl") or 0)
    return {
        "ts": now_iso(),
        "close_ts": c.get("close_ts"),
        "ticker": c.get("ticker"),
        "series": (c.get("ticker") or "").split("-")[0],
        "side": c.get("side"),
        "entry": c.get("entry"),
        "band": entry_band(c.get("entry")),
        "phase": phase_of(c.get("secs_left_at_entry")),
        "cost": c.get("cost"),
        "pnl": round(pnl, 4),
        "won": pnl > 0,
        "exit_reason": c.get("exit_reason") or ("settle" if c.get("settled") else ""),
        "bn_dir": c.get("binance_dir"),
        "bn_confirmed": c.get("binance_confirmed"),
        "risk_frac": c.get("risk_frac"),
        "peak_mark": c.get("peak_mark"),
    }


def alert(msg: str) -> None:
    line = f"[{now_iso()}] {msg}"
    print(line, flush=True)
    with ALERTS.open("a") as f:
        f.write(line + "\n")


def check_patterns(rows: list[dict], new: list[dict]) -> None:
    """new = rows just journaled this poll; rows = full recent history."""
    cutoff = time.time() - 7200
    recent = [r for r in rows if float(r.get("close_ts") or 0) >= cutoff]
    for r in new:
        if r["won"]:
            continue
        pnl = float(r["pnl"])
        ser = r["series"]
        if abs(pnl) >= BIG_LOSS:
            alert(f"BIG_LOSS {ser} {r['ticker']} {pnl:+.2f} band={r['band']} "
                  f"phase={r['phase']} bn={r['bn_dir']} — check sizing/stacking")
        ser_losses = [x for x in recent if x["series"] == ser and not x["won"]]
        if len(ser_losses) >= 3:
            tot = sum(float(x["pnl"]) for x in ser_losses)
            alert(f"SERIES_CHOP {ser} {len(ser_losses)} losses in 2h ({tot:+.2f}) "
                  f"— governor should be cutting; consider demote if it persists")
        ph_losses = [x for x in recent if x["phase"] == r["phase"] and not x["won"]]
        if len(ph_losses) >= 3:
            tot = sum(float(x["pnl"]) for x in ph_losses)
            alert(f"PHASE_LEAK {r['phase']} {len(ph_losses)} losses in 2h ({tot:+.2f}) "
                  f"— review time-phase gates")
        if r.get("bn_dir") and r["side"]:
            want = "up" if r["side"] == "yes" else "down"
            if r["bn_dir"] not in ("", "flat", want):
                alert(f"BN_IGNORED {r['ticker']} {pnl:+.2f} bet {want} vs bn {r['bn_dir']} "
                      f"— lead feed disagreed at entry")
        rf = float(r.get("risk_frac") or 0)
        if rf >= 0.25:
            alert(f"HOT_TICKET_LOSS {r['ticker']} {pnl:+.2f} risk={100*rf:.0f}% "
                  f"— boosted ticket lost; cap working? review")


def watchdog() -> None:
    import subprocess
    try:
        out = subprocess.run(
            ["pgrep", "-f", "python3 -u bot/runner.py"],
            capture_output=True, text=True,
        ).stdout.strip()
        if not out:
            alert("WATCHDOG runner.py NOT RUNNING — needs manual restart "
                  "(bash /workspace/bot/start_live.sh in tmux kalshi-live)")
        elif len(out.splitlines()) > 1:
            alert(f"WATCHDOG multiple runners: {out.splitlines()} — kill extras!")
    except Exception:
        pass
    try:
        age = time.time() - RUNNER_LOG.stat().st_mtime
        if age > 300:
            alert(f"WATCHDOG runner log stale {age:.0f}s — bot may be hung")
    except Exception:
        pass


def main() -> None:
    seen: set[str] = set()
    if SEEN.exists():
        try:
            seen = set(json.loads(SEEN.read_text()))
        except Exception:
            seen = set()
    print(f"[{now_iso()}] journal monitor up poll={POLL_SEC}s big_loss=${BIG_LOSS}",
          flush=True)
    history: list[dict] = []
    if JOURNAL.exists():
        for line in JOURNAL.read_text().splitlines():
            try:
                history.append(json.loads(line))
            except Exception:
                pass
    while True:
        try:
            st = json.loads(STATE.read_text())
            new_rows = []
            with JOURNAL.open("a") as jf:
                for c in st.get("closed") or []:
                    k = key_of(c)
                    if k in seen:
                        continue
                    seen.add(k)
                    if not c.get("filled"):
                        continue  # unfilled scratches aren't lessons
                    row = journal_row(c)
                    jf.write(json.dumps(row) + "\n")
                    new_rows.append(row)
            if new_rows:
                history.extend(new_rows)
                check_patterns(history, new_rows)
            SEEN.write_text(json.dumps(sorted(seen)[-3000:]))
            watchdog()
        except Exception as e:
            print(f"[{now_iso()}] monitor error: {e}", flush=True)
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
