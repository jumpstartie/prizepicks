# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-06 ~10:03 UTC (automation cron)  
**Data freshness:** **LIVE / FRESH (~24m)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) re-awoke. Newest equity **[09:39:01]** `equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886`. Supervising agent last activity **~09:39:24Z**; status **IDLE** after confirming sprint still live. Prior six hourly reports were stuck on the **03:35** mark — that dark stretch is now closed by this print.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~9.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @10:03 via `batch-fetch-details` (~10.1MB / 4589 msgs; ends cleanly).  
**Bot status (confirmed @09:39):** **SPRINT mode live** — `HALT_DISABLED=1`, `HALT_CASH_TARGET=$100`, `HALT_FLOOR` off / halt=$0; runner + watchdog + keep_alive present; `halted=False`. After the equity print, a 3rd fill left cash **~$41.50** with **3 opens** on the `0545` window.

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$56.82** / **$46.60** @09:39:01 (**2 opens** at mark; then **3 opens / ~$41.50** cash) |
| **Latest closed book (DO OR DIE)** | **424 closes · 86% · +$52.29** (~**364–60 to 365–59**) |
| **Cash-save target** | **$100** armed — gap **~$53.40** on mark cash / **~$58.50** after 3rd fill (**not hit**) |
| **Prior report (PR #44 / 09:00)** | stale **$58.59 / 421 / +$54.03** @03:35 |
| **Δ vs prior report (03:35 → 09:39)** | closed **421→424 (+3)**; closed pnl **+$54.03→+$52.29 (−$1.74)**; equity **$58.59→$56.82 (−$1.77)** |
| **Hourly since ~09:03 cron** | **+3 closes / closed PnL −$1.74** (catch-up after dark period + new `0545` fills); exact settle W–L not in tape |
| **Day equity vs $93.75 @10:00** | **−$36.93** at **$56.82** |
| **vs start_equity ($61.54)** | **−$4.72** at **$56.82** |
| **High-water** | **~$99.12** (pre-halt overnight); state `hw 56.8223` post-wake |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** after 09:39 wake (~24m); Bot $100 target **IDLE** since ~00:46 (~9.3h) |

Live book source of truth remains **DO OR DIE**. The runner was dark to this automation for ~6h, then **re-confirmed live @09:39** with three new `0545` fills and a filled closed book at **424 / +$52.29**.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30 (prior stale mark)** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 (latest confirmed)** | **424** | **86** | **~364–60 / 365–59** | **+$52.29** | **$56.82** / $46.60 open2 |

Exact latest confirmed line:
```
[09:39:01] equity=$56.82 cash=$46.60 open=2 closed=424 win%=86 pnl=+52.2886  unit=10.99  risk=18.0%(edge_kelly) edge_wr=86.2% ev=$+0.125
```

**Note:** resume logs still show higher `closed=` counts for filled+unfilled history. Equity-line **`closed=424`** is **filled** closes only; use **424 / +$52.29** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~9.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `424`.

### Opens after 09:39 wake

| Time | Market | Side | Entry ≈ | Size ≈ | Cash after |
|---|---|---|---|---|---|
| 09:39:00 | `KXBNB15M-26AUG060545-45` | YES | ~0.70 | 7.30 | $46.60 |
| 09:39:00 | `KXXRP15M-26AUG060545-45` | NO | ~0.73 | 7.00 | $46.60 |
| 09:39:14 | `KXBTC15M-26AUG060545-45` | NO | ~0.87 | 5.87 | **$41.50** |

Post-mark state peek: `cash 41.4954 halted False open 3 hw 56.8223`. `0545` window should settle ~09:45 — outcome **not yet** in this pull (no SETTLE lines after 09:39).

Dark-period path (03:35 → 09:38 restart): cash recovered from **$49.81 / 2 opens** to flat restart bankroll **$51.71** with filled closed **421→424** and closed pnl **+$54.03→+$52.29**. Intermediate SETTLE lines were **not** captured in the supervising transcript (no 422/423 equity prints).

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03 (this report’s hour)** | **+3 closes** (421→424); ≈**1–2 losers in mix** | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **Bot $100 VM 09:03–10:03** | **0–0** | **$0** | still frozen @$60.61 |

### Post-19:48 closes (updated)

| Time | Result | Trade | PnL |
|---|---|---|---|
| 20:00 | ~flat | PRE-SETTLE BTC NO 1600 | −$0.00 |
| 20:00 | W | PRE-SETTLE XRP NO 1600 | +$1.52 |
| 20:15 | ~flat | SETTLE BNB 1615 | +$0.00 |
| 20:15 | W | SETTLE XRP 1615 | +$2.15 |
| ~03:19–03:33 | W | XRP 2330 (inferred) | ≈+$1.20 |
| **03:35→09:39 (dark)** | **+3 closes** (detail unknown) | net closed | **−$1.74** |
| | **~+6 closes vs 19:48** | | **≈+$3.13** closed (49.16→52.29) |

### 09:03→10:03 path (this report)

- **09:03 prior cron:** DO OR DIE still stuck @03:35 — **$58.59 / 421 / 86% / +$54.03**; STALE ~5.5h; hourly **0–0 / $0**
- **10:03 pull:** re-fetched DO OR DIE transcript — **new activity @09:38–09:39**:
  - `[09:38:59] SPRINT mode… now $51.71`
  - three LIVE FILLs on `0545` BNB/XRP/BTC
  - `[09:39:01] equity=$56.82 … closed=424 … pnl=+52.2886`
  - final assistant: sprint live, cash ~$41.50, 3 opens, target $100
- **Bot $100:** unchanged `$60.61 / 14 / −$15.80`
- **No newer live trading agent** besides DO OR DIE

**Net vs prior cron:** first confirmed book move since 03:35 — **+3 closes, −$1.74 closed PnL, −$1.77 equity**.

### Risk / ops notes

- **Tape is live again** — sprint config confirmed (`HALT_DISABLED=1`, cash-save **$100**).
- Closed book still strong on win rate (**86%**) but lifetime closed PnL slipped **~$1.74** during the dark catch-up; equity **$56.82** is soft vs morning **$93.75** (**−$36.93**).
- Three fresh `0545` opens (~$15 of cash locked) are mark risk until ~09:45 settle — not yet reflected beyond cash **$41.50**.
- Cash-save gap widened (~**$53–59** depending on open mark) vs ~$50 at the old 03:35 print.
- Resume `closed=` ≠ filled equity-line `closed=424`; always prefer equity-line filled count.
- Bot $100 target VM still dark since **00:46** — leftover ledger **6–8 / −$15.80**; do not merge.
- **Ops:** next cron should look for `0545` SETTLE lines and any post-09:39 equity print.

---

## How the bot is working

**What's working**
- Runner **re-confirmed alive** @09:39 after ~6h of supervising-agent silence — watchdog/keep_alive/runner present; sprint still armed.
- Lifetime filled win rate still **86%** at **424** closes.
- Immediate post-wake quoting worked: three `0545` favorites filled within ~15s.
- Abandoned Bot $100 VM correctly kept separate from the live **424** book.

**What's not / risks**
- Dark-period settles (**+3 closes / −$1.74**) have **no SETTLE detail** in the transcript — only the catch-up equity print.
- Bankroll soft: equity **$56.82** (**−$36.93** vs $93.75 day mark; **−$4.72** vs start $61.54; **−$19.64** vs 19:48).
- Cash-save to **$100** not close — ~**$41.50–46.60** cash with opens; floors remain off so drawdowns can continue.
- Three open `0545` contracts are unresolved in this pull; next mark will move cash/equity again.
