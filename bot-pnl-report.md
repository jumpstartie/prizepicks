# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-10 ~13:03 UTC (automation cron)  
**Data freshness:** preferred filled equity mark still **STALE (~72.5h)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled-444 equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent is **IDLE** (`lastMessageActivity` still **04:38:57Z**, ~8.40h vs pull). Transcript **UNCHANGED** vs 12:04 — **no new Kalshi equity / FILL / SETTLE** after the **[19:40:33] HALTED** mark; ASADO still held with **$0 realized** (mark ~0.96x, unrealized ≈ −$0.01).  
**Live reset book:** still **HALTED** — newest live mark **[19:40:33]** `equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299 HALTED` (**unchanged** vs 12:04; ~17.4h since Aug 9 evening).  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~108.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @13:03 via `batch-fetch-details` (`2026-08-10T13-02-48Z-59cc`). DO OR DIE transcript **UNCHANGED** (11,752,074 bytes / 108,310 lines; md5 `d46fdf3fb3add17b5d2a2e2984f4f3b9`). Draft events PR **#126**.  
**Bot status (live Kalshi):** Mid-band EV printer remains **HALTED** at floor **$20**. No unhalt / redeploy. Sniper position still open; no new status refresh this hour.

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash (preferred lifetime)** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE ~72.5h** |
| **Latest closed book (DO OR DIE filled)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Latest live mark (reset book)** | **$43.65** / cash **$39.64** / open **2** / closed **32** / win% **41** / pnl **−$11.43** — **HALTED** @19:40 (**unchanged**) |
| **Live ops this hour** | Transcript **UNCHANGED**; **0** new Kalshi FILL/SETTLE/equity after 19:40; sniper still holding ASADO ~**0.96x**, **$0 realized** |
| **Cash-save / halt** | **halt if equity ≤ $20** — still **TRIGGERED**; cash_target OFF; SPRINT OFF |
| **Prior report (PR #143 / 12:04)** | **$61.71 / 444 / +$57.18** filled; live **$43.65 HALTED / 32 / −$11.43** |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~12:04 cron (filled book)** | **0–0 / $0** on preferred filled counters |
| **Hourly live reset book** | **0–0 / $0**; still **HALTED** at **$43.65 / $39.64** |
| **Day equity vs $93.75 @12:00** | filled mark **−$32.04** ($61.71); live mark **−$50.10** ($43.65) |
| **vs start_equity ($61.54)** | filled **+$0.17**; live **−$17.89** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since **04:38Z** (~8.40h); Bot $100 target **IDLE** since ~00:46 (~108.3h) |
| **Transcript** | **UNCHANGED** — **11,752,074** bytes / **108,310** lines; md5 `d46fdf3fb3add17b5d2a2e2984f4f3b9` |

Live book source of truth for **lifetime closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). Current live bankroll posture remains the **halted reset mark** (**$43.65 / $39.64 cash**).

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — still **+$0.17** vs start equity (`$61.54`), **−$32.04** vs the $93.75 day high.

**Kalshi trading is still idle.** After the 19:29–19:42 reset/mid-band wake (BNB NO loss −$2.09, equity trough $12.57, halt floor $20), there are still **no new Kalshi settles or equity prints** after **19:40**. This hour the transcript fingerprint is identical to 12:04: ASADO still open (`0.00176 SOL` / ~60.9k tokens) at **~0.96x** (mcap ~$2,141; unrealized ≈ **−$0.01**), TP 2x / stop-loss off, **no sells**, **no realized sniper PnL**, and **no Kalshi unhalt**. Agent last refreshed at **04:38Z** and remains **IDLE** (~8.40h).

