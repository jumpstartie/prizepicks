# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~11:02 UTC (automation cron)  
**Data freshness:** **FRESH (~5 min)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) woke ~10:54–10:57Z after ~25h silence. Newest filled equity **[10:56:42]** `equity=$52.99 cash=$40.28 open=3 closed=430 win%=86 pnl=+48.4790`. Supervising agent last activity **~10:57:17Z**; status **IDLE** (runner still logging through 10:57:09).  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~34.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @11:02 via `batch-fetch-details`. DO OR DIE transcript **CHANGED** (+160,735 bytes / +2,246 lines vs 10:01). No newer live trading agent found.  
**Bot status (last confirmed @10:56–10:57):** Redeployed with **halt floor $25** / cash_target OFF (SPRINT $100 briefly armed at wake @10:54:50 then overridden). Runner pid **235604** + keep_alive **235438** + watchdog **235461**; `halted=False`; SAVE False; PAUSED False. After equity mark, SOL fill left cash **$33.39** with **~4 opens** on the `0700` window.

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$52.99** / **$40.28** @10:56:42 (**3 opens** at mark; then SOL fill → **~$33.39** cash / ~**4 opens**) |
| **Latest closed book (DO OR DIE)** | **430 closes · 86% · +$48.48** (~**370–60**) |
| **Cash-save / halt** | SPRINT $100 briefly at wake; final mode **halt if equity ≤ $25**; SAVE not hit |
| **Prior report (PR #68 / 10:00)** | **$56.82 / 424 / +$52.29** @09:39 (STALE) |
| **Δ vs prior report** | closed **424→430 (+6)**; closed pnl **−$3.81**; equity **−$3.83** |
| **Hourly since ~10:01 cron** | **+6 closes / closed PnL −$3.81** — wake + gap catch-up; only 1 SETTLE on-log |
| **Day equity vs $93.75 @10:00** | **−$40.76** at last mark **$52.99** |
| **vs start_equity ($61.54)** | **−$8.55** at last mark **$52.99** |
| **High-water** | state briefly still showed **56.8223**, then **~40.28** after restart |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since ~10:57 (~5 min); Bot $100 target **IDLE** since ~00:46 (~34.3h) |
| **Transcript** | **CHANGED** — **10,226,162** bytes / **94,319** lines (was 10,065,427 / 92,073); last bot ts **10:57:09** |

Live book source of truth remains **DO OR DIE**. After ~25 consecutive stale hourlies, the supervising transcript advanced with a settle, redeploy, and new `0700` fills. The three prior `0545` opens still have **no SETTLE lines** in tape (likely closed off-log during the gap — closed jumped 424→430).

---

## How the bot is working (profit read)

Closed hit rate still strong (**86%**, ~**370–60**), but lifetime closed PnL **softened** to **+$48.48** (was **+$52.29**) and bankroll is lower at last mark (**$52.99** equity, **−$40.76** vs the $93.75 day print, **−$8.55** vs `$61.54` start). The bot is **alive again**: wake @10:54 settled a BNB loss, opened BTC/BNB/(+1) on `0700`, redeployed with a **$25 equity floor**, then filled SOL — cash down to **~$33.39**. Profit figures below are a **fresh ~5 min** snapshot; `0700` opens not yet settled.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 Aug 6** | **424** | **86** | **~365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@10:56:42 Aug 7 (latest confirmed)** | **430** | **86** | **~370–60** | **+$48.48** | **$52.99** / $40.28 open3 |

Exact latest confirmed equity line:
```
[10:56:42] equity=$52.99 cash=$40.28 open=3 closed=430 win%=86 pnl=+48.4790  unit=7.40  risk=13.0%(cut_neg_edge) edge_wr=71.8% ev=$-0.434
```

**Note:** resume logs still show higher `closed=` counts (e.g. `closed=527`). Equity-line **`closed=430`** is **filled** closes only; use **430 / +$48.48** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~34.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `430`.

### Opens last known @10:56–10:57 (`0700` window)

| Time | Market | Side | Entry ≈ | Size ≈ | Cash after |
|---|---|---|---|---|---|
| 10:54:51 | `KXBTC15M-26AUG070700-00` | YES | ~0.83 | 9.58 | $45.04 |
| 10:55:30 | `KXBNB15M-26AUG070700-00` | NO | ~0.71 | 6.71 | $40.28 |
| (unknown 3rd open at equity mark — XRP order @10:55:18 logged fill=0.0) | — | — | — | — | — |
| 10:57:05 | `KXSOL15M-26AUG070700-00` | YES | ~0.85 | 8.10 | **$33.39** |

Post-mark: SOL fill @10:57:05 → cash **$33.39**; DOGE signals skipping soft corr cap. `0700` settle expected ~11:00 — **not yet** in this pull.

### Prior 0545 opens (still no SETTLE in tape)

| Time | Market | Side | Note |
|---|---|---|---|
| 09:39:00 | `KXBNB15M-26AUG060545-45` | YES | no SETTLE line later |
| 09:39:00 | `KXXRP15M-26AUG060545-45` | NO | no SETTLE line later |
| 09:39:14 | `KXBTC15M-26AUG060545-45` | NO | no SETTLE line later |

Closed jumped **424→430** across the gap; fate of these three is inferred closed off-log, not visible as SETTLE strings.

### FILL / LIVE FILL / SETTLE in new wake window

```
[10:54:40] SETTLE KXBNB15M-26AUG060600-00 NO LOSS pnl=-4.8720 markout/c=-0.840  cash=$52.99 equity=$62.67 risk=18.0% bn=flat:-0.003% dir=up
[10:54:51] LIVE FILL YES 9.58 @ ~0.83 on KXBTC15M-26AUG070700-00 status=executed cash=$45.04 risk=18.0% bn=up
[10:55:30] LIVE FILL NO 6.71 @ ~0.71 on KXBNB15M-26AUG070700-00 status=executed cash=$40.28 risk=18.0% bn=flat
[10:57:05] LIVE FILL YES 8.10 @ ~0.85 on KXSOL15M-26AUG070700-00 status=executed cash=$33.39 risk=13.0% bn=flat
```

No SETTLE after **10:54:40**. No further FILL after **10:57:05**.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03** | **+3 closes** (421→424) | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **10:03 Aug 6 – 10:01 Aug 7** | **0–0** | **$0** | STALE — identical 09:39 mark (PRs #45–#68) |
| **10:01–11:20 (this report)** | **+6 closes** (424→430) | closed **−$3.81**; equity **−$3.83** | wake @10:54; 1 on-log SETTLE (BNB −4.87); +5 closes off-log in gap |
| **Bot $100 VM 10:01–11:20** | **0–0** | **$0** | still frozen @$60.61 |

### 10:01→11:20 path (this report)

- **10:01 prior cron (PR #68):** DO OR DIE **STALE** @09:39 — **$56.82 / 424 / 86% / +$52.29**; cash → **~$41.50** / open **3** after BTC fill; sprint armed
- **11:02 pull:** DO OR DIE transcript **advanced** — wake settle + redeploy + `0700` fills; newest filled mark **$52.99 / 430 / +$48.48**; Bot $100 still @00:46; transcript now **10.23 MiB / 10226162 bytes / 94319 lines**
- **No newer live trading agent** besides DO OR DIE (desktop/mobile/web/cli scan: only these two + this automation)

**Net vs prior cron:** **+6 closes / −$3.81 closed PnL / −$3.83 equity** — bot live again; `0700` opens still open at pull.

### Risk / ops notes

- **Alive again** after ~25h supervising silence; last log **10:57:09**; freshness **~5 min**.
- Closed book still **86%** at **430** / **+$48.48**, bankroll soft at **$52.99** (**−$40.76** vs $93.75 day).
- Mode shift: SPRINT $100 at wake → final deploy **halt floor $25** / cash_target OFF; SAVE not hit (cash ~$33.39 after SOL).
- Only **1** SETTLE on-log in the new window; closed +6 implies **5 gap settles** not printed — treat hourly W–L as closed-count delta, not fully tape-attributed.
- Events file: prior PR/artifact history; trading activity is in transcript tool outputs.
