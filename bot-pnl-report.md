# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~16:06 UTC (automation cron)  
**Data freshness:** **FRESH ~5 min** — newest confirmed dump **16:00:39 UTC** (`equity=$79.90`, `cash=$79.90`, open **0**, `closed=398`, win% **87**, pnl **+$55.51**). `HALT_FLOOR=$42`. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **RUNNING** (last bot log **16:01:01**; agent tools through ~**16:02**).  
**Source:** `state_live.json` / `runner_live.log` via DO OR DIE transcript pull @16:02.  
**Bot status (last confirmed):** **LIVE / not halted**, flat cash=equity **~$79.90**, open **0**, **RTP-20** on core **BNB / XRP / BTC**. Risk: **halt_floor=$42**, trail **0.65×HW**, risk sizing **24% edge_kelly** (edge_wr **92.5%**). Early-tip **off**. Watching 16:15 window (mids still in coin-flip band).

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$79.90** (open **0**, **halted=False**) @16:00:39 |
| **Mark equity** | **$79.90** @16:00:39 |
| **Prior report (PR #25 / 15:00)** | mark **$57.53** / cash **$56.75** open1 / closed **387 / +$38.71** (was STALE @14:35) |
| **Δ vs prior report mark** | **+$22.37** (**$57.53 → $79.90**) |
| **Δ closed PnL vs prior** | **+$16.80** (**+$38.71 → +$55.51**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$13.85** at last mark (**$79.90**) |
| **Day equity vs halt-log start ($61.54)** | **+$18.36** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**; lifetime +11 closes since imply day improved, exact n/wr unknown) |
| **Lifetime closed (confirmed @16:00:39)** | **398 closes · 87% · +$55.51** |
| **Hourly 14:00–15:00** | wake flat **$78.87** → bleed to **$57.53** @14:35 → recover **$70.50** @15:08; closed **382→391**; closed PnL **+$55.25→+$45.94** |
| **Hourly 15:00–16:00** | mark **$70.50 → $79.90** (**+$9.40** from 15:08 wake); closed **391→398**; closed PnL **+$45.94→+$55.51** (**+$9.56**); vs prior-cron mark **+$22.37** |
| **vs prior hourly report (PR #25)** | book repaired after settle hole; flat again; closed book **+$17** |

Bot recovered from the **~$57** RTP-20 hole: open inventory settled (XRP **+$3.89** @15:08), then ground **+$9.40** more through the 15:00 hour to flat **~$80**. Lifetime closed back to **+$55.51 @87%** — roughly matching the 14:07 wake print. Treat as **FRESH**.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @11:05 | **15–6** | **−$44.52** | high (was fresh then) |
| AUG05 @13:22 | **n=30** | **−$29.43** | high (prior cron) |
| AUG05 @14:26 | **30–7** (n=37, wr 81%) | **−$32.65** | high |
| AUG05 @14:34 | **n=39** (wr 77%) | **−$54.72** | high — **still last formal** |
| Equity path @15:08 (prior cron end was $57.53) | — | **−$23.25** vs $93.75 ($70.50) | high |
| **Equity path @16:06 (this cron)** | — | **−$13.85** mark ($79.90) | **high / fresh** |

Prefer marked equity for day P&L. Day equity improved **+$22.37** vs the 15:00 cron mark. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — still not refreshed as a midnight rollup.
- Lifetime closed path: **387** (@14:35) → **391** (@15:08) → **398** (@15:57–16:00), closed PnL **+$55.51**.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Resume settle 09:02–09:04 | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |
| Prior report 11:05 | **369** | **~87** | **+$48.90** | **$72.12** flat **LIVE** |
| Prior report 12:02 | **376** | **88** | **+$57.49** | **$81.20** flat **LIVE** |
| Rebound print 12:15 / 13:21 | **378** | **88** | **+$63.99** | **$87.65** flat **LIVE** |
| Peak cash ~13:30 | **~378+** | — | — | cash/HW peak **~$92.42** |
| Wake 14:07 | **382** | **87** | **+$55.25** | **$78.87** flat **LIVE** |
| RTP-20 @14:35 (prior cron) | **387** | **87** | **+$38.71** | cash **$56.75** / open **1** / mark **$57.53** |
| Wake / settle @15:08 | **391** | **87** | **+$45.94** | **$70.50** flat **LIVE** |
| **Latest @16:00:39 (this cron)** | **398** | **87** | **+$55.51** | **$79.90** flat **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193** → nuke/rebound **$72→$88** → peak **~$92** → settle bleed **~$57** → recover **~$80**.

Note: some log tails also show stray equity lines with `closed≈200` / cash **~$120–$137** (AUG04 tickers). Those conflict with the continuous live series (`closed` 387→398) and are **ignored** for headline metrics.

---

## Hourly win / loss (2026-08-04 → 08-05 UTC)

Closed-trade PnL only unless noted as equity/cash. Late hours from equity/cash prints and settle lines.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | reconstructed (prior day) |
| … | … | … | (earlier hours unchanged; see prior reports) |
| **00:00–01:00** | closed **+9** (326→335) | closed **−$2.76**; flat **$98 → $73** | early-tip halt |
| **01:00–02:00** | closed **+8** (335→343) | closed **+$2.58**; flat **$73 → $123** | tip settle + grind |
| **02:00–09:00** | freeze / resume | WD freeze then LIVE @09:02 | see prior |
| **09:00–10:00** | cash path | **+$2.03** (**$117.99 → $120.02**) | LIVE again |
| **10:00–11:00** | closed **+21** (348→369) | cash **−$47.90** (**$120 → $72**) | ETH/BTC/SOL nukes |
| **11:00–12:00** | closed **+7** (369→376) | cash **+$9.08**; closed PnL **+$8.59** | rebound; core trim |
| **12:00–13:00** | closed **+2** (376→378) | cash **+$6.45** (**$81.20 → $87.65**); then **~65m freeze** | BTC/XRP TP |
| **13:00–14:00** | closed **+4** (378→382) by wake | peak **~$92.42** then giveback; wake flat **$78.87**; closed PnL **−$8.74**; **~30m freeze** | 0930 settle + drawdown |
| **14:00–15:00** | closed **+9** (382→391) | mark path **$78.87 → $57.53 → $70.50**; closed PnL **+$55.25 → +$45.94** (**−$9.31** vs 14:07); RTP-20 + XRP settle win | hole then partial recover |
| **15:00–16:00** | closed **+7** (391→398) | mark **$70.50 → $79.90** (**+$9.40**); closed PnL **+$45.94 → +$55.51** (**+$9.56**); flat open=0 | recovery / print hour |

### 14:00–15:00 path (updated this report)

- **14:07:** wake flat **$78.87** / closed **382 / +$55.25**
- **14:28–14:35:** anti-nuke → RTP-20; mark **$57.53** / cash **$56.75** / open **1** / closed **387 / +$38.71**; HW reanchored **61.17**, floor **$42**
- **14:36 → ~15:08:** agent **IDLE ~32m** (visibility gap; no equity dumps)
- **15:08:17:** **SETTLE XRP 1100 YES WIN +$3.89** → cash/eq **$70.50** / closed **391 / +$45.94** / open **0**
- **15:08:21:** `RESTART kalshi-live`; stack healthy; HW **~$70.50**

**Net 14–15 (to 15:08):** closed book **−$9.31** vs 14:07 wake; equity **−$8.37** vs wake flat after partial recover from the **$57** hole.

### 15:00–16:00 path (this report)

- **15:08:** flat **$70.50** / closed **391 / +$45.94**; LIVE orders resume (BTC 1115 bid seen)
- **15:08 → 15:57:** closed **391→398** (**+7**), cash **+$9.40** to **$79.90**, closed PnL **+$9.56** — per-trade path **not** in tailed logs (aggregate dumps only)
- **15:57–16:00:** flat held **$79.90** / open **0** / closed **398 / +$55.51**; rich 99¢ favorites **skipped** by mispricing gate (`rich_entry>=0.950`)
- **16:01:** watching 16:15 BNB/XRP/BTC — mids **0.48–0.60**, below entry band **[0.70, 0.999)**

**Net this hour (15:08→16:00):** mark **+$9.40**; closed PnL **+$9.56**. vs prior cron last mark (**$57.53**): **+$22.37**.

**Day pace (through last confirmed mark):** equity **−$13.85** vs 10:00 baseline ($93.75 → $79.90). Lifetime closed **~$55.51** net with **87%** WR across **398** closes. AUG05 formal calendar still **−$54.72** (stale).

---

## How the bot is working

**What's working**
- **Recovery hour:** book climbed **~$57 → ~$80** since the prior cron; lifetime closed PnL back to **+$55.51** (≈ 14:07 wake level).
- Confirmed **XRP settle win +$3.89** closed the leftover open from RTP-20 restart.
- Ops: agent **RUNNING** again; keep-alive / watchdog / runner stack live; **no new multi-tens-of-minutes freeze** after the 14:36–15:08 IDLE gap.
- Core still **BNB/XRP/BTC only**; risk back to **edge_kelly 24%** with positive edge (wr **92.5%**, ev **+$0.49**).
- Mispricing gate is blocking rich ≥95¢ entries (skips 99¢ NO favorites) — intentional restraint.

**What's not / risks**
- AUG05 formal day-book still **−$54.72** last compute; settle remains the structural bleed when inventory is held.
- Visibility gap **~32m** after 14:35 (IDLE) before 15:08 wake — still an ops reliability issue even if recovered.
- Per-trade detail for the **+7** closes that printed **+$9.56** in the 15:00 hour is missing from tailed logs.
- Entry scarcity now: new 16:15 window stuck in coin-flip mids; bot flat and waiting.
- External alerts still **unarmed** (webhook unset).
- Stray AUG04 / `closed≈200` equity lines in log tails can confuse monitors — always prefer continuous `closed` count series.

**Bottom line:** Bot is **LIVE, flat, and recovering**. Last confirmed book: **398 @87% / +$55.51**, mark **~$79.90**, floor **$42**. The 15:00 hour was an **up hour** (mark **+$9** from 15:08 wake, **+$22** vs prior-cron hole). Day equity still **−$14** vs 10:00 baseline but **+$18** vs halt-log start. Needs a fresh AUG05 calendar recompute to refresh the day W–L table.

---

## Proof lines (from DO OR DIE transcript)

```
reanchored HW 92.4226 -> 61.1708; floor will bind at max(42, 0.65*61.17)=42.00
HALT_FLOOR=42
[14:35:42] equity=$57.53 cash=$56.75 open=1 closed=387 win%=87 pnl=+38.7077
[15:08:17] SETTLE KXXRP15M-26AUG051100-00 YES WIN pnl=+3.8864 cash=$70.50 equity=$70.50
[15:08:18] equity=$70.50 cash=$70.50 open=0 closed=391 win%=87 pnl=+45.9437
[15:08:21] RESTART kalshi-live (no PID for bot/runner.py)
[15:08:23] OK kalshi-live pid=165990
[15:08:33] HB cash=$70.50 pv=0 open=0 halted=False hw=70.5022
[15:57:38] equity=$79.90 cash=$79.90 open=0 closed=398 win%=87 pnl=+55.5081 risk=24.0%(edge_kelly) edge_wr=92.5%
[16:00:39] equity=$79.90 cash=$79.90 open=0 closed=398 win%=87 pnl=+55.5081
[16:01:01] watch KXBTC15M-26AUG051215-15 839s left mid=0.595 — need [0.7,0.999)
HALT_FLOOR 42 | SERIES KXBNB15M,KXXRP15M,KXBTC15M | PRE_SETTLE_EXIT_SECS 60
26AUG05: n=39 wr=77% pnl=-54.72 tp=+20.12 fade=+4.67 settle=-79.52   # last formal @14:34
```
