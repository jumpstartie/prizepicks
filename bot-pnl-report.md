# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~03:03 UTC (automation cron)  
**Data freshness:** **STALE (sprint VM idle ~2h17m)** — last full book from [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) (`cursor/bot-100-flat-9776`, PR #34). Newest full equity still **[00:46:06]** `equity=$60.61 cash=$60.61 open=0 closed=14 win%=43 pnl=-15.8011`; Kalshi API cash **$60.6125** @00:46:25. Agent remains **IDLE** (last activity ~00:46:47; updated ~00:55). **No new equity, closes, or API prints after 00:46.**  
**Prior DO OR DIE book:** still **STALE @19:48:19 Aug 5** — mark **$76.46** / closed **417 / 86% / +$49.16** (agent IDLE since ~19:54). That ledger was **not** continued on the sprint VM.  
**Source:** Bot $100 target + DO OR DIE transcript pulls @03:02 via `batch-fetch-details`.  
**Bot status (last known):** **not strategy-halted** @00:46 (`halted=False`, `SAVE False`), flat **$60.61**, open **0**, `HALT_CASH_TARGET=$100` still armed (~**$39.39** short) — supervising agent **IDLE**; runner liveness after 00:46 **unverified**.

---

## Headline

| Metric | Value |
|---|---|
| **Live flat cash / equity** | **$60.61** @00:46:06 (API **$60.6125** @00:46:25) — **unchanged** |
| **Sprint closed book (this VM)** | **14 closes · 43% · −$15.80** (**6W–8L**) — **unchanged** |
| **Sprint start** | **$79.86** flat @23:29:39–45 |
| **Sprint flat Δ** | **−$19.25** ($79.86 → $60.61) |
| **Cash-save target** | **$100** armed — gap **~$39.39** (**not hit**) |
| **Prior report (PR #37 / 02:00)** | flat **$60.61** / closed **14 / 43% / −$15.80** |
| **Δ vs prior report** | flat **$0.00**; closed **+0**; closed PnL **unchanged** |
| **Prior lifetime closed (DO OR DIE)** | **417 · 86% · +$49.16** @19:48 — historical only |
| **Day equity vs $93.75 @10:00** | **−$33.14** at last flat **$60.61** |
| **vs halt-log start ($61.54)** | **−$0.93** at **$60.61** |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**still not refreshed**) |
| **Hourly 02:03–03:03** | **0W–0L** / **no new marks** (telemetry frozen) |
| **Agent status** | Bot $100 target **IDLE** since ~00:46; DO OR DIE still IDLE |

Sprint remains **deep red and frozen**: no trading telemetry for ~**137 minutes**. Last damage was the 2030/2045 settle losses. **$100** save and **$20** floor both **not** hit. Without a live supervisor, treat **$60.61** as last-known bankroll, not a live stream.

---

## Total win / loss

### Live sprint session (since 23:29 restart)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **Sprint closed @00:46 (still current)** | **6–8** (43%) | **−$15.80** | high @mark; stale since |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |
| Best print | BTC 2015 NO TP | **+$1.92** | high |
| Worst print | BTC 2030 NO settle | **−$5.54** | high |

Closes (full session — **no new closes since prior cron**):

| Time (UTC) | Result | Trade | PnL |
|---|---|---|---|
| 23:44 | L | PRE-SETTLE BNB NO 1945 | −$2.73 |
| 23:44 | L | PRE-SETTLE BTC NO 1945 | −$1.18 |
| 23:44 | L | PRE-SETTLE XRP YES 1945 | −$0.13 |
| 23:56 | W | TAKE PROFIT BTC NO 2000 | **+$0.82** |
| 23:59 | W | PRE-SETTLE XRP NO 2000 | +$0.36 |
| 23:59 | L | PRE-SETTLE BNB NO 2000 | −$0.53 |
| 00:11 | W | TAKE PROFIT BTC NO 2015 | **+$1.92** |
| 00:14 | L | PRE-SETTLE XRP NO 2015 | −$1.57 |
| 00:15 | W | SETTLE BNB YES 2015 | +$0.34 |
| 00:30 | L | SETTLE BTC NO 2030 | **−$5.54** |
| 00:30 | L | SETTLE BNB NO 2030 | **−$3.55** |
| ~00:40–41 | W | XRP 2045 (inferred) | ≈+$0.00 |
| ~00:44 | W | BNB YES 2045 (inferred) | ≈+$0.64 |
| 00:45 | L | SETTLE BTC YES 2045 | **−$4.64** |
| | **6–8** | | **−$15.80** |

### Prior lifetime book (DO OR DIE — stale, ledger not continued)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| **Latest DO OR DIE @19:48:19** | **417** | **86** | **+$49.16** | **$76.46** / cash **$70.72** open1 |
| **Sprint restart @23:29** | **0** (reset) | — | — | **$79.86** flat |
| **Prior cron @02:03** | **14** | **43** | **−$15.80** | **$60.61** flat / agent **IDLE** |
| **This cron @03:03** | **14** | **43** | **−$15.80** | **$60.61** flat / agent **still IDLE** |

Do **not** add sprint `closed=14` onto DO OR DIE `417`. Prefer Kalshi account cash (**$60.61** last-known) for bankroll; prefer sprint closed book for current session W/L.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–23:29** | **unknown** | **unknown → restart $79.86** | blackout then new VM |
| **23:29–00:01** | **2W–4L** | flat **−$6.48** / closed **−$3.40** | first sprint hour |
| **00:01–00:46** | **4W–4L** | flat **−$12.77** / closed **−$12.40** | last active trading hour |
| **00:46–01:02** | **0 closes** | **no new marks** | agent IDLE; frozen @$60.61 |
| **01:02–02:03** | **0 closes** | **no new marks** | still IDLE |
| **02:03–03:03** | **0 closes** | **no new marks** | still IDLE; **this report’s measured hour** |

### 02:03–03:03 path (this report)

- **02:03 prior:** flat **$60.61** / closed **14 / −$15.80**; Bot $100 target **IDLE**
- **03:02 re-pull:** same equity line **`[00:46:06] equity=$60.61 … closed=14 win%=43 pnl=-15.8011`**; cash heartbeats stop at **00:46:17**; API **$60.6125** @00:46:25 still newest
- **No** SETTLE / TAKE PROFIT / PRE-SETTLE fills after **00:45:21**
- **No** closed-count or PnL movement vs PR #37
- Agent lastMessageActivity still **00:46:47**; index updatedAt still **00:55**

**Net since prior cron (02:03 → 03:03):** flat **$60.61 → $60.61 ($0.00)**; closed PnL **−$15.80 → −$15.80**. Session remains **6–8 / −$15.80**.

### Risk / ops notes

- **Supervising agent IDLE for ~137 minutes** — last process check @00:46 showed `runner.py` PID 4101, but **no confirmation since**. Do not assume live risk.
- Cash-save **$100** and floor **$20** still armed in last config dump; **neither hit**.
- Dominant historical damage this sprint: pre-settle IOC no-fills that rode to settle (2030 double + 2045 BTC ≈ **−$13.73**).
- Prefer sprint equity-line closed (**14**) for session stats; keep DO OR DIE **417 / +$49.16** historical.
- AUG05 formal calendar still stale @14:34 (−$54.72).
- **Ops priority:** restart / re-attach a live supervisor if the $100 sprint is still intended — book has not moved and cannot hit **$100** while dark.

---

## How the bot is working

**What's working**
- Last-known risk stack did **not** floor-halt; bankroll stayed above **$20**.
- Local closed ledger consistent and stable: **14 closes / 6W–8L / −$15.80**.
- Take-profit path worked earlier in the sprint when marks ran (BTC **+$1.92**).

**What's not / risks**
- **No new trading activity since 00:46** — hourly W/L is **0–0 / $0** for a third straight cron.
- Session still **deep red**: **6–8 / −$15.80** closed, flat **−$19.25** from **$79.86** — gap to **$100** still ~**$39**.
- **Bot $100 target agent remains IDLE** — runner liveness unverified for over two hours.
- DO OR DIE remains stale; no merged lifetime journal.
- Day equity vs morning **$93.75** is about **−$33**.

**Bottom line:** Last confirmed book is still **$60.61 flat**, sprint **6–8 / −$15.80**, hourly since prior cron **0–0 / $0** (frozen ~2h17m). **$100** save not hit. Sprint supervisor has been **IDLE since ~00:46** — confirm runner / restart before treating bankroll as live.