Ops read: historical filled book still profitable on paper (**+$57.18 / 444**), but **live cash is still ~$40**, the mid-band reset ledger is still **halted underwater (−$11.43 / ~13–19)**, and current activity is sniper position management (draft PR **#126**), not Kalshi. Further Kalshi PnL needs an unhalt / redeploy.

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
| **@16:16 Aug 9 – 12:04 Aug 10** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark **$61.71**; live reset **HALTED** |
| **@13:03 Aug 10 (this pull)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark still **$61.71**; **live reset** still **$43.65 / $39.64 / HALTED** |

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
| **@13:03 Aug 10 (this pull)** | **32** (unchanged) | **41** | **~13–19** | **−$11.43** | still **$43.65 / $39.64 HALTED** |

Last on-log Aug9 Kalshi settle (from earlier; none new this hour):
```
[19:30:21] SETTLE KXBNB15M-26AUG091530-30 NO LOSS pnl=-2.0919 markout/c=-0.570  cash=$41.65 equity=$41.65 risk=15.0% bn=flat:+0.000% dir=up
```

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~108.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444` (or onto reset `32`).

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @19:40 (still current):** **open=2**, cash **$39.64**, equity **$43.65**, **HALTED** (no new settle after 19:30 BNB loss).

### FILL / LIVE FILL / SETTLE in window since prior cron

**Filled-444 book:** still **0** new equity / filled closes after `[12:30:53]`.  
**Live Aug9 tape this hour (after `[19:40:33]`):**
- **0×** FILL / LIVE FILL / true SETTLE / new equity
- **PRE-SETTLE IOC retries** still present after the halt mark in file-order (no fills)
- Transcript **UNCHANGED** vs 12:04 (identical bytes/lines/md5)

Mode last visible (reset mid-band @19:31–19:40; still in force):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **~7.04**, risk **15.0%** (`cut_neg_edge`), band **[0.45, 0.70)**
- **`halted=True`** after floor breach; no unhalt this hour

Sniper (unchanged vs 12:04; not Kalshi PnL):
- ASADO all-in still **held** (`0.00176 SOL` / ~60.9k tokens) @ ~**0.96x** (`multiple=0.9569x`)
- Unrealized ≈ **−$0.01** (`cost≈$0.1347` → `mark≈$0.1289`; `pnl_usd≈$-0.0058`); sells **0**
- TP 2x / stop-loss off; **no realized sniper PnL**
- Latest note still: insufficient SOL for new live buys — exits-only

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet first night |
| **03:09–03:35** | **+1W / 0L** (420→421) | closed **+$1.20** | XRP `052330` inferred WIN; then 2 new opens |
| **03:35–09:03** | **0–0 in tape** | **$0 in tape** | six prior crons; runner logs not visible |
| **09:03–10:03** | **+3 closes** (421→424) | closed **−$1.74**; equity **−$1.77** | catch-up mark @09:39 + new `0545` fills |
| **10:03 Aug 6 – 10:01 Aug 7** | **0–0** | **$0** | STALE — identical 09:39 mark (PRs #45–#68) |
| **10:01–11:20** | **+6 closes** (424→430) | closed **−$3.81**; equity **−$3.83** | wake @10:54; 1 on-log SETTLE (BNB −4.87); +5 closes off-log |
| **11:02–12:05** | **+8 closes** (430→438) | closed **+$7.44**; equity **+$7.43** | `0700` resolved off-log; flat @$60.42 |
| **12:05–13:05** | **+6 closes** (438→444) | closed **+$1.27**; equity **+$1.29** | off-log closes; OG#3 redeploy @12:30 @$61.71 flat |
| **13:05 Aug 7 – 16:05 Aug 9** | **0–0** | **$0** | frozen mark @$61.71 / 444 across PRs #69–#122 |
| **16:05–17:05 Aug 9** | **0–0 closed** | **$0 closed** | transcript **CHANGED**; mid-band live + 1 open fill; filled mark unchanged (PR #123) |
| **17:05–18:05 Aug 9** | **0–0 closed** | **$0 closed** | transcript **UNCHANGED**; agent IDLE ~1.8h (PR #124) |
| **18:05–19:05 Aug 9** | **0–0 closed** | **$0 closed** | transcript **UNCHANGED**; agent IDLE ~2.8h (PR #125) |
| **19:05–20:05 Aug 9** | filled **0–0**; reset **+1 close (~0W–1L)** | filled **$0**; reset closed **≈ −$2.09**; live equity **$43.65 HALTED** | transcript **CHANGED**; wake + halt (PR #127) |
| **20:05–21:05 Aug 9** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **CHANGED** (sniper only); no new Kalshi tape (PR #128) |
| **21:05–22:05 Aug 9** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent IDLE ~1.04h (PR #129) |
| **22:05–23:05 Aug 9** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent IDLE ~2.04h (PR #130) |
| **23:05 Aug 9 – 00:05 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **CHANGED** (sniper retry; buys failed); agent **RUNNING** (PR #131) |
| **00:05–01:05 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **CHANGED** (ASADO filled & held; $0 sniper PnL); agent **IDLE** @00:13 (PR #132) |
| **01:05–02:05 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** ~1.87h (PR #133) |
| **02:05–03:01 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** ~2.80h (PR #134) |
| **03:01–04:01 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** ~3.80h (PR #135) |
| **04:01–05:03 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **CHANGED** (ASADO ~1.03x→~0.96x); agent **IDLE** @04:38 (PR #136) |
| **05:03–06:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (PR #137) |
| **06:04–07:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~2.42h) (PR #138) |
| **07:04–08:02 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~3.39h) (PR #139) |
| **08:02–09:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~4.43h) (PR #140) |
| **09:04–10:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~5.43h) (PR #141) |
| **10:04–11:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~6.42h) (PR #142) |
| **11:04–12:04 Aug 10** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~7.43h) (PR #143) |
| **12:04–13:03 Aug 10 (this report)** | filled **0–0**; reset **0–0** | filled **$0**; reset **$0**; still **HALTED @$43.65** | transcript **UNCHANGED**; agent **IDLE** since 04:38 (~8.40h) |
| **Bot $100 VM 12:04–13:03** | **0–0** | **$0** | still frozen @$60.61 |

### 12:04→13:03 path (this report)

| Step | Equity / cash | Closed / win% / pnl | Δ closed PnL | Notes |
|---|---|---|---|---|
| Prior cron ~12:04 | filled $61.71 / $61.71; live $43.65 / $39.64 | filled 444 / 86% / +57.1847; reset 32 / 41% / −11.4299 | — | PR #143; HALTED; ASADO ~0.96x |
| This pull ~13:03 | filled still $61.71; live still **$43.65 / $39.64** | filled 444 / +57.18; reset 32 / −11.43 | filled **+$0.00**; reset **+$0.00** | fingerprint identical; Kalshi quiet; agent IDLE @04:38 |

**Hourly closed W–L (filled 444 book):** **0–0**  
**Hourly closed PnL (filled 444 book):** **+$0.00**  
**Hourly equity Δ (filled mark):** **+$0.00**  
**Hourly live reset book:** **0–0 / $0**; still **HALTED** at **$43.65 / cash $39.64**  
**Hourly equity Δ (live mark):** **+$0.00**  
**Hourly sniper:** ASADO still held (~0.96x); unrealized ≈ −$0.01; **$0 realized**

---

## Caveats

1. Prefer filled equity-line **`closed=444`** for lifetime OG#3; ignore resume **`closed=544`**. Report reset **`closed=32`** separately.
2. Filled equity mark age **~72.5h** — lifetime closed W/L/PnL are last confirmed filled, not live MTM.
3. Live cash **~$39.64** / equity **$43.65** diverge hard from stale mark **$61.71**; use live mark for current bankroll.
4. Equity jump **$12.57 → $43.65** while still HALTED with same closed=32 (prior) likely reflects mark-to-market / open valuation recovery, not a new settle (no SETTLE after 19:30 in pulls).
5. Mid-band session is still **HALTED** at floor $20; further Kalshi PnL needs an unhalt / redeploy.
6. Agent is **IDLE** since sniper ASADO status refresh @04:38Z (draft PR **#126**); transcript **UNCHANGED** this hour; sniper has **no realized PnL** yet (open ~0.96x).
7. Abandoned Bot $100 VM remains a separate ledger — do not merge onto DO OR DIE.
