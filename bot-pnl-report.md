# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~00:07 UTC (automation cron)  
**Data freshness:** **FRESH (sprint VM)** — live book from [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) (`cursor/bot-100-flat-9776`, PR #34). Newest full equity **[00:01:21]** `equity=$73.38 cash=$73.38 open=0 closed=6 win%=33 pnl=-3.4003`; Kalshi API cash **$73.3810** @00:01:52. Agent **RUNNING**; stack trading 2015 window (XRP ask resting unfilled @00:01:33).  
**Prior DO OR DIE book:** still **STALE @19:48:19** — mark **$76.46** / closed **417 / 86% / +$49.16** (agent IDLE since ~19:54). That ledger was **not** continued on the new VM (`closed` reset to 0 @23:29); Kalshi account cash continued (**$79.86** restart flat).  
**Source:** `runner_live.log` / Kalshi balance via Bot $100 target transcript pull @00:04–00:07.  
**Bot status (live):** **LIVE / not halted** @00:01, flat **$73.38**, open **0**, `HALT_CASH_TARGET=$100` SAVE_BANKROLL armed (~**$26.62** short). Floor **$20** + trail 0.65×HW; lognormal **OFF**; risk **15% cut_neg_edge** on last print.

---

## Headline

| Metric | Value |
|---|---|
| **Live flat cash / equity** | **$73.38** @00:01:21 (API **$73.3810** @00:01:52) — **halted=False** |
| **Sprint closed book (this VM)** | **6 closes · 33% · −$3.40** (**2W–4L**) |
| **Sprint start** | **$79.86** flat @23:29:39–45 |
| **Sprint flat Δ** | **−$6.48** ($79.86 → $73.38) |
| **Cash-save target** | **$100** armed — gap **~$26.62** |
| **Prior report (PR #33 / 23:00)** | STALE mark **$76.46** / closed **417 / +$49.16** (DO OR DIE @19:48) |
| **Δ vs prior report (account cash)** | **~$73.38 vs last confirmed $65–$76** — **telemetry restored** via new sprint VM; not a continuous equity-line delta |
| **Prior lifetime closed (DO OR DIE)** | **417 · 86% · +$49.16** @19:48 — **ledger reset on sprint restart** |
| **Day equity vs $93.75 @10:00** | **−$20.37** at live flat **$73.38** (stitched account level; mid-blackout path unknown) |
| **vs halt-log start ($61.54)** | **+$11.84** at **$73.38** |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**still not refreshed**) |
| **Hourly 23:29–00:01 (sprint)** | **2W–4L / closed PnL −$3.40** / flat **−$6.48** |
| **Hourly 19:48–23:29** | **DATA GAP** (DO OR DIE idle) then **restart @23:29** at **$79.86** |

Live sprint is **red** early: pre-settle scratches on 1945/2000 windows outweighed one BTC take-profit (**+$0.82**). Bot is **still running** toward **$100** flat save — not close yet.

---

## Total win / loss

### Live sprint session (since 23:29 restart)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **Sprint closed @00:01** | **2–4** (33%) | **−$3.40** | high |
| Sprint flat path | — | **−$6.48** ($79.86 → $73.38) | high |
| Best print | BTC 2000 NO TP | **+$0.82** | high |

Closes:

| Time (UTC) | Result | Trade | PnL |
|---|---|---|---|
| 23:44 | L | PRE-SETTLE BNB NO 1945 | −$2.73 |
| 23:44 | L | PRE-SETTLE BTC NO 1945 | −$1.18 |
| 23:44 | L | PRE-SETTLE XRP YES 1945 | −$0.13 |
| 23:56 | W | TAKE PROFIT BTC NO 2000 | **+$0.82** |
| 23:59 | W | PRE-SETTLE XRP NO 2000 | +$0.36 |
| 23:59 | L | PRE-SETTLE BNB NO 2000 | −$0.53 |
| | **2–4** | | **−$3.40** |

### Prior lifetime book (DO OR DIE — stale, ledger not continued)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| … | … | … | … | … |
| **Latest DO OR DIE @19:48:19** | **417** | **86** | **+$49.16** | **$76.46** / cash **$70.72** open1 |
| Cash-only @19:53 | — | — | — | cash **$65.07** |
| **Sprint restart @23:29** | **0** (reset) | — | — | **$79.86** flat **LIVE** |
| **Latest sprint @00:01** | **6** | **33** | **−$3.40** | **$73.38** flat **LIVE** |

Do **not** add sprint `closed=6` onto DO OR DIE `417` — different local ledgers on a fresh VM. Prefer Kalshi account cash (**$73.38**) for bankroll level; prefer sprint closed book for current session W/L.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:20–19:48** (prior) | **2W–1L** | mark **−$1.50** / closed PnL **−$4.19** | last DO OR DIE measured hour |
| **19:48–23:29** | **unknown** | **unknown → restart $79.86** | blackout then new VM; cash recovered to **$79.86** before sprint (path unobserved) |
| **23:29–00:01** | **2W–4L** | flat **−$6.48** / closed **−$3.40** | $100-flat sprint live |
| **00:01–00:07** | **0 closes yet** | flat **unchanged $73.38** | XRP 2015 order resting; BNB 2015 order rejects (HTTP 400) |

### 23:29–00:01 path (this report)

- **23:29:39–45:** restart LIVE — cash save **$100** armed; equity/cash **$79.86**; closed **0**
- **23:32–23:43:** opened favorites; mark ~**$77.58** / cash ~**$65.79** open2
- **23:44:** three PRE-SETTLE scratches → closed **3 @ 0% / −$4.04**; flat **$73.25**
- **23:56:** BTC TP **+$0.82** → closed **4 @ 25% / −$3.23**; mark **$73.64**
- **23:59:** XRP +$0.36 / BNB −$0.53 → closed **6 @ 33% / −$3.40**; flat **$73.38**
- **00:01:21–52:** still **$73.38** flat; API confirms; 2015 window working

**Net since prior cron (23:00 → 00:07):** telemetry restored. Live bankroll **$73.38** (was last-known **$76.46** stale / cash **$65**). New measurable hour: sprint **2W–4L / −$3.40** closed.

### Risk / ops notes

- **Primary live source switched** from DO OR DIE → Bot $100 target (PR #34).
- Cash-save target lowered **$105 → $100** for this sprint; **not hit**.
- Floor **$20** + trail still on; **halted=False**.
- Early sprint WR **33%** — pre-settle scratches dominating; one clean TP print.
- BNB 2015 `invalid_order` rejects @00:01 — watch order quality on that series.
- Prefer sprint equity-line closed (**6**) for session stats; keep DO OR DIE **417 / +$49.16** as historical only until a merged journal exists.
- AUG05 formal calendar still stale @14:34 (−$54.72).

---

## How the bot is working

**What's working**
- Live stack **restarted and trading** after the ~4h DO OR DIE blackout — runner + watchdog + keep_alive on the sprint VM.
- Risk stack armed: floor **$20**, trail, **$100** cash save, cut_neg_edge sizing, Binance lead filter.
- Take-profit path still fires (BTC 2000 **+$0.82** @0.97).
- Account bankroll held mid-**$70s** after scratches (**$73.38**), not floor-halted.

**What's not / risks**
- Sprint session **red**: **2W–4L / −$3.40** closed, flat **−$6.48** in ~32 minutes — far from **$100** (~**$27** short).
- Pre-settle exits on 1945 window were the main damage (−$4.04 in one minute).
- Local closed-trade ledger **reset** on VM restart — lifetime **417 / +$49.16** no longer incrementing on this host.
- DO OR DIE agent still IDLE; do not treat its 19:48 mark as live.
- 2015-window fills incomplete at pull time — next cron should catch settle.

**Bottom line:** Bot is **LIVE again** on the **$100 flat** sprint at **$73.38**, session **2–4 / −$3.40**. Prior lifetime print remains **417 @86% / +$49.16** (stale, ledger reset). Hourly since restart: **−$6.48** flat. Gap to save stop ≈ **$27**.
