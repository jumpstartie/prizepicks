# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-09 ~17:05 UTC (automation cron)  
**Data freshness:** filled equity mark still **STALE (~52h 34m)** — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) newest filled equity remains **[12:30:53]** `equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847`. Supervising agent **woke** this hour (`lastMessageActivity` **16:17:04Z**, ~0.80h quiet vs pull); status **IDLE** after mid-band deploy. Transcript **CHANGED** vs 16:05.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~88.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @17:05 via `batch-fetch-details` (`2026-08-09T17-03-05Z-aec5`). DO OR DIE transcript **CHANGED** (10,884,803 bytes / 99,789 lines; md5 `36de14add41392bb92f6657b007c0fae`) — **auth fix + mid-band redeploy + 1 LIVE order fill**; **no new filled crypto equity line**.  
**Bot status (post 16:16 redeploy):** Strategy swapped to **Mid-band EV printer** (band **[0.45, 0.70)**, TP abs **0.92**). Auth restored; cash at auth **$56.74** / opens **0**. Full engine restart → runner pid **9226**; `HALT_FLOOR=20` / cash_target OFF / SPRINT OFF; `halted=False`; SAVE False; PAUSED False. Immediately after start: **LIVE order** BTC YES fill **6.14 @ 0.59** (`KXBTC15M-26AUG091230-30`); side-check **cash 53.08 / hw 56.74 / health ok / runner [9226]**.

---

## Headline

