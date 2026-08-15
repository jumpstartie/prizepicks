# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-15 ~03:01 UTC (automation cron)  
**Data freshness:** preferred filled equity mark still **STALE (~182.51h)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled-444 equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Live reset book still **HALTED** at **[19:40:33]** `equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299` (~127.35h). Agent **IDLE** after LMA **10:19:05Z** (~40.71h before pull). Transcript **UNCHANGED** vs 02:05 — **no new Kalshi fills**. Sniper **JOEVER** transcript mark still **~0.90x / ≈ −$2.09**; live public refresh this hour **~$17,121 mcap (0.823x) / mark ≈ $25.34 / ≈ −$5.47** (Δ ≈ **$0.00** vs 02:05 live −$5.47).  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~218.24h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @03:01 via `batch-fetch-details` (`2026-08-15T03-01-28Z-97df`). DO OR DIE transcript **UNCHANGED** vs 02:05 — **12,674,261** bytes / **115,958** lines; md5 `8ea94a66f72689347512b87e1d718f53`. Draft events PR **#126**.  
**Bot status (live Kalshi):** Preferred mid-band reset remains **HALTED** at floor **$20**. Separate **$0.08** micro restart still floor-halted with **closed=0** — do **not** merge into filled 444 or reset 32. Sniper still held in **JOEVER**.

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash (preferred lifetime)** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE ~182.51h** |
| **Latest closed book (DO OR DIE filled)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Latest live mark (reset book)** | **$43.65** / cash **$39.64** / open **2** / closed **32** / win% **41** / pnl **−$11.43** — **HALTED** @19:40 (**unchanged**) |
| **Live ops this hour** | Preferred Kalshi books **flat**; transcript **UNCHANGED**; agent **IDLE** (LMA **10:19:05Z**) |
| **Cash-save / halt** | preferred reset: **halt if equity ≤ $20** still **TRIGGERED**; micro book still floor-halted at **$0.08** |
| **Prior report (02:05 / PR #245)** | **$61.71 / 444 / +$57.18** filled; live **$43.65 HALTED / 32 / −$11.43** |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~02:05 cron (filled book)** | **0–0 / $0** on preferred filled counters |
| **Hourly live reset book** | **0–0 / $0**; still **HALTED** at **$43.65 / $39.64** |
| **Day equity vs $93.75 @12:00** | filled mark **−$32.04** ($61.71); live mark **−$50.10** ($43.65) |
| **vs start_equity ($61.54)** | filled **+$0.17**; live **−$17.89** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** (LMA **10:19:05Z**, ~40.71h); Bot $100 target **IDLE** since ~00:46 (~218.24h) |
| **Transcript** | **UNCHANGED** — **12,674,261** bytes / **115,958** lines; md5 `8ea94a66f72689347512b87e1d718f53` |
| **Sniper JOEVER (open)** | transcript **~$18,711 (0.90x) / ≈ −$2.09**; live refresh **~$17,121 (0.823x) / ≈ −$5.47** (Δ ≈ **$0.00** vs 02:05 live) |

Live book source of truth for **lifetime closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). Current live bankroll posture for the Aug-9 mid-band session remains the **halted reset mark** (**$43.65 / $39.64 cash**). The **$0.08** restart remains a separate dust ledger.

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — still **+$0.17** vs start equity (`$61.54`), **−$32.04** vs the $93.75 day high.

**Preferred Kalshi books did not trade since the prior cron.** Filled `closed=444` and live reset `closed=32` are unchanged. DO OR DIE transcript fingerprint is identical to the 02:05 pull (no new Kalshi equity prints, fills, or settles). Gap since last successful report is ~0.93h (02:05 → 03:01).

Carry-forward (still current):

1. **Micro Kalshi restart @11:23** — engine came up at **equity=$0.08 / closed=0**, hit halt floor **$20** immediately (`HALT RUN`), then SAVE_BANKROLL / STOPPED. No FILL/SETTLE. Treat as a failed dust restart, not a new lifetime book.
2. **Sniper roll** — ASADO dust position sold earlier; **JOEVER** still held (**1,525,462** tokens). Entry mcap **$20,814**; last transcript mark **~$18,711 (0.90x, ≈ −$2.09)** on ~$30.81 entry / $28.72 mark. Live public refresh @03:01 (DexScreener): mcap **~$17,121 (0.823x)**, mark ≈ **$25.34**, unrealized ≈ **−$5.47** (Δ ≈ **$0.00** vs 02:05 live −$5.47). TP **2.8x** / SL **0.45x**. No exit / no new sniper trade in the agent transcript.
3. Agent LMA still **10:19:05Z** (~40.71h before pull); status remains **IDLE**.

Ops read: historical filled book still profitable on paper (**+$57.18 / 444**), live Aug-9 cash still ~**$40** and halted underwater (**−$11.43 / ~13–19**), preferred Kalshi deltas since prior cron still **flat**, and sniper JOEVER still open with an **unchanged** live mark this hour (~**−$5.47** unrealized).

---

## Total win / loss

### Live lifetime book (DO OR DIE — filled equity source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 Aug 6** | **424** | **86** | **~365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@10:56:42 Aug 7** | **430** | **86** | **~370–60** | **+$48.48** | **$52.99** / $40.28 open3 |
| **@11:16:02 Aug 7** | **438** | **86** | **~377–61** | **+$55.92** | **$60.42** / $60.42 flat |
| **@12:30:53 Aug 7 (latest confirmed filled)** | **444** | **86** | **~382–62** | **+$57.18** | **$61.71** / **$61.71** flat |
| **@16:16 Aug 9 – 02:05 Aug 15** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark **$61.71**; live reset **HALTED** |
| **@03:01 Aug 15 (this pull)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark still **$61.71**; **live reset** still **$43.65 / $39.64 / HALTED** |

