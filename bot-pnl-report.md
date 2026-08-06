# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~04:08 UTC (automation cron)  
**Data freshness:** **LIVE (DO OR DIE re-awake)** — newest full book from [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`). Latest equity **[03:35:30]** `equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275`. Supervising agent last tool activity ~**03:35:35Z**; status **IDLE** after deploying **SPRINT to $100**.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. No new marks after 00:46; runner liveness unverified since then. Treat as a separate reset ledger, **not** the live book.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @04:03–04:08 via `batch-fetch-details`.  
**Bot status (live):** **SPRINT mode** — `HALT_DISABLED=1`, `HALT_FLOOR=0`, `HALT_CASH_TARGET=$100` (lock & SAVE when flat cash ≥ $100); currently cash **$49.81**, **2 opens**, `halted=False`.

---

## Headline

| Metric | Value |
|---|---|
| **Live equity / cash** | **$58.59** / **$49.81** @03:35:30 (**2 opens**) |
| **Live closed book (DO OR DIE)** | **421 closes · 86% · +$54.03** (~**362W–59L**) |
| **Cash-save target** | **$100** armed — gap **~$50.19** on flat cash (**not hit**) |
| **Prior report (PR #38 / 03:00)** | Bot $100 frozen **$60.61 / 14 / −$15.80**; DO OR DIE wrongly treated as stale @19:48 |
| **Δ vs prior DO OR DIE mark (19:48)** | closed **417→421 (+4)**; pnl **+$49.16→+$54.03 (+$4.87)**; equity **$76.46→$58.59 (−$17.87)** |
| **Hourly since ~03:03 cron** | first new marks @**03:09**; then **+1W** close + **2 new opens**; latest **$58.59 / 421 / +$54.03** |
| **Day equity vs $93.75 @10:00** | **−$35.16** at **$58.59** |
| **vs start_equity ($61.54)** | **−$2.95** at **$58.59** |
| **High-water** | **~$99.12** (trail floor briefly halted @03:09 before floors disabled) |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge into 421 |
| **Agent status** | DO OR DIE **IDLE** after 03:35 sprint deploy (runner may still be up); Bot $100 target **IDLE** since ~00:46 |

Live book flipped back to **DO OR DIE**: overnight it continued settling while the supervising agent slept, hit a **loss-floor halt** at **$57.41** (~03:09), then was restarted in **no-stop $100 sprint** with **2 open legs** and flat cash **~$50**. The separate Bot $100 flat VM remains dark.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30 (latest)** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |

Exact latest line:
```
[03:35:30] equity=$58.59 cash=$49.81 open=2 closed=421 win%=86 pnl=+54.0275  unit=11.34  risk=18.0%(cut_neg_edge) edge_wr=83.1% ev=$-0.224
```

**Note:** resume logs show `closed=518` — that is **all** closed records (filled + unfilled). Equity-line **`closed=421`** is **filled** closes only; use **421 / +$54.03** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~3h20m |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `421`. Prefer DO OR DIE filled closed book for live W/L; prefer live cash/equity (**$49.81 / $58.59**) for bankroll.

### Opens @03:35

| Market | Side | Entry ≈ | Size ≈ |
|---|---|---|---|
| `KXBTC15M-26AUG052345-45` | YES | 0.71 | 4.39 |
| `KXXRP15M-26AUG052345-45` | NO | 0.73 | 4.39 |

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles clustered ~20:00–20:15; then quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:03–04:08 (this report’s hour)** | **+1W** after first mark @03:09; **2 opens still live** | closed book **+$1.20** from halt mark; equity **$57.41→$58.59** | prior cron had **no** DO OR DIE marks (thought stale) |
| **Bot $100 VM 03:03–04:08** | **0–0** | **$0** | still frozen @$60.61 |

### Post-19:48 closes (journal @03:09)

| Time | Result | Trade | PnL |
|---|---|---|---|
| 20:00 | ~flat | PRE-SETTLE BTC NO 1600 | −$0.00 |
| 20:00 | W | PRE-SETTLE XRP NO 1600 | +$1.52 |
| 20:15 | ~flat | SETTLE BNB 1615 | +$0.00 |
| 20:15 | W | SETTLE XRP 1615 | +$2.15 |
| ~03:19–03:33 | W | XRP 2330 (inferred) | ≈+$1.20 |
| | **~+3W / +1L vs 19:48** | | **≈+$4.87** closed |

### 03:03→04:08 path (this report)

- **03:00 prior cron:** treated DO OR DIE as stale @19:48; Bot $100 frozen @$60.61
- **03:09:** DO OR DIE equity reappears — **loss_floor halt** at **$57.41** (`closed=420 / +$52.83`); API health cash briefly looked **$71.88** vs state **$57.41** (desync caveat)
- **03:19–03:35:** floors disabled / **SPRINT $100** armed; filled XRP 2330 + opened BTC YES / XRP NO 2345
- **03:35:30 latest:** **$58.59 / $49.81 / open=2 / closed=421 / +$54.03**
- **No newer marks after 03:35:30** in transcript; supervising agent went **IDLE**

**Net vs prior cron’s DO OR DIE snapshot (19:48 → 03:35):** flat equity **$76.46 → $58.59 (−$17.87)**; closed PnL **+$49.16 → +$54.03 (+$4.87)**; closes **+4**.

### Risk / ops notes

- **Live source of truth is DO OR DIE again**, not the abandoned Bot $100 flat VM.
- Sprint config: **no loss-floor stops**; only cash-save lock at **flat ≥ $100**. Gap ≈ **$50**.
- Two opens (~BTC YES / XRP NO 2345) carry mark risk — equity **$58.59** vs cash **$49.81**.
- At 03:09 halt, state cash **$57.41** vs API health **$71.88** — treat mid-halt cash prints carefully; latest post-sprint snaps show cash **$49.81**.
- Resume `closed=518` ≠ filled `closed=421`; always prefer equity-line filled count.
- Bot $100 target VM still dark since **00:46** — leftover ledger **6–8 / −$15.80**; do not merge.
- **Ops:** confirm DO OR DIE `runner.py` still alive under IDLE supervisor; 2345 window may already be settling.

---

## How the bot is working

**What's working**
- Lifetime filled book still strong: **421 / 86% / +$54.03**.
- Bot recovered from overnight quiet + loss-floor halt and is back in a defined **$100 cash-save sprint**.
- Closed PnL improved **+$4.87** since 19:48 even while equity mark fell (open risk / MTM / cash path).

**What's not / risks**
- Equity mark **$58.59** is **−$17.87** vs 19:48 and **−$35.16** vs morning **$93.75** — bankroll is soft.
- Loss floors are **off** in sprint mode; only the **$100** save remains. A bad settle on the 2 opens can cut cash further with no trail halt.
- Supervising agent is **IDLE** again after 03:35 — runner liveness after that minute is **unverified**.
- Parallel Bot $100 VM is abandoned/stale and can confuse reporting if merged.
- Halt-time API vs state cash desync needs watching on the next live pull.

**Bottom line:** Live book is **DO OR DIE @03:35** — **421 closes / ~362–59 / +$54.03**, equity **$58.59**, cash **$49.81** with **2 opens**, sprinting to **$100** (~$50 short). Hourly since prior cron: DO OR DIE reappeared, **+1 filled win** after halt, then re-risked with 2 opens. Abandoned Bot $100 VM still **6–8 / −$15.80 @$60.61** — ignore for live totals.
