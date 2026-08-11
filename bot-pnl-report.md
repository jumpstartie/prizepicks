# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-11 ~21:21 UTC (automation cron)  
**Data freshness:** preferred filled equity mark still **STALE (~104.85h)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled-444 equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent still **IDLE** (`lastMessageActivity` **14:03:51Z**, ~31.30h vs pull). Transcript **UNCHANGED** vs 19:20 — **no new Kalshi equity / FILL / SETTLE** after the **[19:40:33] HALTED** mark; ASADO still held with **$0 realized** (mark ~0.955–0.957x, unrealized ≈ −$0.01).  
**Live reset book:** still **HALTED** — newest live mark **[19:40:33]** `equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299 HALTED` (**unchanged** vs 19:20; ~49.69h since Aug 9 evening).  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~140.59h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @21:21 via `batch-fetch-details` (`2026-08-11T21-21-06Z-23a3` / `2026-08-11T21-21-06Z-8f0e`). DO OR DIE transcript **UNCHANGED** (11,759,771 bytes / 108,368 lines; md5 `7b1aac42770c59e5fe5ac1c83964873f`). Draft events PR **#126**.  
**Bot status (live Kalshi):** Mid-band EV printer remains **HALTED** at floor **$20**. Index shows agent **IDLE**; no unhalt / redeploy / new Kalshi tape. Sniper position still open; last mark refresh still ~14:03 Aug 10 (ASADO ~0.955–0.957x).

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash (preferred lifetime)** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE ~104.85h** |
| **Latest closed book (DO OR DIE filled)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Latest live mark (reset book)** | **$43.65** / cash **$39.64** / open **2** / closed **32** / win% **41** / pnl **−$11.43** — **HALTED** @19:40 (**unchanged**) |
| **Live ops this hour** | Transcript **UNCHANGED**; **0** new Kalshi FILL/SETTLE/equity after 19:40; agent **IDLE** (LMA still 14:03 Aug 10); sniper still holding ASADO ~**0.955–0.957x**, **$0 realized** |
| **Cash-save / halt** | **halt if equity ≤ $20** — still **TRIGGERED**; cash_target OFF; SPRINT OFF |
| **Prior report (19:20 / PR #172)** | **$61.71 / 444 / +$57.18** filled; live **$43.65 HALTED / 32 / −$11.43** |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~19:20 cron (filled book)** | **0–0 / $0** on preferred filled counters |
| **Hourly live reset book** | **0–0 / $0**; still **HALTED** at **$43.65 / $39.64** |
| **Day equity vs $93.75 @12:00** | filled mark **−$32.04** ($61.71); live mark **−$50.10** ($43.65) |
| **vs start_equity ($61.54)** | filled **+$0.17**; live **−$17.89** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** (LMA **14:03:51Z**, ~31.30h); Bot $100 target **IDLE** since ~00:46 (~140.59h) |
| **Transcript** | **UNCHANGED** — **11,759,771** bytes / **108,368** lines; md5 `7b1aac42770c59e5fe5ac1c83964873f` |

Live book source of truth for **lifetime closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). Current live bankroll posture remains the **halted reset mark** (**$43.65 / $39.64 cash**).

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — still **+$0.17** vs start equity (`$61.54`), **−$32.04** vs the $93.75 day high.

**Kalshi trading is still idle on-tape.** After the 19:29–19:42 reset/mid-band wake (BNB NO loss −$2.09, equity trough $12.57, halt floor $20), there are still **no new Kalshi settles or equity prints** after **19:40**. This hour the transcript is **byte-identical** to the 19:20 pull: no new sniper Update and **no Kalshi unhalt**. The supervising agent remains **IDLE** (last activity still the ~14:03 Aug 10 sniper status check; ~31.30h idle). ASADO is still open at **~0.955–0.957x** (mcap ~$2,138–$2,141), TP 2x / stop-loss off, **no sells**, **no realized sniper PnL**.

