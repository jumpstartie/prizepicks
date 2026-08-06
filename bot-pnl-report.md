# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~01:02 UTC (automation cron)  
**Data freshness:** **STALE-ISH (sprint VM idle)** — last full book from [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) (`cursor/bot-100-flat-9776`, PR #34). Newest full equity **[00:46:06]** `equity=$60.61 cash=$60.61 open=0 closed=14 win%=43 pnl=-15.8011`; Kalshi API cash **$60.6125** @00:46:25. Agent now **IDLE** (last activity ~00:46); no newer equity prints after that.  
**Prior DO OR DIE book:** still **STALE @19:48:19** — mark **$76.46** / closed **417 / 86% / +$49.16** (agent IDLE since ~19:54). That ledger was **not** continued on the sprint VM.  
**Source:** `runner_live.log` / Kalshi balance via Bot $100 target transcript pull @01:02.  
**Bot status (last known):** **not strategy-halted** @00:46 (`halted=False`, `SAVE False`), flat **$60.61**, open **0**, `HALT_CASH_TARGET=$100` still armed (~**$39.39** short) — but **supervising agent IDLE**, so live trading may have stopped with the agent.

---

## Headline

| Metric | Value |
|---|---|
| **Live flat cash / equity** | **$60.61** @00:46:06 (API **$60.6125** @00:46:25) — **halted=False** |
| **Sprint closed book (this VM)** | **14 closes · 43% · −$15.80** (**6W–8L**) |
| **Sprint start** | **$79.86** flat @23:29:39–45 |
| **Sprint flat Δ** | **−$19.25** ($79.86 → $60.61) |
| **Cash-save target** | **$100** armed — gap **~$39.39** (**not hit**) |
| **Prior report (PR #35 / 00:00)** | flat **$73.38** / closed **6 / 33% / −$3.40** |
| **Δ vs prior report** | flat **−$12.77**; closed **+8** (6→14); closed PnL **−$12.40** worse |
| **Prior lifetime closed (DO OR DIE)** | **417 · 86% · +$49.16** @19:48 — historical only |
| **Day equity vs $93.75 @10:00** | **−$33.14** at last flat **$60.61** |
| **vs halt-log start ($61.54)** | **−$0.93** at **$60.61** |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**still not refreshed**) |
| **Hourly 00:01–00:46** | **4W–4L** / closed PnL **−$12.40** / flat **−$12.77** |
| **Agent status** | Bot $100 target **IDLE** after ~00:46; DO OR DIE still IDLE |

Sprint is **deep red**: failed pre-settles rode to settle (−$5.54 / −$3.55 / −$4.64). Peak after 00:01 was **$75.28** on BTC TP; book then bled to **$60.61**. **$100** save and **$20** floor both **not** hit.

---

## Total win / loss

### Live sprint session (since 23:29 restart)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **Sprint closed @00:46** | **6–8** (43%) | **−$15.80** | high |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high |
| Best print | BTC 2015 NO TP | **+$1.92** | high |
| Worst print | BTC 2030 NO settle | **−$5.54** | high |

Closes (full session):

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
| **Prior cron @00:01** | **6** | **33** | **−$3.40** | **$73.38** flat |
| **Latest sprint @00:46** | **14** | **43** | **−$15.80** | **$60.61** flat / agent **IDLE** |

Do **not** add sprint `closed=14` onto DO OR DIE `417`. Prefer Kalshi account cash (**$60.61**) for bankroll; prefer sprint closed book for current session W/L.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–23:29** | **unknown** | **unknown → restart $79.86** | blackout then new VM |
| **23:29–00:01** (prior) | **2W–4L** | flat **−$6.48** / closed **−$3.40** | first sprint hour |
| **00:01–00:46** | **4W–4L** | flat **−$12.77** / closed **−$12.40** | this report’s measured hour |
| **00:46–01:02** | **0 closes** | **no new marks** | supervising agent IDLE; telemetry frozen @$60.61 |

### 00:01–00:46 path (this report)

- **00:01:** prior mark flat **$73.38** / closed **6 / −$3.40**; 2015 window filling
- **00:11:** BTC TP **+$1.92** → closed **7 @ 43% / −$1.48**; equity peak **$75.28**
- **00:14–15:** XRP scratch **−$1.57**, BNB settle **+$0.34** → closed **9 / −$2.72**; flat ~**$73.91** then open risk
- **00:30:** BTC/BNB 2030 pre-settle IOC **no-fill** → ride to settle **−$5.54 / −$3.55** → closed **11 / −$11.80**; flat **~$58–63**
- **~00:40–44:** two small wins (XRP ≈+$0.00, BNB ≈+$0.64) → closed **13 / −$11.16**
- **00:45:** BTC 2045 YES settle **−$4.64** → closed **14 @ 43% / −$15.80**; flat **$60.61**
- **00:46:25:** API confirms **$60.6125** / portfolio **0**; watching 2100 — then agent goes quiet → **IDLE**

**Net since prior cron (00:07 → 01:02):** flat **$73.38 → $60.61 (−$12.77)**; closed PnL **−$3.40 → −$15.80**. Session WR improved slightly (33%→43%) but absolute PnL worsened on large settle losses.

### Risk / ops notes

- **Supervising agent IDLE** — last claim was runner still up @00:46, but no confirmation after that. Treat book as **last-known**, not live streaming.
- Cash-save **$100** and floor **$20** still armed in last config dump; **neither hit**.
- Dominant damage: **pre-settle IOC no-fills** that rode to full settle (2030 double + 2045 BTC).
- TP path still works when marks run (BTC **+$1.92** @0.97) — not enough to offset settle losses.
- Prefer sprint equity-line closed (**14**) for session stats; keep DO OR DIE **417 / +$49.16** historical.
- AUG05 formal calendar still stale @14:34 (−$54.72).

---

## How the bot is working

**What's working**
- Sprint did keep trading through 2015/2030/2045 windows after the 00:00 report.
- Take-profit still fires on strong favorites (BTC 2015 **+$1.92**).
- Risk stack did **not** floor-halt; bankroll stayed above **$20** (low print ~**$53.49** cash with open risk).
- Local closed ledger consistent: **14 closes / 6W–8L / −$15.80**.

**What's not / risks**
- Session **deep red**: **6–8 / −$15.80** closed, flat **−$19.25** from **$79.86** — gap to **$100** now ~**$39**.
- Pre-settle exit quality failed on 2030/2045 — IOC no-fills turned into full settle losses (**−$13.73** combined on those three).
- **Bot $100 target agent is IDLE** — without a live supervisor, do not assume the runner is still placing risk.
- DO OR DIE remains stale; no merged lifetime journal.
- Day equity vs morning **$93.75** is about **−$33**.

**Bottom line:** Last confirmed book is **$60.61 flat**, sprint **6–8 / −$15.80**, hourly since prior cron **4–4 / −$12.40** closed (**−$12.77** flat). **$100** save not hit. Agent supervising the sprint is now **IDLE** — next priority is confirming whether the runner is still alive or needs a restart.
