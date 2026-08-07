# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~13:05 UTC (automation cron)  
**Data freshness:** **STALE (~34 min)** but **CHANGED** vs prior cron — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) advanced with a full OG#3 engine restart @12:30. Newest filled equity **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent last activity **~12:31:02Z**; status **IDLE**. Runner may have traded after that without new transcript capture.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~36.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @13:03 via `batch-fetch-details`. DO OR DIE transcript **CHANGED** (+10,112 bytes / +104 lines vs 12:05). No newer live trading agent found.  
**Bot status (last confirmed @12:30):** Redeployed OG#3 with **halt floor $25** / cash_target OFF / SPRINT OFF. Flat (`open=0`), bankroll **$61.71**. Runner pid **244266** + keep_alive **244099** + watchdog **244119**; health `ok` @12:30:48–12:30:53Z; `halted=False`; SAVE False; PAUSED False.

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$61.71** / **$61.71** @12:30:53 (**flat**, open **0**) |
| **Latest closed book (DO OR DIE)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Cash-save / halt** | **halt if equity ≤ $25**; cash_target OFF; SPRINT OFF; SAVE not hit |
| **Prior report (PR #70 / 12:00)** | **$60.42 / 438 / +$55.92** @11:16 flat |
| **Δ vs prior report** | closed **438→444 (+6)**; closed pnl **+$1.27**; equity **+$1.29** |
| **Hourly since ~12:05 cron** | **+6 closes / closed PnL +$1.27** — closes off-log between 11:16 and 12:30; book flat again |
| **Day equity vs $93.75 @10:00** | **−$32.04** at last mark **$61.71** |
| **vs start_equity ($61.54)** | **+$0.17** at last mark **$61.71** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since ~12:31 (~34 min); Bot $100 target **IDLE** since ~00:46 (~36.3h) |
| **Transcript** | **CHANGED** — **10,269,160** bytes / **94,673** lines (was 10,259,048 / 94,569); last bot ts **~12:30:53** |

Live book source of truth remains **DO OR DIE**. Since the 12:00 print @$60.42 / 438, the next confirmed mark is the 12:30 redeploy: closed **+6**, equity **+$1.29** to **$61.71**, flat. **No Aug-7 SETTLE / LIVE FILL strings** after 10:57 — the +6 closes remain off-log.

---

## How the bot is working (profit read)

Closed hit rate still strong (**86%**, ~**382–62**). Lifetime closed PnL is **+$57.18** (was **+$55.92** at 12:00) and bankroll is **$61.71** — now slightly **above** start equity (**+$0.17** vs `$61.54`), still **−$32.04** vs the $93.75 day high. Between 11:16 and 12:30 the book quietly added **6 closes** for about **+$1.27** closed PnL with no on-log fills/settles. At 12:30 the supervisor fully restarted OG#3 (floor $25, edge_kelly 13%, unit 8.62), confirmed health ok, left the book flat — then went **IDLE**, so this print is **~34 min stale**.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 Aug 6** | **424** | **86** | **~365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@10:56:42 Aug 7** | **430** | **86** | **~370–60** | **+$48.48** | **$52.99** / $40.28 open3 |
| **@11:16:02 Aug 7** | **438** | **86** | **~377–61** | **+$55.92** | **$60.42** / $60.42 flat |
| **@12:30:53 Aug 7 (latest confirmed)** | **444** | **86** | **~382–62** | **+$57.18** | **$61.71** / $61.71 flat |

Exact latest confirmed equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

**Note:** resume logs still show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only; use **444 / +$57.18** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~36.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444`.

### Opens last known

**Flat @12:30** — resumed / live balance cash **$61.71**, opens **0**. Deploy note: “OG Strategy #3 is live — flat at **$61.71**”.

### FILL / LIVE FILL / SETTLE in window since prior cron

**No LIVE FILL after 10:57:05.** **No Aug-7 SETTLE strings after 10:56.** Entire **+6 / +$1.27** move since 11:16 is off-log (likely `0715`/`0730` window resolutions while the supervising agent was idle).

Redeploy context immediately before newest mark:
- Full engine restart @12:30:40–12:30:52; stack up keep_alive **244099** / watchdog **244119** / runner **244266**
- Mode: `HALT_FLOOR=25`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **8.62**, risk **13.0%(edge_kelly)**, edge_wr **83.7%**
- `halted=False`; PAUSED False; SAVE False

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03** | **+3 closes** (421→424) | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **10:03 Aug 6 – 10:01 Aug 7** | **0–0** | **$0** | STALE — identical 09:39 mark (PRs #45–#68) |
| **10:01–11:20** | **+6 closes** (424→430) | closed **−$3.81**; equity **−$3.83** | wake @10:54; 1 on-log SETTLE (BNB −4.87); +5 closes off-log |
| **11:02–12:05** | **+8 closes** (430→438) | closed **+$7.44**; equity **+$7.43** | `0700` resolved off-log; flat @$60.42 |
| **12:05–13:05 (this report)** | **+6 closes** (438→444) | closed **+$1.27**; equity **+$1.29** | off-log closes; OG#3 redeploy @12:30 @$61.71 flat |
| **Bot $100 VM 12:05–13:05** | **0–0** | **$0** | still frozen @$60.61 |

### 12:05→13:05 path (this report)

- **12:05 prior cron (PR #70):** DO OR DIE **CHANGED / STALE ~49m** @11:16 — **$60.42 / 438 / 86% / +$55.92**; flat; halt floor $25
- **13:05 pull:** DO OR DIE transcript **advanced** — newest filled mark **$61.71 / 444 / +$57.18** flat after 12:30 redeploy; Bot $100 still @00:46; transcript now **10.27 MiB / 10269160 bytes / 94673 lines**
- **No newer live trading agent** besides DO OR DIE (scan: only these two + this automation)
- Agent IDLE since ~12:31 → mark age **~34 min** at pull; further post-12:30 trading would not appear here

**Net vs prior cron:** **+6 closes / +$1.27 closed PnL / +$1.29 equity** — bankroll now slightly above start; still below day high.

### Risk / ops notes

- Last confirmed log **~12:30:53**; freshness **~34 min STALE** despite **CHANGED** vs 12:00 cron.
- Closed book **86%** at **444** / **+$57.18**; bankroll **$61.71** (**−$32.04** vs $93.75 day; **+$0.17** vs $61.54 start).
- Mode: **halt floor $25** / cash_target OFF / SPRINT OFF; SAVE not hit; flat after OG#3 redeploy.