Ops read: historical filled book still profitable on paper (**+$57.18 / 444**), but **live cash is still ~$40**, the mid-band reset ledger is still **halted underwater (−$11.43 / ~13–19)**, and current activity is sniper position monitoring (draft PR **#126**), not Kalshi. Further Kalshi PnL needs an unhalt / redeploy that actually lands new tape.

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
| **@16:16 Aug 9 – 19:20 Aug 11** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark **$61.71**; live reset **HALTED** |
| **@21:21 Aug 11 (this pull)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark still **$61.71**; **live reset** still **$43.65 / $39.64 / HALTED** |

Exact latest confirmed filled equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

Newest live reset-book equity line (unchanged):
```
[19:40:33] equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299  unit=7.04  risk=15.0%(cut_neg_edge) edge_wr=43.3% ev=$-0.619  HALTED
```

**Note:** resume logs can show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only for the lifetime OG#3 book. The **`closed=32`** lines are a **reset mid-band ledger** — report them separately; do **not** replace 444 with 32.

### Reset mid-band ledger (live — separate from filled 444)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:29:35** | **31** | **42** | **~13–18** | **−$9.34** | **$43.75** / $41.65 open1 |
| **@19:36–19:40 (HALTED)** | **32** | **41** | **~13–19** | **−$11.43** | trough **$12.57** → mark **$43.65** / $39.64 open2 |
| **@19:20 Aug 11** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |
| **@21:21 Aug 11 (this pull)** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |

Last on-log Aug9 Kalshi settle (from earlier; none new this hour):
```
[19:30:21] SETTLE KXBNB15M-26AUG091530-30 NO LOSS pnl=-2.0919 markout/c=-0.570  cash=$41.65 equity=$41.65 risk=15.0% bn=flat:+0.000% dir=up
```

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~140.59h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444` (or onto reset `32`).

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @19:40 (still current):** **open=2**, cash **$39.64**, equity **$43.65**, **HALTED** (no new settle after 19:30 BNB loss).

### FILL / LIVE FILL / SETTLE in window since prior cron

**Filled-444 book:** still **0** new equity / filled closes after `[12:30:53]`.  
**Live Aug9 tape this hour (after `[19:40:33]`):**
- **0×** FILL / LIVE FILL / true SETTLE / new equity
- Transcript **UNCHANGED** vs 19:20 (no new sniper or Kalshi lines)
- After `[19:40:33]`: PRE-SETTLE **8** (retries **7**) still present from prior tape; no new equity-line HALTED prints

Mode last visible (reset mid-band @19:31–19:40; still in force):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **~7.04**, risk **15.0%** (`cut_neg_edge`), band **[0.45, 0.70)**
- **`halted=True`** after floor breach; no unhalt this hour

Sniper (last refresh still ~14:03; not Kalshi PnL):
- ASADO all-in still **held** (`0.00176 SOL` / ~60.9k tokens) @ ~**0.955–0.957x** (mcap **~$2,138–$2,141**)
- Unrealized ≈ **−$0.01** (prior tool: cost `$0.2640` → mark `$0.2522`; `pnl $-0.0118` with SOL fallback $150)
- sells **0**; runner still alive; TP 2x / stop-loss off; **no realized sniper PnL**
- Latest note still: insufficient SOL for new live buys — exits-only

---

## Hourly win / loss (preferred filled book)

| Window | ≈W–L | Closed Δ | Closed PnL Δ | Equity Δ | Notes |
|---|---|---|---|---|---|
| **Prior cron ~19:20 → this ~21:21** | **0–0** | **+0** (444→444) | **+$0.00** | **+$0.00** ($61.71→$61.71) | transcript **UNCHANGED**; no new Kalshi tape |
| **Live reset same window** | **0–0** | **+0** (32→32) | **+$0.00** | **+$0.00** ($43.65→$43.65) | still **HALTED**; open **2** unchanged |
| **Abandoned Bot $100 same window** | **0–0** | **+0** (14→14) | **+$0.00** | **+$0.00** ($60.61) | still frozen; do not merge |

**Hourly summary:** filled **0–0 / $0**; live reset **0–0 / $0**; abandoned **0–0 / $0**.

---

## PnL summary (what to watch)

| Book | Equity | Cash | Closed | ≈W–L | PnL | Status |
|---|---|---|---|---|---|---|
| **Preferred filled (lifetime)** | **$61.71** | **$61.71** | **444** | **~382–62** | **+$57.18** | STALE ~104.85h |
| **Live reset (mid-band)** | **$43.65** | **$39.64** | **32** | **~13–19** | **−$11.43** | **HALTED** ~49.69h |
| **Abandoned Bot $100** | **$60.61** | **$60.61** | **14** | **6–8** | **−$15.80** | frozen ~140.59h |

**Bottom line:** Lifetime filled book still **+$57.18 (~382–62 @ 86%)**. Live Kalshi session still **halted underwater (−$11.43)**. Hourly deltas all **flat**. Agent **IDLE**; sniper ASADO open with **$0 realized**.
