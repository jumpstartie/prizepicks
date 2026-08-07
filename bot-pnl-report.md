# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~00:05 UTC (automation cron)  
**Data freshness:** **STALE (~14h26m)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) still shows the same newest equity **[09:39:01]** `equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886`. Supervising agent last activity **~09:39:24Z**; status **IDLE**. No SETTLE / FILL / equity lines after the 09:39 wake + 3rd fill.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~23.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @00:04 via `batch-fetch-details` (identical end state to 23:03 / PR #57). No newer live trading agent found.  
**Bot status (last confirmed @09:39):** **SPRINT mode** — `HALT_DISABLED=1`, `HALT_CASH_TARGET=$100`, `HALT_FLOOR` off / halt=$0; runner + watchdog + keep_alive present at that check; `halted=False`. After the equity print, a 3rd fill left cash **~$41.50** with **3 opens** on the `0545` window. **Runner status after 09:39 unknown** (no new supervising transcript).

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$56.82** / **$46.60** @09:39:01 (**2 opens** at mark; then **3 opens / ~$41.50** cash) |
| **Latest closed book (DO OR DIE)** | **424 closes · 86% · +$52.29** (~**364–60 to 365–59**) |
| **Cash-save target** | **$100** armed — gap **~$53.40** on mark cash / **~$58.50** after 3rd fill (**not hit**) |
| **Prior report (PR #57 / 23:00)** | same **$56.82 / 424 / +$52.29** @09:39 |
| **Δ vs prior report** | closed **424→424 (0)**; closed pnl **unchanged**; equity **unchanged** |
| **Hourly since ~23:03 cron** | **0–0 / $0** — no new equity/FILL/SETTLE in tape |
| **Day equity vs $93.75 @10:00** | **−$36.93** at last mark **$56.82** |
| **vs start_equity ($61.54)** | **−$4.72** at last mark **$56.82** |
| **High-water** | **~$99.12** (pre-halt overnight); state `hw 56.8223` @09:39 |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since 09:39 (~14.4h); Bot $100 target **IDLE** since ~00:46 (~23.3h) |

Live book source of truth remains **DO OR DIE**, but the supervising transcript has **not advanced** past the 09:39 wake. The three `0545` opens that should have settled ~09:45 are **still unresolved in the pull** — next mark unknown. Fifteenth consecutive stale hourly after the 09:39 wake (11:00, 12:00 gap/miss, 13:00–00:00).

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 (latest confirmed)** | **424** | **86** | **~364–60 / 365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@00:05 cron pull (Aug 7)** | **424** (unchanged) | **86** | same | **+$52.29** | **STALE** — no newer mark |

Exact latest confirmed line:
```
[09:39:01] equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886  unit=10.99  risk=18.0%(edge_kelly) edge_wr=86.2% ev=$+0.125
```

**Note:** resume logs still show higher `closed=` counts for filled+unfilled history. Equity-line **`closed=424`** is **filled** closes only; use **424 / +$52.29** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~23.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `424`.

### Opens last known @09:39 (settle still missing)

| Time | Market | Side | Entry ≈ | Size ≈ | Cash after |
|---|---|---|---|---|---|
| 09:39:00 | `KXBNB15M-26AUG060545-45` | YES | ~0.70 | 7.30 | $46.60 |
| 09:39:00 | `KXXRP15M-26AUG060545-45` | NO | ~0.73 | 7.00 | $46.60 |
| 09:39:14 | `KXBTC15M-26AUG060545-45` | NO | ~0.87 | 5.87 | **$41.50** |

Post-mark state peek @09:39:16: `cash 41.4954 halted False open 3 hw 56.8223`. `0545` window should have settled ~09:45 — outcome **still not** in this pull (no SETTLE lines after 09:39). ~14.4h of silence since.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03** | **+3 closes** (421→424) | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **10:03–11:06** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **11:06–13:06** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **13:06–14:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **14:05–15:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **15:05–16:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **16:05–17:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **17:05–18:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **18:05–19:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **19:05–20:03** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **20:03–21:04** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **21:04–22:03** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **22:03–23:05** | **0–0** | **$0** | STALE — identical 09:39 mark |
| **23:05–00:05 (this report)** | **0–0** | **$0** | STALE — still identical 09:39 mark; `0545` settle still missing |
| **Bot $100 VM 23:05–00:05** | **0–0** | **$0** | still frozen @$60.61 |

### Post-19:48 closes (unchanged vs PR #57)

| Time | Result | Trade | PnL |
|---|---|---|---|
| 20:00 | ~flat | PRE-SETTLE BTC NO 1600 | −$0.00 |
| 20:00 | W | PRE-SETTLE XRP NO 1600 | +$1.52 |
| 20:15 | ~flat | SETTLE BNB 1615 | +$0.00 |
| 20:15 | W | SETTLE XRP 1615 | +$2.14 |
| ~03:19–03:33 | W | XRP 2330 (inferred) | ≈+$1.20 |
| **03:35→09:39 (dark)** | **+3 closes** (detail unknown) | net closed | **−$1.74** |
| | **~+6 closes vs 19:48** | | **≈+$3.13** closed (49.16→52.29) |

### 23:05→00:05 path (this report)

- **23:03 prior cron (PR #57):** DO OR DIE **STALE** @09:39 — **$56.82 / 424 / 86% / +$52.29**; cash → **~$41.50** / open **3** after BTC fill; sprint armed
- **00:04 pull:** re-fetched both transcripts — **no new messages** on DO OR DIE past 09:39:24; Bot $100 still @00:46
- **No newer live trading agent** besides DO OR DIE (only this automation + extract subagents)

**Net vs prior cron:** **0 closes / $0 closed PnL / $0 equity delta** — tape stuck; `0545` settle still missing (~14.3h past expected settle).

### Risk / ops notes

- **Tape still quiet** after the 09:39 wake — supervising agent IDLE ~14.4h; cannot confirm runner still alive.
- Closed book still **86%** at **424** / **+$52.29**, but bankroll soft at last mark **$56.82** (**−$36.93** vs $93.75 day).
- Three `0545` opens (~$15 cash locked @09:39) should have settled ~09:45; absence of SETTLE/equity is the main gap (~14.3h).
- Cash-save to **$100** still far — last known cash **~$41.50–46.60**; floors off.
- Resume `closed=` ≠ filled equity-line `closed=424`; always prefer equity-line filled count.
- Bot $100 target VM still dark since **00:46** — leftover ledger **6–8 / −$15.80**; do not merge.
- **Ops:** wake DO OR DIE (or pull `state_live.json` / Kalshi balance) — now critical after ~14.4h dark post-wake.

---

## How the bot is working

**What's working (last confirmed @09:39)**
- Edge stack still printing high filled WR (**86%** on **424** closes) with closed PnL **+$52.29**.
- SPRINT cash-save armed at **$100** with floors disabled; last state `halted=False`, `SAVE False`, `PAUSED False`.
- Runner + watchdog + keep_alive were healthy at the 09:39 check (hb 0.7).

**What's not / risks**
- **No live telemetry for ~14.4h** — DO OR DIE IDLE; Bot $100 target frozen ~23.3h. Hourly **0–0 / $0** is absence-of-data, not confirmed flat trading.
- Bankroll last mark **$56.82** is **−$36.93** vs day $93.75 and **~$58.50** short of the $100 save after the 3rd fill.
- Three `0545` opens never showed a SETTLE in transcript (~14.3h overdue).
- Separate abandoned sprint ledger (**6–8 / −$15.80**) must not be merged into DO OR DIE.

**Bottom line:** Last confirmed book is **424 closes @ 86% / +$52.29**, equity **$56.82**. Since the prior hourly (and for ~14.4h total): **0–0 / $0**. Bot is **not confirmed live** — wake the DO OR DIE agent or refresh Kalshi balance to restore the tape.
