# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-09 ~20:05 UTC (automation cron)  
**Data freshness:** preferred filled equity mark still **STALE (~55h 34m)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled-444 equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent **woke** this hour (`lastMessageActivity` **20:03:05Z**, ~0.03h freeze). Transcript **CHANGED** vs 19:05.  
**Live reset book (new this hour):** mid-band stack printed newer equities on a **reset** closed counter (**closed=31→32**, win% **41–42**, pnl **−$9.34 → −$11.43**) and is now **HALTED** at floor **$20** — newest live mark **[19:40:33]** `equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299 HALTED`.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~91.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @20:05 via `batch-fetch-details` (`2026-08-09T20-04-42Z-bd27`). DO OR DIE transcript **CHANGED** (11,432,590 bytes / 106,067 lines; md5 `8eea6bb6cae2e7a25998fd9a87556c68`; prior 10,884,803 / 99,789 / `36de14add41392bb92f6657b007c0fae`).  
**Bot status (live @19:29–19:42):** Mid-band EV printer redeployed / continued; restart bankroll **$37.56** (unit **6.05**, risk **15%** cut_neg_edge, edge_wr **43.3%**); `HALT_FLOOR=20`, cash_target OFF; then **HALT RUN** at equity **$12.57 ≤ $20** (hw **$37.56**, start was **$56.74**). Newest mark recovered to **$43.65** cash **$39.64** with **2 opens**, still **HALTED**. Agent also opened draft PR **#126** (`cursor/pumpfun-axiom-sniper-1ecb`) — post-halt tail is mostly sniper work, not new Kalshi settles.

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash (preferred lifetime)** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE ~55.6h** |
| **Latest closed book (DO OR DIE filled)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Latest live mark (reset book)** | **$43.65** / cash **$39.64** / open **2** / closed **32** / win% **41** / pnl **−$11.43** — **HALTED** @19:40 |
| **Live ops this hour** | Transcript **CHANGED**; Aug9 SETTLE BNB NO **LOSS −$2.09** @19:30; reset book **31→32**; equity trough **$12.57** then **HALTED**; cash **~$53 → ~$39.64** |
| **Cash-save / halt** | **halt if equity ≤ $20** — **TRIGGERED**; cash_target OFF; SPRINT OFF; SAVE not hit |
| **Prior report (PR #125 / 19:00)** | **$61.71 / 444 / +$57.18** @12:30; mid-band last known cash ~$53 + 1 open |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~19:05 cron (filled book)** | **0–0 / $0** on preferred filled counters |
| **Hourly live reset book** | **+1 close** (31→32); closed pnl **≈ −$2.09** (matches on-log SETTLE); equity mark now **$43.65 HALTED** |
| **Day equity vs $93.75 @10:00** | filled mark **−$32.04** ($61.71); live mark **−$50.10** ($43.65) |
| **vs start_equity ($61.54)** | filled **+$0.17**; live **−$17.89** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** but active thru **20:03Z** (~0.03h); Bot $100 target **IDLE** since ~00:46 (~91.3h) |
| **Transcript** | **CHANGED** — **11,432,590** bytes / **106,067** lines; filled equity ts still **~12:30:53**; live equity thru **19:40:33** |

Live book source of truth for **lifetime closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). This hour the runner printed a **reset mid-band ledger** (**closed≈32 / −$11.43**) and **halted** — treat **$43.65 / $39.64 cash** as current live bankroll posture, not the stale $61.71 filled mark.

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — still **+$0.17** vs start equity (`$61.54`), **−$32.04** vs the $93.75 day high.

**Ops woke hard this hour, then halted.** After hours of quiet mid-band (last soft cash ~$53 + 1 open BTC @16:16), the DO OR DIE transcript grew ~0.55MB. The live stack came back on a **reset closed counter** (~31 closes already on that ledger), took a BNB NO settle **loss (−$2.09)** @19:30, printed equity down to **$12.57**, tripped **HALT_FLOOR=$20**, then marked **$43.65 / cash $39.64 / 2 opens** still **HALTED**. Edge on the restart was already poor (**edge_wr 43.3%**, `cut_neg_edge`, kelly **−30%**).

