# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~09:02 UTC (automation cron)  
**Data freshness:** **STALE (~23h23m / ~23.4h)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) still shows the same newest equity **[09:39:01]** `equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886`. Supervising agent last activity **~09:39:24Z**; status **IDLE**. No SETTLE / FILL / equity lines after the 09:39 wake + 3rd fill @09:39:14.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~32.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @09:02 via `batch-fetch-details` (identical end state to 08:02 / PR #66). No newer live trading agent found.  
**Bot status (last confirmed @09:39:16):** **SPRINT mode** — `HALT_DISABLED=1`, `HALT_CASH_TARGET=$100`, `HALT_FLOOR=0`; runner pid **230425** + keep_alive **227092** + watchdog **230397**; `halted=False`; SAVE False; PAUSED False. After the equity print, a 3rd fill left cash **41.4954** with **3 opens** / `hw 56.8223` on the `0545` window. **Runner status after 09:39 unknown** (no new supervising transcript).

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$56.82** / **$46.60** @09:39:01 (**2 opens** at mark; then **3 opens / $41.4954** cash) |
| **Latest closed book (DO OR DIE)** | **424 closes · 86% · +$52.29** (~**365–59**) |
| **Cash-save target** | **$100** armed — gap **~$53.40** on mark cash / **~$58.50** after 3rd fill (**not hit**) |
| **Prior report (PR #66 / 08:00)** | same **$56.82 / 424 / +$52.29** @09:39 |
| **Δ vs prior report** | closed **424→424 (0)**; closed pnl **unchanged**; equity **unchanged** |
| **Hourly since ~08:02 cron** | **0–0 / $0** — no new equity/FILL/SETTLE in tape |
| **Day equity vs $93.75 @10:00** | **−$36.93** at last mark **$56.82** |
| **vs start_equity ($61.54)** | **−$4.72** at last mark **$56.82** |
| **High-water** | **~$99.12** (pre-halt overnight); state `hw 56.8223` @09:39 |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since 09:39 (~23.4h); Bot $100 target **IDLE** since ~00:46 (~32.3h) |
| **Transcript** | **UNCHANGED** — 9.60 MiB / **10065427** bytes / **92073** lines; last bot ts **09:39:14** |

Live book source of truth remains **DO OR DIE**, but the supervising transcript has **not advanced** past the 09:39 wake. The three `0545` opens that should have settled ~09:45 are **still unresolved in the pull** — next mark unknown. Twenty-fourth consecutive stale hourly after the 09:39 wake.

---

## How the bot is working (profit read)

Last confirmed closed book is still strong on hit rate (**86%**, ~**365–59**, **+$52.29** lifetime closed PnL), but the **bankroll softens** at last mark (**$56.82** equity, **−$36.93** vs the $93.75 day print, **−$4.72** vs `$61.54` start). Sprint-to-$100 remains armed and not hit (cash ~**$41.50** after the third `0545` fill). **No trading confirmation for ~23.4h** — profit figures below are a frozen last-known snapshot, not evidence of ongoing production.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 (latest confirmed)** | **424** | **86** | **~365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@09:02 cron pull (Aug 7)** | **424** (unchanged) | **86** | same | **+$52.29** | **STALE** — no newer mark |

Exact latest confirmed equity line:
```
[09:39:01] equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886  unit=10.99  risk=18.0%(edge_kelly) edge_wr=86.2% ev=$+0.125
```

**Note:** resume logs still show higher `closed=` counts for filled+unfilled history. Equity-line **`closed=424`** is **filled** closes only; use **424 / +$52.29** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~32.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `424`.

### Opens last known @09:39 (settle still missing)

| Time | Market | Side | Entry ≈ | Size ≈ | Cash after |
|---|---|---|---|---|---|
| 09:39:00 | `KXBNB15M-26AUG060545-45` | YES | ~0.70 | 7.30 | $46.60 |
| 09:39:00 | `KXXRP15M-26AUG060545-45` | NO | ~0.73 | 7.00 | $46.60 |
| 09:39:14 | `KXBTC15M-26AUG060545-45` | NO | ~0.87 | 5.87 | **$41.50** |

Post-mark state peek @09:39:16: `cash 41.4954 halted False open 3 hw 56.8223`. `0545` window should have settled ~09:45 — outcome **still not** in this pull (no SETTLE lines after 09:39). ~23.4h of silence since.

### FILL / LIVE FILL after 09:39:01

```
[09:39:14] LIVE FILL NO 5.87 @ ~0.87 on KXBTC15M-26AUG060545-45 status=executed cash=$41.50 risk=18.0% bn=flat
```

No further FILL / LIVE FILL / SETTLE after **09:39:14**.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03** | **+3 closes** (421→424) | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **10:03–08:20** | **0–0** | **$0** | STALE — identical 09:39 mark (PRs #45–#66) |
| **08:02–09:20 (this report)** | **0–0** | **$0** | STALE — still identical 09:39 mark; `0545` settle still missing |
| **Bot $100 VM 08:02–09:20** | **0–0** | **$0** | still frozen @$60.61 |

### 08:02→09:20 path (this report)

- **08:02 prior cron (PR #66):** DO OR DIE **STALE** @09:39 — **$56.82 / 424 / 86% / +$52.29**; cash → **~$41.50** / open **3** after BTC fill; sprint armed
- **09:02 pull:** re-fetched both transcripts — **no new messages** on DO OR DIE past 09:39:24; Bot $100 still @00:46; transcript size still **9.60 MiB / 10065427 bytes / 92073 lines**
- **No newer live trading agent** besides DO OR DIE (desktop/mobile/web/cli scan: only these two)

**Net vs prior cron:** **0 closes / $0 closed PnL / $0 equity delta** — tape stuck; `0545` settle still missing (~23.3h past expected settle).

### Risk / ops notes

- **Tape still quiet** after the 09:39 wake — supervising agent IDLE ~23.4h; cannot confirm runner still alive.
- Closed book still **86%** at **424** / **+$52.29**, but bankroll soft at last mark **$56.82** (**−$36.93** vs $93.75 day).
- **SPRINT $100** still armed at last confirm; SAVE not hit (cash ~$41.50 after 3rd fill).
- Events file: only old PR/artifact events; no new trading activity signals.
