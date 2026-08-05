# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~15:08 UTC (automation cron)  
**Data freshness:** **STALE ~31 min** — newest confirmed dump **14:35:42 UTC** (`equity=$57.53`, `cash=$56.75`, open **1**, `closed=387`, win% **87**, pnl **+$38.71**). HW reanchored **$61.17**, `HALT_FLOOR=$42`. No equity/settle dumps after **14:35:49**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last message **14:35:57**; updatedAt **14:36:11**).  
**Source:** `state_live.json` / `health.json` / `runner_live.log` via DO OR DIE transcript pull @15:06.  
**Bot status (last confirmed):** **LIVE / not halted**, cash **~$56.75** with **1 open** (mark **$57.53**), **RTP-20** ratchet TP printer on core **BNB / XRP / BTC**. Risk: **halt_floor=$42**, trail **0.65×HW**, session HW **$61.17** (reanchored from peak **$92.42**), soft BN / pre-settle exits on, early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$56.75** (open **1**, **halted=False**) @14:35:42 |
| **Mark equity** | **$57.53** @14:35:42 |
| **Session HW (current)** | **$61.17** (reanchored @14:35 from peak **$92.42**) |
| **Peak HW today (pre-reanchor)** | **$92.42** (~13:30) |
| **Prior report (PR #24 / 14:00)** | cash **$65.46** open2 / last flat **$87.65** / closed **378 / +$63.99** (was STALE @13:22) |
| **Δ vs prior report last flat** | **−$30.12** (**$87.65 → $57.53** mark) |
| **Δ closed PnL vs prior** | **−$25.28** (**+$63.99 → +$38.71**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$36.22** at last mark (**$57.53**) |
| **Day equity vs halt-log start ($61.54)** | **−$4.01** (last mark) |
| **AUG05 calendar closed book** | **n=39 / 77% / −$54.72** @14:34 (**refreshed**; was n=30/−$29.43) |
| **AUG05 W–L (14:26 checkpoint)** | **30–7** (**−$32.65**, n=37) — later worsened to n=39/−$54.72 |
| **Lifetime closed (last confirmed @14:35:42)** | **387 closes · 87% · +$38.71** |
| **Hourly 13:00–14:00** | wake→peak **$92.42**→freeze; wake flat **$78.87**; closed **378→382**; closed PnL **+$63.99→+$55.25** (**−$8.74**) |
| **Hourly 14:00–15:00** | mark **$78.87 → $57.53** (**−$21.34**); closed **382→387**; closed PnL **+$55.25→+$38.71** (**−$16.54**); RTP-20 + floor **$42** |
| **vs prior hourly report (PR #24)** | 0930 settle resolved into book; then further settle bleed + another freeze; closed book **−$25** |

Bot briefly printed a **session high (~$92)** after the prior-report open risk settled, then **froze ~30m**, woke into more trading, and closed the hour near **$57–$58** after settle nukes. Lifetime closed still green (**+$39 @87%**) but **down ~$25** vs the 14:00 cron print. Treat post-**14:35** as **STALE**.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @11:05 | **15–6** | **−$44.52** | high (was fresh then) |
| AUG05 @13:22 | **n=30** | **−$29.43** | high (prior cron) |
| AUG05 @14:26 | **30–7** (n=37, wr 81%) | **−$32.65** | **high** |
| AUG05 @14:34 | **n=39** (wr 77%; W–L not rebroken) | **−$54.72** | **high** |
| Equity path last flat prior cron | — | **−$6.10** vs $93.75 ($87.65) | high then |
| **Equity path @15:08 (this cron)** | — | **−$36.22** mark ($57.53) | **stale** (~31m) |

Prefer marked equity for day P&L when fresh. AUG05 closed book **worsened sharply** in the 14:00 hour: **−$29.43 → −$54.72** (**−$25.29**), driven by settle losses (**settle −$79.52** on the day split vs TP **+$20.12** / fade **+$4.67**).

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — still not refreshed as a midnight rollup.
- Lifetime closed path: **378** (@13:21) → **382** (@14:07) → **384** (@14:13) → **385** (@14:28) → **387** (@14:35), closed PnL **+$38.71**.

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
| Post fade/TP 14:13 | **384** | **88** | **+$58.56** | cash **$84.18** (mark ~$82) |
| Anti-nuke 14:28 | **385** | **88** | **+$60.77** | cash **$61.95** / open **2** / mark **$84.02** |
| **RTP-20 @14:35 (this cron)** | **387** | **87** | **+$38.71** | cash **$56.75** / open **1** / mark **$57.53** |

\*no dumps after 14:35:49; agent IDLE.

Path: 10:00 baseline **$93.75** → ATH **$193** → nuke/rebound **$72→$88** → peak **~$92** → settle bleed + freezes → **~$57**.

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
| **13:00–14:00** | closed **+4** (378→382) by wake | peak cash/HW **~$92.42** then giveback; wake flat **$78.87**; closed PnL **−$8.74** (**+$63.99→+$55.25**); **~30m freeze** 13:37–14:07 | 0930 settle + drawdown |
| **14:00–15:00** | closed **+5** (382→387) | mark **−$21.34** (**$78.87→$57.53**); closed PnL **−$16.54** (**+$55.25→+$38.71**); AUG05 **−$32.65→−$54.72** | settle bleed; RTP-20 @14:35 |

### 13:00–14:00 path (confirmed this report)

- **13:21:50:** wake — flat **$87.65** / closed **378 / 88% / +$63.99**
- **13:21:53–58:** BTC+XRP 0930 fills → cash **$65.46**, open **2**
- **~13:29–13:30:** cash climbs **65.46 → 78.98 → 92.42** (session HW peak) — 0930 path resolved into book
- **13:31–13:36:** cash **79.41 → 61.15**
- **13:37 → 14:07:** **~30m freeze** (runner gap 30m25s / WD gap 30m31s)
- **14:07:33:** wake flat **$78.87** / closed **382 / 87% / +$55.25**; HW still **$92.42**

**Net 13–14:** brief peak to **~$92**, then drawdown + freeze; closed book **−$8.74** vs 13:21; wake equity **$78.87** (**−$8.78** vs prior flat **$87.65**).

### 14:00–15:00 path (this report)

- **14:07–14:08:** new XRP/BTC 1015 entries → cash **$52.70**, open filled
- **14:10–14:14:** FULL ENGINE RESTART / freeze-recovery surgery; process flaps then stack healthy
- **14:11:50:** SPIKE FADE BTC **+$2.31** → cash **$70.61**
- **14:11:55 → 14:13:31:** BNB NO fill @0.81 then TAKE PROFIT **+$2.22** → cash **$84.18**; closed **384 / +$58.56**
- **14:14 → 14:26:** cash **~$84 → ~$62**; AUG05 **37 / 30–7 / −$32.65** (settle bucket **−$57.45**)
- **14:28:** anti-nuke deploy (floor **$45**, soft BN flat-block); cash **$61.95** open **2**; closed **385 / +$60.77**; mark **$84.02**
- **14:34:** AUG05 **39 / 77% / −$54.72**; book cash **$61.17**; filled PnL **+$38.71**
- **14:35:** **RTP-20** restart + HW reanchor **92.42→61.17**; floor **$42**; cash **$56.75** / mark **$57.53** / open **1** / closed **387 / 87% / +$38.71**
- **14:36 → 15:08:** agent **IDLE**; **no further** dumps

**Net this hour vs wake flat ($78.87):** mark **−$21.34** to **$57.53**; closed PnL **−$16.54**. vs prior cron last flat (**$87.65**): **−$30.12**.

**Day pace (through last confirmed mark):** equity **−$36.22** vs 10:00 baseline ($93.75 → $57.53). Lifetime closed **~$39** net with **87%** WR across **387** closes. AUG05 calendar **−$54.72**.

---

## How the bot is working

**What's working**
- TP / spike-fade edge still prints when allowed: BTC fade **+$2.31**, BNB TP **+$2.22** in the 14:11–14:13 window; day split still shows TP **+$20.12** + fade **+$4.67**.
- Ops stack recovered twice (13:21 and 14:07) after multi-tens-of-minutes freezes; freeze-recovery jump detection + `restart_engine` landed ~14:10.
- Core remains **BNB/XRP/BTC only**; lifetime closed book still **green (+$39 @87%)**.
- Risk ratchet: floor lowered with book (**$48→$45→$42**) and HW reanchored so trail doesn't false-halt above cash.

**What's not / risks**
- **Settle nukes dominate:** AUG05 settle **−$79.52** vs TP/fade **+$24.79** — same failure mode as the morning ETH/SOL/BTC nukes.
- **Recurring freezes:** ~65m (12:16–13:21) then ~30m (13:37–14:07); agent again **IDLE ~31m** with **1 open** and no dumps.
- Day equity **−$36** vs 10:00; AUG05 **−$55**; lifetime closed **−$25** since the 14:00 cron print.
- External alerts still **unarmed** (webhook unset).
- RTP-20 just deployed @14:35 (re-allows half-size bn=flat entries with pre-settle flatten) — **too fresh to judge**; last contact left inventory on.

**Bottom line:** Bot is **LIVE but bleeding on settles**. Last confirmed book: **387 @87% / +$38.71**, mark **~$57.53**, floor **$42**. The 14:00 hour was a **down hour** (mark **−$21**, closed PnL **−$17**, AUG05 **−$22** from the 14:26 checkpoint). Ops reliability + settle exposure remain the constraints. Needs a DO OR DIE nudge (or fresh `state_live` / settle dump) before trusting post-14:35 numbers.

---

## Proof lines (from DO OR DIE transcript)

```
[13:21:50] equity=$87.65 cash=$87.65 open=0 closed=378 win%=88 pnl=+63.9913
[13:21:58] LIVE FILL ... cash=$65.46  |  AUG05 pnl -29.43 n 30
13:37:02 -> 14:07:27  gap=30m25s  (watchdog gap ~30m31s)
[14:07:33] equity=$78.87 cash=$78.87 open=0 closed=382 win%=87 pnl=+55.2489
[14:11:50] SPIKE FADE KXBTC15M-26AUG051015-15 ... pnl=+2.3133 cash=$70.61
[14:13:31] TAKE PROFIT KXBNB15M-26AUG051015-15 ... pnl=+2.2174 cash=$84.18
cash now 62.11 hw 92.42 halted False
AUG05 trades 37 pnl -32.65
W/L 30 7 wr 81%
by exit {'take_profit': 20.12, 'spike_fade': 4.67, 'settle': -57.45}
[14:28:38] equity=$84.02 cash=$61.95 open=2 closed=385 win%=88 pnl=+60.7725
26AUG05: n=39 wr=77% pnl=-54.72 tp=+20.12 fade=+4.67 settle=-79.52
n filled 387 total pnl 38.71
reanchored HW 92.4226 -> 61.1708; floor ... =42.00
[14:35:42] equity=$57.53 cash=$56.75 open=1 closed=387 win%=87 pnl=+38.7077
HALT_FLOOR=42 / HALT_TRAIL_FRAC=0.65
```
