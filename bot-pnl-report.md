# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~05:06 UTC (automation cron)  
**Data freshness:** **STALE (~90m)** — newest full book still from [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`). Latest equity **[03:35:30]** `equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275`. Supervising agent last tool activity ~**03:35:35Z**; status still **IDLE**. **No new equity / fill / settle lines after 03:35:30** in the re-pulled transcript @05:02–05:06.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. No new marks after 00:46. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @05:02–05:06 via `batch-fetch-details` (incl. start-logs; no post-03:35 runner prints).  
**Bot status (last known):** **SPRINT mode** — `HALT_DISABLED=1`, `HALT_FLOOR=0`, `HALT_CASH_TARGET=$100` (lock & SAVE when flat cash ≥ $100); last cash **$49.81**, **2 opens**, `halted=False`. Runner left under keep_alive/watchdog at 03:35 — **liveness unverified since**.

---

## Headline

| Metric | Value |
|---|---|
| **Last known equity / cash** | **$58.59** / **$49.81** @03:35:30 (**2 opens**) |
| **Last known closed book (DO OR DIE)** | **421 closes · 86% · +$54.03** (~**362W–59L**) |
| **Cash-save target** | **$100** armed — gap **~$50.19** on flat cash (**not confirmed hit**) |
| **Prior report (PR #39 / 04:00)** | same mark **$58.59 / 421 / +$54.03**; sprint armed |
| **Δ vs prior report (04:08 → 05:06)** | **no confirmed change** — closed **421→421**, pnl **+$54.03→+$54.03**, equity print unchanged |
| **Hourly since ~04:08 cron** | **0–0 / $0** confirmed; transcript dark after 03:35 |
| **Day equity vs $93.75 @10:00** | **−$35.16** at last mark **$58.59** |
| **vs start_equity ($61.54)** | **−$2.95** at last mark **$58.59** |
| **High-water** | **~$99.12** (pre-halt overnight) |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since 03:35; Bot $100 target **IDLE** since ~00:46 |

Live book source of truth remains **DO OR DIE**, but the mark is **unchanged for ~90 minutes**. The 2345 BTC/XRP opens from 03:31–03:33 should have settled by now if the runner stayed up; **no settle confirmation** is available without live workspace files.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30 (latest confirmed)** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@05:06 pull** | **421** | **86** | **362–59** | **+$54.03** | **unchanged (stale)** |

Exact latest confirmed line:
```
[03:35:30] equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275  unit=11.34  risk=18.0%(cut_neg_edge) edge_wr=83.1% ev=$-0.224
```

**Note:** resume logs show `closed=518` — that is **all** closed records (filled + unfilled). Equity-line **`closed=421`** is **filled** closes only; use **421 / +$54.03** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~4h20m |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `421`. Prefer DO OR DIE filled closed book for live W/L; prefer last known cash/equity (**$49.81 / $58.59**) for bankroll until a fresher mark appears.

### Opens @03:35 (unconfirmed since)

| Market | Side | Entry ≈ | Size ≈ |
|---|---|---|---|
| `KXBTC15M-26AUG052345-45` | YES | 0.71 | 4.39 |
| `KXXRP15M-26AUG052345-45` | NO | 0.73 | 4.39 |

These windows should already be past; outcome **unknown** without a post-03:35 equity line.

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–04:08 (prior hour)** | **0–0 confirmed** | **$0 confirmed** | agent IDLE after sprint deploy |
| **04:08–05:06 (this report’s hour)** | **0–0 confirmed** | **$0 confirmed** | transcript still dark; no new marks |
| **Bot $100 VM 04:08–05:06** | **0–0** | **$0** | still frozen @$60.61 |

### Post-19:48 closes (unchanged vs PR #39)

| Time | Result | Trade | PnL |
|---|---|---|---|
| 20:00 | ~flat | PRE-SETTLE BTC NO 1600 | −$0.00 |
| 20:00 | W | PRE-SETTLE XRP NO 1600 | +$1.52 |
| 20:15 | ~flat | SETTLE BNB 1615 | +$0.00 |
| 20:15 | W | SETTLE XRP 1615 | +$2.15 |
| ~03:19–03:33 | W | XRP 2330 (inferred) | ≈+$1.20 |
| | **~+3W / +1L vs 19:48** | | **≈+$4.87** closed |

### 04:08→05:06 path (this report)

- **04:08 prior cron:** DO OR DIE live @03:35 — **$58.59 / 421 / 86% / +$54.03**; SPRINT $100 armed; 2 opens
- **05:02–05:06 pull:** re-fetched DO OR DIE transcript + start-logs + Bot $100 transcript
- **Result:** **identical last mark** `[03:35:30]`; supervising agent still IDLE; Bot $100 still `$60.61 / 14 / −$15.80`
- **Ops implication:** either the runner is printing only to gitignored local logs (not visible here), or the stack went quiet after IDLE — **2345 settle outcome not visible**

**Net vs prior cron:** confirmed closed book / equity **unchanged**. True bankroll may have moved if opens settled offline.

### Risk / ops notes

- **Stale data is the story this hour** — not a PnL change.
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
- **No confirmed activity for ~90 minutes** after sprint deploy — hourly W/L is **0–0 / $0** only because the tape is dark, not because we saw flat trading.
- Supervising agent remains **IDLE**; runner liveness after 03:35 is **unverified**.
- Equity mark **$58.59** remains **−$35.16** vs morning **$93.75** and **−$17.87** vs 19:48 — bankroll soft at last print.
- Loss floors **off** in sprint mode if the runner is still alive.
- Parallel Bot $100 VM still abandoned/stale.

**Bottom line:** Last confirmed live book is still **DO OR DIE @03:35** — **421 closes / ~362–59 / +$54.03**, equity **$58.59**, cash **$49.81** with **2 opens**, sprinting to **$100** (~$50 short). **This hour: no new confirmed W/L or PnL** — data stale ~90m. Abandoned Bot $100 VM still **6–8 / −$15.80 @$60.61**. Need a live VM check to see whether the 2345 opens settled and where cash sits now.
