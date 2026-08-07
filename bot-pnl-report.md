# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-07 ~12:05 UTC (automation cron)  
**Data freshness:** **STALE (~49 min)** but **CHANGED** vs prior cron — [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`cursor/kalshi-15m-research-1ecb`) advanced through a profitable `0700` settle gap and OG#3 redeploy. Newest filled equity **[11:16:02]** `equity=$60.42 cash=$60.42 open=0 closed=438 win%=86 pnl=+55.9162`. Supervising agent last activity **~11:16:19Z**; status **IDLE**. Runner may have traded after that without new transcript capture.  
**Abandoned sprint VM:** [Bot $100 target](https://cursor.com/agents/bc-019fd43c-4a8f-76c0-a895-cc8091c29776) still **frozen @00:46** — mark **$60.61** / closed **14 / 43% / −$15.80** / open **0**. ~35.3h stale. Separate reset ledger — **do not merge**.  
**Source:** DO OR DIE + Bot $100 target transcript pulls @12:05 via `batch-fetch-details`. DO OR DIE transcript **CHANGED** (+32,886 bytes / +250 lines vs 11:02). No newer live trading agent found.  
**Bot status (last confirmed @11:16):** Redeployed OG#3 with **halt floor $25** / cash_target OFF / SPRINT OFF. Flat (`open=0`), scanning `070730`. Runner pid **239777** + keep_alive **239610** + watchdog **239633**; health `ok` @11:16:16Z; `halted=False`; SAVE False; PAUSED False.

---

## Headline

| Metric | Value |
|---|---|
| **Latest equity / cash** | **$60.42** / **$60.42** @11:16:02 (**flat**, open **0**) |
| **Latest closed book (DO OR DIE)** | **438 closes · 86% · +$55.92** (~**377–61**) |
| **Cash-save / halt** | **halt if equity ≤ $25**; cash_target OFF; SPRINT OFF; SAVE not hit |
| **Prior report (PR #69 / 11:00)** | **$52.99 / 430 / +$48.48** @10:56 (then ~4 opens / cash ~$33.39) |
| **Δ vs prior report** | closed **430→438 (+8)**; closed pnl **+$7.44**; equity **+$7.43** |
| **Hourly since ~11:02 cron** | **+8 closes / closed PnL +$7.44** — `0700` window resolved off-log; book flat again |
| **Day equity vs $93.75 @10:00** | **−$33.33** at last mark **$60.42** |
| **vs start_equity ($61.54)** | **−$1.12** at last mark **$60.42** |
| **Abandoned Bot $100 VM** | still **$60.61 / 6W–8L / −$15.80** @00:46 — do not merge |
| **Agent status** | DO OR DIE **IDLE** since ~11:16 (~49 min); Bot $100 target **IDLE** since ~00:46 (~35.3h) |
| **Transcript** | **CHANGED** — **10,259,048** bytes / **94,569** lines (was 10,226,162 / 94,319); last bot ts **~11:16:16** |

Live book source of truth remains **DO OR DIE**. After the 11:00 wake left ~4 opens on `0700` with cash ~$33.39, the next mark shows those positions resolved: closed **+8**, cash back to **$60.42**, flat. **Zero SETTLE strings** after 10:56 — the entire hourly gain is off-log.

---

## How the bot is working (profit read)

Closed hit rate still strong (**86%**, ~**377–61**). Lifetime closed PnL **recovered** to **+$55.92** (was **+$48.48** at 11:00) and bankroll climbed back to **$60.42** — nearly flat vs start equity (**−$1.12** vs `$61.54`), still **−$33.33** vs the $93.75 day high. The `0700` basket (BTC YES / BNB NO / SOL YES, plus any silent extras) appears to have settled net-positive (~+$7.44 closed PnL / +$7.43 equity). Bot redeployed OG#3 @11:15–11:16 with **$25 halt floor**, flat, scanning the next window — then supervising agent went **IDLE**, so this print is **~49 min stale** even though the book improved vs last cron.

---

## Total win / loss

### Live lifetime book (DO OR DIE — current source of truth)

| Checkpoint | Closed | Win% | ≈W–L | Closed PnL | Equity / cash |
|---|---|---|---|---|---|
| **@19:48:19 Aug 5** | **417** | **86** | **359–58** | **+$49.16** | **$76.46** / $70.72 open1 |
| **@03:09:09 Aug 6 (halt)** | **420** | **86** | **361–59** | **+$52.83** | **$57.41** flat |
| **@03:35:30** | **421** | **86** | **362–59** | **+$54.03** | **$58.59** / $49.81 open2 |
| **@09:39:01 Aug 6** | **424** | **86** | **~365–59** | **+$52.29** | **$56.82** / $46.60 open2 |
| **@10:56:42 Aug 7** | **430** | **86** | **~370–60** | **+$48.48** | **$52.99** / $40.28 open3 |
| **@11:16:02 Aug 7 (latest confirmed)** | **438** | **86** | **~377–61** | **+$55.92** | **$60.42** / $60.42 flat |

Exact latest confirmed equity line:
```
[11:16:02] equity=$60.42 cash=$60.42 open=0 closed=438 win%=86 pnl=+55.9162  unit=8.44  risk=13.0%(cut_neg_edge) edge_wr=79.0% ev=$-0.262
```

**Note:** resume logs still show higher `closed=` counts (e.g. `closed=538`). Equity-line **`closed=438`** is **filled** closes only; use **438 / +$55.92** for reporting.

### Abandoned sprint VM (Bot $100 target — historical / separate ledger)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| **@00:46 (still frozen)** | **6–8** (43%) | **−$15.80** | high @mark; stale ~35.3h |
| Sprint flat path | — | **−$19.25** ($79.86 → $60.61) | high @mark; stale since |

Do **not** add Bot $100 `closed=14` onto DO OR DIE `438`.

### Opens last known

**Flat @11:16** — `pre_restart API cash 60.42 opens 0 []`; newest equity `open=0`. Watching `070730` only (mids &lt;0.70 skipped as too cheap).

Prior `0700` opens (inferred settled off-log between 10:57 and 11:16):

| Time | Market | Side | Entry ≈ | Size ≈ | Cash after fill |
|---|---|---|---|---|---|
| 10:54:51 | `KXBTC15M-26AUG070700-00` | YES | ~0.83 | 9.58 | $45.04 |
| 10:55:30 | `KXBNB15M-26AUG070700-00` | NO | ~0.71 | 6.71 | $40.28 |
| 10:57:05 | `KXSOL15M-26AUG070700-00` | YES | ~0.85 | 8.10 | **$33.39** |

Closed jumped **430→438** (+8) with cash **$33.39→$60.42** — net win on the window, but **no SETTLE strings** for `KX*15M-26AUG070700*`.

### FILL / LIVE FILL / SETTLE in window since prior cron

```
[10:57:05] LIVE FILL YES 8.10 @ ~0.85 on KXSOL15M-26AUG070700-00 status=executed cash=$33.39 risk=13.0% bn=flat
```

**No SETTLE lines after 10:56:00.** No LIVE FILL after **10:57:05**. Entire **+8 / +$7.44** move is off-log (likely ~11:00 `0700` resolution).

Redeploy context immediately before newest mark:
- Engine restart @11:15:49–11:16:01; `pre_restart API cash 60.42 opens 0 []`
- Mode: `HALT_FLOOR=25`, `HALT_CASH_TARGET=0`, SPRINT OFF, unit **8.44**, risk **13.0%(cut_neg_edge)**

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
| **11:02–12:05 (this report)** | **+8 closes** (430→438) | closed **+$7.44**; equity **+$7.43** | `0700` resolved off-log; flat @$60.42; 0 SETTLE on-log |
| **Bot $100 VM 11:02–12:05** | **0–0** | **$0** | still frozen @$60.61 |

### 11:02→12:05 path (this report)

- **11:02 prior cron (PR #69):** DO OR DIE **FRESH** @10:56 — **$52.99 / 430 / 86% / +$48.48**; post-SOL cash **~$33.39** / ~**4 opens** on `0700`; halt floor $25
- **12:05 pull:** DO OR DIE transcript **advanced** — `0700` settled off-log; newest filled mark **$60.42 / 438 / +$55.92** flat; Bot $100 still @00:46; transcript now **10.26 MiB / 10259048 bytes / 94569 lines**
- **No newer live trading agent** besides DO OR DIE (scan: only these two + this automation)
- Agent IDLE since ~11:16 → mark age **~49 min** at pull; further post-11:16 trading would not appear here

**Net vs prior cron:** **+8 closes / +$7.44 closed PnL / +$7.43 equity** — bankroll recovered toward start; still below day high.

### Risk / ops notes

- Last confirmed log **~11:16**; freshness **~49 min STALE** despite **CHANGED** vs 11:00 cron.
- Closed book **86%** at **438** / **+$55.92**; bankroll **$60.42** (**−$33.33** vs $93.75 day; **−$1.12** vs $61.54 start).
- Mode: **halt floor $25** / cash_target OFF / SPRINT OFF; SAVE not hit; flat scanning `070730`.
- **Zero** SETTLE on-log for the +8 closes — treat hourly W–L as closed-count / equity delta, not fully tape-attributed.
- Prefer filled `closed=438`, not resume `closed=538`.
- Events file: prior PR/artifact history; trading activity is in transcript tool outputs.
