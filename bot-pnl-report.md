# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~17:47 UTC (automation cron)  
**Data freshness:** **FRESH ~8–9 min** — newest confirmed dump **17:38:40 UTC** (`equity=$90.65`, `cash=$90.65`, open **1**, `closed=402`, win% **88**, pnl **+$66.39**). Health confirm **17:39:17** (`cash 90.6496`, issues `[]`). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last tools **17:39:17**; last bot log **17:39:15**).  
**Source:** `runner_live.log` / healthz via DO OR DIE transcript pull @17:47.  
**Bot status (last confirmed):** **LIVE / not halted**, mark **~$90.65**, open **0–1** (flat-ish after BNB TP), **RTP-20 printer replay** on core **BNB / XRP / BTC**. Risk: **halt_floor=$20** (cut from $42 @17:38), trail **0.65×HW**, risk sizing **24% edge_kelly** (edge_wr **95.6%**). Lognormal gate **OFF**. Early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$90.65** (health **$90.6496**, **halted=False**) @17:38–17:39 |
| **Mark equity** | **$90.65** @17:38:40 |
| **Prior report (PR #26 / 16:00)** | mark **$79.90** / cash **$79.90** open0 / closed **398 / +$55.51** (FRESH @16:00) |
| **Δ vs prior report mark** | **+$10.75** (**$79.90 → $90.65**) |
| **Δ closed PnL vs prior** | **+$10.88** (**+$55.51 → +$66.39**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$3.10** at last mark (**$90.65**) |
| **Day equity vs halt-log start ($61.54)** | **+$29.11** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**; lifetime +4 closes since imply day improved) |
| **Lifetime closed (confirmed @17:38:40)** | **402 closes · 88% · +$66.39** |
| **Hourly 15:00–16:00** | mark **$70.50 → $79.90** (**+$9.40**); closed **391→398**; closed PnL **+$45.94→+$55.51** (**+$9.56**) |
| **Hourly 16:00–17:00** | mark **$79.90 → $86.26** (**+$6.36**); closed **398→401**; closed PnL **+$55.51→+$62.20** (**+$6.69**); **3–0** (BNB TP / XRP fade / BTC TP) |
| **Hourly 17:00–17:39** | mark **$86.26 → $90.65** (**+$4.39**); closed **401→402**; closed PnL **+$62.20→+$66.39** (**+$4.19**); **1–0** BNB TP; ~35m fill starvation then printer-replay restart |
| **vs prior hourly report (PR #26)** | book continued recovery; flat-ish **~$90.65**; closed book **+$11** |

Bot extended the recovery: **~$80 → ~$90** since the 16:00 cron. Lifetime closed **+$66.39 @88%** across **402** closes — best lifetime closed print since the 12:15 rebound era. Day equity nearly back to the 10:00 baseline (**−$3.10**). Treat as **FRESH**.

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
| Equity path @16:00 (prior cron) | — | **−$13.85** vs $93.75 ($79.90) | high |
| **Equity path @17:47 (this cron)** | — | **−$3.10** mark ($90.65) | **high / fresh** |

Prefer marked equity for day P&L. Day equity improved **+$10.75** vs the 16:00 cron mark. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute. Implied improvement from +4 lifetime closes (all green in the 16–17 window) is not yet formalized.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38 prior-day formal) — still not refreshed as a midnight rollup.
- Lifetime closed path: **398** (@16:00) → **401** (@16:16) → **402** (@17:38), closed PnL **+$66.39**.

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
| RTP-20 @14:35 | **387** | **87** | **+$38.71** | cash **$56.75** / open **1** / mark **$57.53** |
| Wake / settle @15:08 | **391** | **87** | **+$45.94** | **$70.50** flat **LIVE** |
| Prior report @16:00:39 | **398** | **87** | **+$55.51** | **$79.90** flat **LIVE** |
| 1215 window @16:16 | **401** | **88** | **+$62.20** | **$86.26** flat **LIVE** |
| **Latest @17:38:40 (this cron)** | **402** | **88** | **+$66.39** | **$90.65** open1 **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193** → nuke/rebound **$72→$88** → peak **~$92** → settle bleed **~$57** → recover **~$80 → ~$90**.

Note: state-file resume counter can show **closed≈494** after restarts — that is a **different ledger**. Prefer continuous equity-line `closed` series (**398→401→402**). Also ignore stray AUG04 / `closed≈200` equity lines.

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
| **16:00–17:00** | closed **+3** (398→401) **3–0** | mark **$79.90 → $86.26** (**+$6.36**); closed PnL **+$55.51 → +$62.20** (**+$6.69**) | 1215 BNB/XRP/BTC closes |
| **17:00–17:39** | closed **+1** (401→402) **1–0** | mark **$86.26 → $90.65** (**+$4.39**); closed PnL **+$62.20 → +$66.39** (**+$4.19**) | lognormal starve → printer replay BNB TP |

### 16:00–17:00 path (this report)

- **16:00:39:** flat **$79.90** / closed **398 / +$55.51** / open **0**
- **16:02:** LIVE FILL BNB YES @0.71 → cash **$70.31** open **1**; full engine restart @16:02:56
- **16:04:** mark **$79.71** / cash **$60.67** / open **2** (inventory on)
- **16:09:** LIVE FILL BTC YES @0.91 → cash **$63.70**
- **16:16:16:** flat **$86.26** / closed **401 / +$62.20** / win% **88** — three green closes:
  - BNB 1215 YES TP **+$3.45**
  - XRP 1215 YES fade **+$2.56**
  - BTC 1215 YES TP **+$0.69**
- **16:26:** another full engine restart; resumed flat **$86.26**; lognormal gate began starving fills (`lognormal_ok 0`, 608 skips by later count)
- **16:40–17:31:** mark held **$86.26** / closed **401** (no new closes)

**Net 16–17:** mark **+$6.36**; closed PnL **+$6.69**; **3–0**.

### 17:00–17:39 path (partial hour)

- **16:56 → 17:31:** ~**35m** fill starvation / visibility gap under lognormal overlay; equity dump @17:31 still **$86.26 / 401 / +$62.20**
- **17:38:26:** FULL ENGINE RESTART — **RTP-20 printer replay**: `LOGNORMAL_GATE=0`, `HALT_FLOOR=20`, `CONFIRM_POLLS=1`, `MIN_SECS_LEFT=25`
- **17:38:40:** TAKE PROFIT BNB 1345 YES **+$4.19** → cash/eq **$90.65** / closed **402 / +$66.39** / open **1** / win% **88**
- **17:39:17:** health ok cash **90.6496**; agent went **IDLE** shortly after

**Net this partial hour (17:00→17:39):** mark **+$4.39**; closed PnL **+$4.19**. vs prior cron last mark (**$79.90**): **+$10.75**.

**Day pace (through last confirmed mark):** equity **−$3.10** vs 10:00 baseline ($93.75 → $90.65). Lifetime closed **~$66.39** net with **88%** WR across **402** closes. AUG05 formal calendar still **−$54.72** (stale).

---

## How the bot is working

**What's working**
- **Second recovery leg:** book climbed **~$80 → ~$90** since the prior cron; lifetime closed PnL **+$66.39** (best since midday rebound).
- Clean **3–0** 1215 window (BNB TP / XRP fade / BTC TP) printed **+$6.69** closed.
- Printer-replay restart immediately banked BNB TP **+$4.19** — TP/pre-settle path still the money.
- Core still **BNB/XRP/BTC only**; edge_kelly **24%** with strong edge (wr **95.6%**, ev **+$2.03** @17:38).
- Day equity nearly healed vs 10:00 baseline (**−$3.10** only).

**What's not / risks**
- **Lognormal 80% overlay starved fills** for ~35m (608 lognormal skips); agent disabled it @17:38 — watch whether that reintroduces bad entries.
- **HALT_FLOOR cut $42 → $20** widens drawdown room; HW last printed **~$79.90** still lagging cash **$90.65** until reanchor.
- Repeated **FULL ENGINE RESTART**s (16:02, 16:26, 17:38) and brief healthz 503s — ops fragility continues.
- VM / agent **IDLE** gaps persist (agent IDLE @17:39 while runner was healthy).
- AUG05 formal day-book still **−$54.72** last compute; needs refresh.
- Dual closed counters (equity-line **402** vs state-file **~494**) — always prefer equity-line series.
- External alerts still **unarmed** (webhook unset).

**Bottom line:** Bot is **LIVE and recovering hard**. Last confirmed book: **402 @88% / +$66.39**, mark **~$90.65**, floor **$20**. The 16:00 hour was an **up hour** (**+$6.36** mark / **3–0**), and 17:00 partial continued up (**+$4.39**). Day equity **−$3** vs 10:00 baseline / **+$29** vs halt-log start. Needs a fresh AUG05 calendar recompute and HW reanchor after the floor cut.

---

## Proof lines (from DO OR DIE transcript)

```
[16:00:39] equity=$79.90 cash=$79.90 open=0 closed=398 win%=87 pnl=+55.5081  unit=20.61  risk=24.0%(edge_kelly) edge_wr=92.5% ev=$+0.488
[16:02:11] LIVE FILL YES 13.50 @ ~0.71 on KXBNB15M-26AUG051215-15 status=executed cash=$70.31 risk=24.0% bn=flat
[16:02:56] === FULL ENGINE RESTART ===
[16:04:09] equity=$79.71 cash=$60.67 open=2 closed=398 win%=87 pnl=+55.5081
[16:09:03] LIVE FILL YES 10.96 @ ~0.91 on KXBTC15M-26AUG051215-15 status=executed cash=$63.70 risk=24.0% bn=flat
[16:16:16] equity=$86.26 cash=$86.26 open=0 closed=401 win%=88 pnl=+62.1993  unit=22.26  risk=24.0%(edge_kelly) edge_wr=95.6% ev=$+1.802
CLOSED NB15M-26AUG051215-15 yes entry=0.71 pnl=3.4452 take_profit
CLOSED RP15M-26AUG051215-15 yes entry=0.71 pnl=2.5555 spike_fade
CLOSED TC15M-26AUG051215-15 yes entry=0.91 pnl=0.6905 take_profit
[16:26:25] === FULL ENGINE RESTART ===
since 16:26 — fills/orders 132 lognormal_ok 0 skips {'time_phase':57,'rich':1124,'other':1775,'bn':14,'lognormal':608}
[17:31:54] equity=$86.26 cash=$86.26 open=0 closed=401 win%=88 pnl=+62.1993
[17:38:26] === FULL ENGINE RESTART ===
HALT_FLOOR=20  LOGNORMAL_GATE=0  CONFIRM_POLLS=1  MIN_SECS_LEFT=25
[17:38:40] TAKE PROFIT KXBNB15M-26AUG051345-45 YES entry=0.70 mark=0.99 exit~0.99 pnl=+4.1874 cash=$90.65
[17:38:40] equity=$90.65 cash=$90.65 open=1 closed=402 win%=88 pnl=+66.3867  unit=23.39  risk=24.0%(edge_kelly) edge_wr=95.6% ev=$+2.027
health ok cash 90.6496 issues []
26AUG05: n=39 wr=77% pnl=-54.72 tp=+20.12 fade=+4.67 settle=-79.52   # last formal @14:34
```