Ops read: historical filled book still profitable on paper (**+$57.18 / 444**), but **live cash is ~$40** and the active mid-band session is **halted underwater on its reset ledger (−$11.43 / ~13–19)**. Agent attention also split into a new **pumpfun/axiom sniper** draft PR (#126) after the halt — no further Kalshi equity prints after **19:40**.

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
| **@16:16 Aug 9 (live ops, no new filled-444 line)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | auth cash **$56.74** → post-fill **~$53.08** / **1 open** |
| **@19:05 Aug 9** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark **$61.71**; live cash print **~$53.08** |
| **@20:05 Aug 9 (this pull)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | filled mark still **$61.71**; **live reset** **$43.65 / $39.64 / HALTED** |

Exact latest confirmed filled equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

Newest live reset-book equity lines:
```
[19:29:35] equity=$43.75 cash=$41.65 open=1 closed=31 win%=42 pnl=-9.3380  unit=7.05  risk=15.0%(cut_neg_edge) edge_wr=43.3% ev=$-0.576
[19:36:29] equity=$12.57 cash=$8.56 open=2 closed=32 win%=41 pnl=-11.4299  unit=2.02  risk=15.0%(cut_neg_edge) edge_wr=43.3% ev=$-0.619  HALTED
[19:40:33] equity=$43.65 cash=$39.64 open=2 closed=32 win%=41 pnl=-11.4299  unit=7.04  risk=15.0%(cut_neg_edge) edge_wr=43.3% ev=$-0.619  HALTED
```

**Note:** resume logs can show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only for the lifetime OG#3 book. The new **`closed=32`** lines are a **reset mid-band ledger** — report them separately; do **not** replace 444 with 32.

### Reset mid-band ledger (live — separate from filled 444)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:29:35** | **31** | **42** | **~13–18** | **−$9.34** | **$43.75** / $41.65 open1 |
| **@19:36–19:40 (HALTED)** | **32** | **41** | **~13–19** | **−$11.43** | trough **$12.57** → mark **$43.65** / $39.64 open2 |

On-log Aug9 settle this hour:
```
[19:30:21] SETTLE KXBNB15M-26AUG091530-30 NO LOSS pnl=-2.0919 markout/c=-0.570  cash=$41.65 equity=$41.65 risk=15.0% bn=flat:+0.000% dir=up
```

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~91.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444` (or onto reset `32`).

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @16:16–16:17 (prior hour):** BTC YES @ 59¢ fill **6.14** → cash **~53.08**, runner **[9226]**.  
**Live @19:40 (this pull):** **open=2**, cash **$39.64**, equity **$43.65**, **HALTED** (no new settle after 19:30 BNB loss).

### FILL / LIVE FILL / SETTLE in window since prior cron

**Filled-444 book:** still **0** new equity / filled closes after `[12:30:53]`.  
**Live Aug9 tape this hour:**
- **1×** on-log `SETTLE` — BNB `26AUG091530` NO **LOSS −$2.0919** @19:30:21
- Reset equity prints: **6** lines (`closed=31/32`), ending **HALTED**
- Many `PRE-SETTLE IOC` retries around 19:29–19:42 (no-fill exits)
- Prior mid-band BTC fill @16:16:50 still the last `LIVE order … fill=` on Aug9 tickers in the pull
- Restart: `starting MODE=live bankroll=$37.56 … halt if equity <= $20.00` then `HALT RUN equity=$12.57 <= floor $20.00`

Mode last visible (reset mid-band @19:31–19:40):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **~7.04**, risk **15.0%** (`cut_neg_edge`), band **[0.45, 0.70)**, TP style abs/gain on restart
- **`halted=True`** after floor breach; PAUSED/SAVE cleared on restart; pid churn after **9226** (later **123420 → 123496**; unrelated sniper pid **133145** near end)

---

## Hourly win / loss

| Window (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| **19:48–03:09** | **~+2W / +1L** (417→420) | closed **+$3.67** | settles ~20:00–20:15; quiet until halt |
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
| **19:05–20:05 Aug 9 (this report)** | filled **0–0**; reset **+1 close (~0W–1L)** | filled **$0**; reset closed **≈ −$2.09**; live equity now **$43.65 HALTED** | transcript **CHANGED**; wake + halt |
| **Bot $100 VM 19:05–20:05** | **0–0** | **$0** | still frozen @$60.61 |

### 19:05→20:05 path (this report)

| Step | Equity / cash | Closed / win% / pnl | Δ closed PnL | Notes |
|---|---|---|---|---|
| Prior cron ~19:05 | filled $61.71 / $61.71; live cash ~$53.08 | filled 444 / 86% / +57.1847 | — | PR #125; mid-band last known + 1 open |
| Live ~19:29 | $43.75 / $41.65 | reset 31 / 42% / −9.3380 | — | reset ledger visible |
| Live ~19:30 | $41.65 / $41.65 | +1 SETTLE loss | **−$2.09** | BNB NO LOSS |
| Live ~19:36 | $12.57 / $8.56 | reset 32 / 41% / −11.4299 | **≈ −$2.09** vs 19:29 | **HALT RUN** floor $20 |
| This pull ~20:05 | filled still $61.71; live **$43.65 / $39.64** | filled 444 / +57.18; reset 32 / −11.43 | filled **+$0.00** | HALTED; agent on sniper PR #126 |

**Hourly closed W–L (filled 444 book):** **0–0**  
**Hourly closed PnL (filled 444 book):** **+$0.00**  
**Hourly equity Δ (filled mark):** **+$0.00**  
**Hourly live reset book:** **~0–1 / ≈ −$2.09** closed; bankroll posture **~$53 → ~$40 cash**, **HALTED**  
**Hourly equity Δ (live mark vs prior soft cash posture):** live equity mark **$43.65** (vs prior soft ~$53 cash + open) — account clearly lower; do not use $61.71 as current bankroll

---

## Caveats

1. Prefer filled equity-line **`closed=444`** for lifetime OG#3; ignore resume **`closed=544`**. Report reset **`closed=32`** separately.
2. Filled equity mark age **~55h 34m** — lifetime closed W/L/PnL are last confirmed filled, not live MTM.
3. Live cash **~$39.64** / equity **$43.65** diverge hard from stale mark **$61.71**; use live mark for current bankroll.
4. Equity jump **$12.57 → $43.65** while still HALTED with same closed=32 likely reflects mark-to-market / open valuation recovery, not a new settle (no SETTLE after 19:30 in pull).
5. Mid-band session is **HALTED** at floor $20; further Kalshi PnL needs an unhalt / redeploy.
6. Agent opened draft PR **#126** (pumpfun/axiom sniper) after the halt — Kalshi attention may stay diverted.
7. Abandoned Bot $100 VM remains a separate ledger — do not merge onto DO OR DIE.
