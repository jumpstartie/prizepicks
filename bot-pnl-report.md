# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-12 ~11:21 UTC (automation cron)  
**Data freshness:** preferred filled equity mark still **STALE (~118.83h)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled-444 equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent woke to **RUNNING** (`lastMessageActivity` **11:20:39Z**, fresh vs pull) but the growth is **chat/citations only** — **no new Kalshi equity / FILL / SETTLE** after the **[19:40:33] HALTED** mark; ASADO still held with **$0 realized** (mark ~0.955x, unrealized ≈ −$0.01).  
**Live reset book:** still **HALTED** — newest live mark **[19:40:33]** `equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299 HALTED` (**unchanged** vs 10:16; ~63.67h since Aug 9 evening).  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~154.57h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @11:21 via `batch-fetch-details` (`2026-08-12T11-20-44Z-efdc`). DO OR DIE transcript **CHANGED** vs 10:16 — **12,086,828** bytes / **111,715** lines; md5 `97bba4ce07f898174059bf63548f3f9e` (was 11,759,771 / 108,368 / `7b1aac…`) — delta is agent replies quoting old marks, **not** new bot tape. Draft events PR **#126**.  
**Bot status (live Kalshi):** Mid-band EV printer remains **HALTED** at floor **$20**. Index shows agent **RUNNING** with fresh LMA; no unhalt / redeploy / new Kalshi tape. Sniper position still open; last mark refresh still ~14:03 Aug 10 (ASADO ~0.955x).

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash (preferred lifetime)** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE ~118.83h** |
| **Latest closed book (DO OR DIE filled)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Latest live mark (reset book)** | **$43.65** / cash **$39.64** / open **2** / closed **32** / win% **41** / pnl **−$11.43** — **HALTED** @19:40 (**unchanged**) |
| **Live ops this hour** | Transcript **CHANGED** (chat only); **0** new Kalshi FILL/SETTLE/equity after 19:40; agent **RUNNING** (LMA **11:20:39Z**); sniper still holding ASADO ~**0.955x**, **$0 realized** |
| **Cash-save / halt** | **halt if equity ≤ $20** — still **TRIGGERED**; cash_target OFF; SPRINT OFF |
| **Prior report (10:16 / PR #185)** | **$61.71 / 444 / +$57.18** filled; live **$43.65 HALTED / 32 / −$11.43** |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~10:16 cron (filled book)** | **0–0 / $0** on preferred filled counters |
| **Hourly live reset book** | **0–0 / $0**; still **HALTED** at **$43.65 / $39.64** |
| **Day equity vs $93.75 @12:00** | filled mark **−$32.04** ($61.71); live mark **−$50.10** ($43.65) |
| **vs start_equity ($61.54)** | filled **+$0.17**; live **−$17.89** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **RUNNING** (LMA **11:20:39Z**, ~0.00h); Bot $100 target **IDLE** since ~00:46 (~154.57h) |
| **Transcript** | **CHANGED** — **12,086,828** bytes / **111,715** lines; md5 `97bba4ce07f898174059bf63548f3f9e` (chat/citations; **no new tape**) |

Live book source of truth for **lifetime closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). Current live bankroll posture remains the **halted reset mark** (**$43.65 / $39.64 cash**).

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — still **+$0.17** vs start equity (`$61.54`), **−$32.04** vs the $93.75 day high.

**Kalshi trading is still idle on-tape.** After the 19:29–19:42 reset/mid-band wake (BNB NO loss −$2.09, equity trough $12.57, halt floor $20), there are still **no new Kalshi settles or equity prints** after **19:40**. This hour the supervising agent is **RUNNING** again (fresh LMA ~11:20), and the transcript grew (~+327 KB / +3,347 lines) from **agent chat quoting prior marks** — not from new FILLs/SETTLEs. ASADO is still open at **~0.955x** (mcap ~$2,138), TP 2x / stop-loss off, **no sells**, **no realized sniper PnL**.