| Metric | Value |
|---|---|
| **Latest filled equity / cash** | **$61.71** / **$61.71** @12:30:53 (**flat on mark**, open **0**) — **STALE** |
| **Latest closed book (DO OR DIE)** | **444 closes · 86% · +$57.18** (~**382–62**) |
| **Live ops (new this hour)** | Mid-band **RUNNING** pid **9226**; auth cash **$56.74** → post-fill cash **~$53.08**; **1 open** BTC YES @59¢ → TP 92¢ |
| **Cash-save / halt** | **halt if equity ≤ $20** (was $25); cash_target OFF; SPRINT OFF; SAVE not hit |
| **Prior report (PR #122 / 16:00)** | **$61.71 / 444 / +$57.18** @12:30 flat; transcript frozen |
| **Δ vs prior report (filled book)** | closed **444→444 (+0)**; closed pnl **+$0.00**; equity **+$0.00** |
| **Hourly since ~16:05 cron** | filled book **0–0 / $0**; ops: mid-band live + **1 fill** (no settle yet) |
| **Day equity vs $93.75 @10:00** | **−$32.04** at last filled mark **$61.71** |
| **vs start_equity ($61.54)** | **+$0.17** at last filled mark **$61.71** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE activity **16:17Z** then **IDLE** (~0.80h); Bot $100 target **IDLE** since ~00:46 (~88.3h) |
| **Transcript** | **CHANGED** — **10,884,803** bytes / **99,789** lines (+279,497 B / +3,294 lines); last filled equity ts still **~12:30:53** |

Live book source of truth for **closed W/L + PnL** remains the last filled equity line on **DO OR DIE** (**$61.71 / 444 / +$57.18**). This hour the supervising agent **came back online**, fixed Kalshi auth, and **redeployed mid-band**. There is **still no new `equity=$… closed=… pnl=` line**, so hourly closed PnL stays **flat**, while live cash (**~$53**) and **1 open** show the runner is trading again under the new strategy.

---

## How the bot is working (profit read)

Closed hit rate on the filled OG#3 book remains strong (**86%**, ~**382–62**). Lifetime closed PnL holds at **+$57.18** and the last filled bankroll mark is **$61.71** — slightly **above** start equity (**+$0.17** vs `$61.54`), still **−$32.04** vs the $93.75 day high.

**This hour’s ops change matters more than the flat closed tape:** after ~51h of freeze, auth was restored (`cash $56.74`, opens 0) and the bot left **OG Strategy #3** for **Mid-band EV printer** (45–70¢ band, TP 0.92, halt floor **$20**, unit **12.20**, risk **~20%** of $56.74). Within seconds it took a **BTC YES** fill (**6.14 @ 59¢**). That position is **unsettled**, so it does **not** yet move `closed` / `pnl` on the equity tape. Soft side-check cash **$53.08** vs hw **$56.74** matches that open; both sit **below** the stale filled mark **$61.71**.

Ops read: historical filled book still profitable; live stack is **active again** under mid-band with **1 open** and **no confirmed settle this hour**. Treat **+$57.18 / 444** as last confirmed closed book, and **~$53 cash + open BTC** as current live posture until a new equity line prints.

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
| **@16:16 Aug 9 (live ops, no new equity line)** | **444** (unchanged) | **86** | **~382–62** | **+$57.18** | auth cash **$56.74** → post-fill **~$53.08** / **1 open** |

Exact latest confirmed filled equity line:
```
[12:30:53] equity=$61.71 cash=$61.71 open=0 closed=444 win%=86 pnl=+57.1847  unit=8.62  risk=13.0%(edge_kelly) edge_wr=83.7% ev=$+0.128
```

**Note:** resume logs can show higher `closed=` counts (e.g. `closed=544`). Equity-line **`closed=444`** is **filled** closes only; use **444 / +$57.18** for reporting until a newer equity line lands.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~88.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `444`.

### Opens last known

**Filled equity @12:30:** flat — cash **$61.71**, opens **0**.  
**Live @16:16–16:17 (new):** auth **opens 0** / cash **$56.74**; then **BTC YES @ 59¢** fill **6.14** → inferred **1 open**, cash **~53.08**, hw **56.74**, health ok, runner **[9226]**.

### FILL / LIVE FILL / SETTLE in window since prior cron

**No `LIVE FILL` / `SETTLE` / new `equity=` after 12:30:53.**  
**New this hour:** **1×** `LIVE order … fill=6.14` @ **16:16:50** on `KXBTC15M-26AUG091230-30` (bid 6.14 @ 0.5900, TP 0.92 abs).  
Hourly **closed** book **unchanged** (fill not settled).

Mode now (mid-band @16:16):
- `HALT_FLOOR=20`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **12.20**, risk **~20.0%** of bankroll **$56.74**, band **[0.45, 0.70)**, TP abs **0.92**
- `halted=False`; PAUSED False; SAVE False; pid **9226**

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
| **16:05–17:05 Aug 9 (this report)** | **0–0 closed** | **$0 closed** | transcript **CHANGED**; mid-band live + 1 open fill; filled mark unchanged |
| **Bot $100 VM 16:05–17:05** | **0–0** | **$0** | still frozen @$60.61 |

### 16:05→17:05 path (this report)

| Step | Equity / cash | Closed / win% / pnl | Δ closed PnL | Notes |
|---|---|---|---|---|
| Prior cron ~16:05 | $61.71 / $61.71 | 444 / 86% / +57.1847 | — | PR #122; transcript frozen |
| This pull ~17:05 | filled mark still $61.71 / $61.71; live cash ~$53.08 | 444 / 86% / +57.1847 | **+$0.00** | mid-band redeploy; 1 LIVE order fill unsettled |

**Hourly closed W–L:** **0–0**  
**Hourly closed PnL:** **+$0.00**  
**Hourly equity Δ (filled mark):** **+$0.00**  
**Hourly live ops:** auth OK → mid-band start bankroll **$56.74** → fill → cash **~$53.08** / **1 open**

---

## Caveats

1. Prefer filled equity-line **`closed=444`**; ignore resume **`closed=544`**.
2. Filled equity mark age **~52h 34m** — closed W/L/PnL are last confirmed, not live MTM.
3. Live cash **~$53.08** and auth cash **$56.74** both diverge from stale mark **$61.71**; do not treat $61.71 as current bankroll.
4. Mid-band strategy just went live; one BTC open is **unsettled** — next settle will be the first mid-band closed PnL print.
5. Abandoned Bot $100 VM remains a separate ledger — do not merge onto DO OR DIE.
