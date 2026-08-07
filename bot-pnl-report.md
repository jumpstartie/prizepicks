# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~21:05 UTC (automation cron)  
**Data freshness:** **STALE (~8h 34m)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled equity still **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent last activity **~13:21:52Z** (~7h 43m freeze); status **IDLE**. Transcript **UNCHANGED** vs 20:05.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~44.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @21:00 via `batch-fetch-details`. DO OR DIE transcript **UNCHANGED** (10,605,306 bytes / 96,495 lines) — **no new filled crypto equity line**. No newer live trading agent found.  
**Bot status (last confirmed @12:30):** Redeployed OG#3 with **halt floor $25** / cash_target OFF / SPRINT OFF. Last equity mark flat (`open=0`), bankroll **$61.71**. Runner pid **244266**; health `ok` @12:30; `halted=False`; SAVE False; PAUSED False. Stale MLB side-check still shows **crypto cash 54.1 / hw 55.25 / runner True / health ok** (possible open exposure; no new equity line).

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) |
| **Latest closed book (DO OR DIE)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Cash-save / halt** | **halt if equity ≤ $25**; cash_target OFF; SPRINT OFF; SAVE not hit |
| **Prior report (PR #78 / 20:00)** | **$61.71 / 444 / +$57.18** @12:30 flat |
| **Δ vs prior report** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~20:05 cron** | **0–0 / $0** — identical filled mark; transcript frozen |
| **Day equity vs $93.75 @10:00** | **−$32.04** at last mark **$61.71** |
| **vs start_equity ($61.54)** | **+$0.17** at last mark **$61.71** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since ~13:21 (~7h 43m); Bot $100 target **IDLE** since ~00:46 (~44.3h) |
| **Transcript** | **UNCHANGED** — **10,605,306** bytes / **96,495** lines; last bot equity ts **~12:30:53** |

Live book source of truth remains **DO OR DIE**. Since the 20:00 print @$61.71 / 444, there is **no new filled equity mark** and **no transcript growth**. Hourly closed PnL is **flat**. The mid-session MLB side-check (**crypto cash $54.1 / hw $55.25**) remains the only soft warning that the book may have opened size after 12:30 without a fresh equity line.

---

## How the bot is working (profit read)

Closed hit rate remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last bankroll mark is **$61.71** — slightly **above** start equity (**+$0.17** vs `$61.54`), still **−$32.04** vs the $93.75 day high. This hour added **no confirmed closes**: the supervising agent stayed **IDLE** with an identical transcript blob, so the crypto equity tape is still pinned at the 12:30 OG#3 redeploy mark. Ops read: strategy still profitable on the filled book, but the print is **~8h 34m stale**, and the $54.1 cash side-check still suggests possible live exposure not yet reflected in `closed`/`pnl` equity lines.

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
| **@12:30:53 Aug 7 (latest confirmed)** | **444** | **86** | **~382–62** | **+$57.18** | **$61.71** / **$61.71** flat |

Exact latest confirmed equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

**Note:** resume logs still show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only; use **444 / +$57.18** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~44.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444`.

### Opens last known

**Flat on last equity @12:30** — cash **$61.71**, opens **0**.  
**Soft side-check (~13:15–13:21 MLB session):** `crypto cash 54.1 halted False hw 55.25` / `runner True` / `health ok True []` — cash **−$7.61** vs mark without a new equity/`open=` line.

### FILL / LIVE FILL / SETTLE in window since prior cron

**No LIVE FILL after 10:57:05.** **No Aug-7 SETTLE strings after 10:56.**  
**No new filled equity after 12:30:53.** Hourly closed book **unchanged**.

Mode still last confirmed at OG#3 redeploy:
- `HALT_FLOOR=25`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **8.62**, risk **13.0%(edge_kelly)**, edge_wr **83.7%**
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
| **12:05–13:05** | **+6 closes** (438→444) | closed **+$1.27**; equity **+$1.29** | off-log closes; OG#3 redeploy @12:30 @$61.71 flat |
| **13:05–14:05** | **0–0** | **$0** | same filled mark @$61.71 / 444; MLB transcript growth only |
| **14:05–15:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **15:05–16:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **16:05–17:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **17:05–18:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **18:05–19:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **19:05–20:05** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **20:05–21:05 (this report)** | **0–0** | **$0** | transcript **UNCHANGED**; mark still @$61.71 / 444 |
| **Bot $100 VM 20:05–21:05** | **0–0** | **$0** | still frozen @$60.61 |

### 20:05→21:05 path (this report)

- **20:05 prior cron (PR #78):** DO OR DIE **UNCHANGED / STALE ~7h34m** @12:30 — **$61.71 / 444 / 86% / +$57.18**; flat; halt floor $25
- **21:05 pull:** DO OR DIE transcript **identical** — newest filled crypto mark **unchanged** **$61.71 / 444 / +$57.18**; Bot $100 still @00:46; transcript still **10.61 MiB / 10605306 bytes / 96495 lines**
- **No newer live trading agent** besides DO OR DIE (scan: only these two + this automation)
- Agent IDLE since ~13:21 → equity mark age **~8h 34m** at pull; cash side-check **$54.1** may imply post-mark opens not yet equity-logged

**Net vs prior cron:** **+0 closes / +$0.00 closed PnL / +$0.00 equity** on the filled book — still slightly above start; still below day high.

### Risk / ops notes

- Last confirmed equity log **~12:30:53**; freshness **~8h 34m STALE**. Transcript **UNCHANGED** vs 20:05.
- Closed book **86%** at **444** / **+$57.18**; bankroll mark **$61.71** (**−$32.04** vs $93.75 day; **+$0.17** vs $61.54 start).
- Mode: **halt floor $25** / cash_target OFF / SPRINT OFF; SAVE not hit.
- Watch: MLB side-check **crypto cash $54.1 / hw $55.25** while equity mark still shows flat **$61.71** — needs a fresh equity/`open=` print to confirm exposure.