Ops read: historical filled book still profitable on paper (**+$57.18 / 444**), but **live cash is still ~$40**, the mid-band reset ledger is still **halted underwater (−$11.43 / ~13–19)**, and current activity is agent chat + sniper position monitoring (draft PR **#126**), not Kalshi. Further Kalshi PnL needs an unhalt / redeploy that actually lands new tape.

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
| **@16:16 Aug 9 – 10:16 Aug 12** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark **$61.71**; live reset **HALTED** |
| **@11:21 Aug 12 (this pull)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark still **$61.71**; **live reset** still **$43.65 / $39.64 / HALTED** |

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
| **@10:16 Aug 12** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |
| **@11:21 Aug 12 (this pull)** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |

Last on-log Aug9 Kalshi settle (from earlier; none new this hour):
```
[19:30:21] SETTLE KXBNB15M-26AUG091530-30 NO LOSS pnl=-2.0919 markout/c=-0.570  cash=$41.65 equity=$41.65 risk=15.0% bn=flat:+0.000% dir=up
```

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~154.57h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444` (or onto reset `32`).

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @19:40 (still current):** **open=2**, cash **$39.64**, equity **$43.65**, **HALTED** (no new settle after 19:30 BNB loss).

### FILL / LIVE FILL / SETTLE in window since prior cron

**Filled-444 book:** still **0** new equity / filled closes after `[12:30:53]`.  
**Live Aug9 tape this hour (after `[19:40:33]`):**
- **0×** FILL / LIVE FILL / true SETTLE / new equity
- Transcript **CHANGED** vs 10:16 from agent chat/citations only (no new sniper Update or Kalshi lines on tape)
- After `[19:40:33]`: PRE-SETTLE **8** (retries **7**) still present from prior tape; no new equity-line HALTED prints
- After `[12:30:53]`: equity lines **6**; FILL **0**; LIVE FILL **0**; SETTLE **1**; PRE-SETTLE **56** (retries **55**); HALTED on equity **5**

Mode last visible (reset mid-band @19:31–19:40; still in force):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **~7.04**, risk **15.0%** (`cut_neg_edge`), band **[0.45, 0.70)**
- **`halted=True`** after floor breach; no unhalt this hour
- restart bankroll last seen **$37.56**

Sniper (last refresh still ~14:03; not Kalshi PnL):
- ASADO all-in still **held** (`0.00176 SOL` / ~60.9k tokens) @ ~**0.955x** (mcap **~$2,138**)
- Unrealized ≈ **−$0.01** (prior tool: cost `$0.2640` → mark `$0.2522`; `pnl $-0.0118` with SOL fallback $150)
- sells **0**; runner still alive (pid **158935**); TP 2x / stop-loss off; **no realized sniper PnL**
- Latest note still: insufficient SOL for new live buys — exits-only

---

## Hourly win / loss (preferred filled book)

| Window | ≈W–L | Closed Δ | Closed PnL Δ | Equity Δ | Notes |
|---|---|---|---|---|---|
| **Prior cron ~10:16 → this ~11:21** | **0–0** | **+0** (444→444) | **+$0.00** | **+$0.00** ($61.71→$61.71) | transcript **CHANGED** (chat); **no new Kalshi tape** |
| **Live reset same window** | **0–0** | **+0** (32→32) | **+$0.00** | **+$0.00** ($43.65→$43.65) | still **HALTED**; open **2** unchanged |
| **Abandoned Bot $100 same window** | **0–0** | **+0** (14→14) | **+$0.00** | **+$0.00** ($60.61) | still frozen; do not merge |

**Hourly summary:** filled **0–0 / $0**; live reset **0–0 / $0**; abandoned **0–0 / $0**.

---

## PnL summary (what to watch)

| Book | Equity | Cash | Closed | ≈W–L | PnL | Status |
|---|---|---|---|---|---|
| **Preferred filled (lifetime)** | **$61.71** | **$61.71** | **444** | **~382–62** | **+$57.18** | STALE ~118.83h |
| **Live reset (mid-band)** | **$43.65** | **$39.64** | **32** | **~13–19** | **−$11.43** | **HALTED** ~63.67h |
| **Abandoned Bot $100** | **$60.61** | **$60.61** | **14** | **6–8** | **−$15.80** | frozen ~154.57h |

**Bottom line:** Lifetime filled book still **+$57.18 (~382–62 @ 86%)**. Live Kalshi session still **halted underwater (−$11.43)**. Hourly deltas all **flat**. Agent **RUNNING** with fresh LMA but **no new Kalshi tape**; sniper ASADO open with **$0 realized**.
