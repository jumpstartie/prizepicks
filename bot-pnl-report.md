# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~07:03 UTC (automation cron)  
**Data freshness:** **STALE (~3.5h / ~208m)** — newest full book still from [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`). Latest equity **[03:35:30]** `equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275`. Supervising agent last tool activity ~**03:35:40Z**; status still **IDLE**. **No new equity / fill / settle lines after 03:35:30** in the re-pulled transcript @07:03.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. No new marks after 00:46 (~6.3h stale). Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @07:03 via `batch-fetch-details`.  
**Bot status (last known):** **SPRINT mode** — `HALT_DISABLED=1`, `HALT_FLOOR=0`, `HALT_CASH_TARGET=$100` (lock & SAVE when flat cash ≥ $100); last cash **$49.81**, **2 opens**, `halted=False`. Runner left under keep_alive/watchdog at 03:35 — **liveness unverified since**.

---

## Headline

| Metric | Value |
|---|---|
| **Last known equity / cash** | **$58.59** / **$49.81** @03:35:30 (**2 opens**) |
| **Last known closed book (DO OR DIE)** | **421 closes · 86% · +$54.03** (~**362W–59L**) |
| **Cash-save target** | **$100** armed — gap **~$50.19** on flat cash (**not confirmed hit**) |
| **Prior report (PR #41 / 06:00)** | same mark **$58.59 / 421 / +$54.03**; sprint armed; already stale ~2.5h |
| **Δ vs prior report (06:06 → 07:03)** | **no confirmed change** — closed **421→421**, pnl **+$54.03→+$54.03**, equity print unchanged |
| **Hourly since ~06:06 cron** | **0–0 / $0** confirmed; transcript still dark after 03:35 |
| **Day equity vs $93.75 @10:00** | **−$35.16** at last mark **$58.59** |
| **vs start_equity ($61.54)** | **−$2.95** at last mark **$58.59** |
| **High-water** | **~$99.12** (pre-halt overnight) |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since 03:35 (~208m); Bot $100 target **IDLE** since ~00:46 (~377m) |

Live book source of truth remains **DO OR DIE**, but the mark is **unchanged for ~3.5 hours**. The 2345 BTC/XRP opens from 03:31–03:33 should have settled long ago if the runner stayed up; **no settle confirmation** is available without live workspace files. No newer live trading agent has appeared since 03:00 UTC.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30 (latest confirmed)** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@07:03 pull** | **421** | **86** | **362–59** | **+$54.03** | **unchanged (stale ~3.5h)** |

Exact latest confirmed line:
```
[03:35:30] equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275  unit=11.34  risk=18.0%(cut_neg_edge) edge_wr=83.1% ev=$-0.224
```

**Note:** resume logs show `closed=518` — that is **all** closed records (filled + unfilled). Equity-line **`closed=421`** is **filled** closes only; use **421 / +$54.03** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~6.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `421`. Prefer DO OR DIE filled closed book for live W/L; prefer last known cash/equity (**$49.81 / $58.59**) for bankroll until a fresher mark appears.

### Opens @03:35 (unconfirmed since)

| Market | Side | Entry ≈ | Size ≈ |
|---|---|---|---|
| `KXBTC15M-26AUG052345-45` | YES | 0.71 | ~6.18 contracts |
| `KXXRP15M-26AUG052345-45` | NO | 0.73 | ~6.02 contracts |

These windows should already be past; outcome **unknown** without a post-03:35 equity line.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–04:08** | **0–0 confirmed** | **$0 confirmed** | agent IDLE after sprint deploy |
| **04:08–05:06** | **0–0 confirmed** | **$0 confirmed** | transcript dark; no new marks |
| **05:06–06:06** | **0–0 confirmed** | **$0 confirmed** | still dark; mark age ~151m |
| **06:06–07:03 (this report’s hour)** | **0–0 confirmed** | **$0 confirmed** | still dark; mark age now ~208m |
| **Bot $100 VM 06:06–07:03** | **0–0** | **$0** | still frozen @$60.61 |

### Post-19:48 closes (unchanged vs PR #41)

| Time | Result | Trade | PnL |
|---|---|---|---|
| 20:00 | ~flat | PRE-SETTLE BTC NO 1600 | −$0.00 |
| 20:00 | W | PRE-SETTLE XRP NO 1600 | +$1.52 |
| 20:15 | ~flat | SETTLE BNB 1615 | +$0.00 |
| 20:15 | W | SETTLE XRP 1615 | +$2.15 |
| ~03:19–03:33 | W | XRP 2330 (inferred) | ≈+$1.20 |
| | **~+3W / +1L vs 19:48** | | **≈+$4.87** closed |

### 06:06→07:03 path (this report)

- **06:06 prior cron:** DO OR DIE still @03:35 — **$58.59 / 421 / 86% / +$54.03**; SPRINT $100 armed; already stale ~2.5h
- **07:03 pull:** re-fetched DO OR DIE transcript + Bot $100 transcript; scanned for any newer live trading agent since 03:00 — **none**
- **Result:** **identical last mark** `[03:35:30]`; supervising agent still IDLE (~208m); Bot $100 still `$60.61 / 14 / −$15.80`
- **Ops implication:** either the runner is printing only to gitignored local logs (not visible here), or the stack went quiet after IDLE — **2345 settle outcome not visible for a fourth consecutive hour**

**Net vs prior cron:** confirmed closed book / equity **unchanged**. True bankroll may have moved if opens settled offline.

### Risk / ops notes

- **Stale data remains the story** — fourth straight hourly report with **0–0 / $0** because the tape is dark, not because we saw flat trading.
- Sprint config last known: **no loss-floor stops**; only cash-save lock at **flat ≥ $100**. Gap was ≈ **$50** at last mark.
- Two opens at last mark (~BTC YES / XRP NO 2345) were mark risk — if they settled, cash should have moved off **$49.81**; we cannot see it.
- Resume `closed=518` ≠ filled `closed=421`; always prefer equity-line filled count.
- Bot $100 target VM still dark since **00:46** — leftover ledger **6–8 / −$15.80**; do not merge.
- **Ops:** wake DO OR DIE or inspect `bot/runner_live.log` / `bot/state_live.json` on that VM for a post-03:35 equity line.

---

## How the bot is working

**What's working**
- Lifetime filled book still strong at last mark: **421 / 86% / +$54.03**.
- Clear sprint plan was deployed @03:35: floors off, cash-save at **$100**.
- Abandoned Bot $100 VM correctly kept separate from the live 421 book.

**What's not / risks**
- **No confirmed activity for ~3.5 hours** after sprint deploy — hourly W/L is **0–0 / $0** only because the tape is dark.
- Supervising agent remains **IDLE** (~208m); runner liveness after 03:35 is **unverified**.
- Equity mark **$58.59** remains **−$35.16** vs morning **$93.75** and **−$17.87** vs 19:48 — bankroll soft at last print.
- Cash-save to **$100** not confirmed; last flat-cash gap was ~**$50.19**.