Exact latest confirmed filled equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

Newest live reset-book equity line (unchanged):
```
[19:40:33] equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299  unit=7.04  risk=15.0%(cut_neg_edge) edge_wr=43.3% ev=$-0.619  HALTED
```

Newest micro-restart equity lines (separate dust ledger — do **not** merge):
```
[11:23:05] equity=$0.08 cash=$0.08 open=0 closed=0  unit=0.01  risk=15.0%(prior_no_samples+halt_cap)
[11:23:27] equity=$0.08 cash=$0.08 open=0 closed=0  unit=0.01  risk=15.0%(prior_no_samples+halt_cap)
```

**Note:** resume logs can show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only for the lifetime OG#3 book. The **`closed=32`** lines are a **reset mid-band ledger**. The **`closed=0` / $0.08** lines are a third dust restart — report separately; do **not** replace 444 or 32.

### Reset mid-band ledger (live — separate from filled 444)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:29:35** | **31** | **42** | **~13–18** | **−$9.34** | **$43.75** / $41.65 open1 |
| **@19:36–19:40 (HALTED)** | **32** | **41** | **~13–19** | **−$11.43** | trough **$12.57** → mark **$43.65** / $39.64 open2 |
| **@02:05 Aug 15** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |
| **@03:01 Aug 15 (this pull)** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |

Last on-log Aug9 Kalshi settle (from earlier; none new since prior cron on the preferred books):
```
[19:30:21] SETTLE KXBNB15M-26AUG091530-30 NO LOSS pnl=-2.0919 markout/c=-0.570  cash=$41.65 equity=$41.65 risk=15.0% bn=flat:+0.000% dir=up
```

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~218.24h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444` (or onto reset `32`).

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @19:40 (still current preferred live):** **open=2**, cash **$39.64**, equity **$43.65**, **HALTED**.  
**Micro @11:23:** open **0**, cash/equity **$0.08**, immediately floor-halted.

### FILL / LIVE FILL / SETTLE in window since prior cron

**Filled-444 book:** still **0** new preferred filled closes after `[12:30:53]`.  
**Live Aug9 tape after `[19:40:33]`:**
- **0×** new FILL / LIVE FILL / true SETTLE on preferred books since prior cron (transcript unchanged)
- After first `[19:40:33]`: equity **6** (reprints + $0.08 lines); FILL **1** (historical in tail, not new this hour); LIVE FILL **0**; SETTLE **0**; PRE-SETTLE **10**; HALTED on equity **2**
- After first `[12:30:53]`: equity lines **12**; FILL **1**; LIVE FILL **2**; SETTLE **1**; PRE-SETTLE **62**; HALTED on equity **6**

Mode last visible (preferred reset mid-band @19:31–19:40; still in force for that book):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **~7.04**, risk **15.0%** (`cut_neg_edge`), band **[0.45, 0.70)**
- **`halted=True`** after floor breach; no unhalt that restored the $43.65 book
- restart bankroll last seen **$37.56**

Micro restart mode (@11:23; separate):
- halt floor **$20**; cash_target **$60** SAVE armed; unit **0.01**; risk **15%** (`prior_no_samples+halt_cap`)
- immediately **HALT RUN** → SAVE_BANKROLL / STOPPED

Sniper (transcript unchanged; live mark refreshed):
- **JOEVER held** — **1,525,462** tokens; entry mcap **$20,814**
- Transcript last known: mark **~$18,711 (0.90x, ≈ −$2.09)** on entry_usd **$30.81** / mark_usd **$28.72**
- Live public refresh @03:01 (DexScreener): mcap **~$17,121 (0.823x)** / mark ≈ **$25.34** / unrealized ≈ **−$5.47** (Δ ≈ **$0.00** vs 02:05 live −$5.47)
- TP **2.8x** / SL **0.45x**; no exit / no new sniper buys in transcript

---

## Hourly win / loss (preferred filled book)

| Window | ≈W–L | Closed Δ | Closed PnL Δ | Equity Δ | Notes |
|---|---|---|---|---|---|
| **Prior cron ~02:05 → this ~03:01** | **0–0** | **+0** (444→444) | **+$0.00** | **+$0.00** ($61.71→$61.71) | preferred Kalshi flat; transcript UNCHANGED (~0.93h gap) |
| **Live reset same window** | **0–0** | **+0** (32→32) | **+$0.00** | **+$0.00** ($43.65→$43.65) | still **HALTED**; open **2** unchanged |
| **Micro restart ($0.08)** | **0–0** | **+0** (0→0) | **+$0.00** | dust **$0.08** | still floor-halted; do not merge |
| **Abandoned Bot $100 same window** | **0–0** | **+0** (14→14) | **+$0.00** | **+$0.00** ($60.61) | still frozen; do not merge |
| **Sniper JOEVER (unrealized)** | — | open held | — | live mark **≈ $0.00** vs 02:05 live | transcript still **0.90x / −$2.09**; live **0.823x / −$5.47** |

**Hourly summary:** filled **0–0 / $0**; live reset **0–0 / $0**; abandoned **0–0 / $0**. Sniper JOEVER still open; live mark **flat** (~**−$5.47**, Δ ≈ **$0.00**) vs last report’s live refresh.

---

## Verdict

DO OR DIE is **IDLE** with an **unchanged** transcript. Preferred lifetime book remains **+$57.18 / 444 closes / 86%** at filled equity **$61.71**. Live Aug-9 reset book remains **HALTED** at **$43.65 / −$11.43 / 32 closes**. Kalshi W/L and closed PnL since the prior cron are **flat**. Sniper JOEVER unrealized live mark ≈ **−$5.47** (Δ ≈ **$0.00** vs prior live −$5.47).
