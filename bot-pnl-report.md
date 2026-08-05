# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~19:30 UTC (automation cron)  
**Data freshness:** **FRESH ~10 min** — newest confirmed dump **19:19:48 UTC** (`equity=$77.96`, `cash=$77.96`, open **1**, `closed=414`, win% **86**, pnl **+$53.34**). Live balance **$77.9643** @19:19:41; health ok @19:20:08 (`halted=False`, HW **$99.1154**). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last tools **~19:20:11**; last bot equity **19:19:48**).  
**Source:** `runner_live.log` / healthz via DO OR DIE transcript pull @19:30.  
**Bot status (last confirmed):** **LIVE / not halted**, mark **~$77.96**, open **1**, **RTP-20 printer replay** on core **BNB / XRP / BTC**. Risk: **halt_floor=$20**, trail **0.65×HW**, **cash_target=$105** SAVE_BANKROLL armed, risk sizing recently **~15% cut_neg_edge** (edge_wr ~77%, EV negative on last print). Lognormal gate **OFF**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$77.96** (live **$77.9643**, **halted=False**) @19:19–19:20 |
| **Mark equity** | **$77.96** @19:19:48 (open **1**) |
| **Prior report (PR #28 / 18:00)** | mark **$99.12** / cash **$99.12** open0 / closed **404 / +$74.85** (FRESH @18:06) |
| **Δ vs prior report mark** | **−$21.16** (**$99.12 → $77.96**) |
| **Δ closed PnL vs prior** | **−$21.51** (**+$74.85 → +$53.34**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$15.79** at last mark (**$77.96**) |
| **Day equity vs halt-log start ($61.54)** | **+$16.42** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**) |
| **Lifetime closed (confirmed @19:19:48)** | **414 closes · 86% · +$53.34** |
| **Hourly 17:00–18:00** | mark **$86.26 → $99.12** (**+$12.86**); closed **401→404**; closed PnL **+$62.20→+$74.85** (**+$12.65**); printer-replay **3W–0L** |
| **Hourly 18:00–19:20** | mark **$99.12 → $77.96** (**−$21.16**); closed **404→414**; closed PnL **+$74.85→+$53.34** (**−$21.51**); replay @18:30 **4W–4L / −$5.48** |
| **vs prior hourly report (PR #28)** | sharp giveback from session peak **~$99**; day equity **red again** vs 10:00 baseline |

Bot gave back the 18:00 recovery: **~$99 → ~$78** since the last cron. Lifetime closed slipped to **+$53.34 @86%** across **414** closes (−10 pp win-rate from 88%). Day equity flipped back red vs the 10:00 baseline (**−$15.79**). Treat as **FRESH**.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @14:34 | **n=39** (wr 77%) | **−$54.72** | high — **still last formal** |
| Equity path @18:12 (prior cron) | — | **+$5.37** vs $93.75 ($99.12) | high (prior) |
| **Equity path @19:30 (this cron)** | — | **−$15.79** mark ($77.96) | **high / fresh** |

Prefer marked equity for day P&L. Day equity fell **−$21.16** vs the 18:00 cron mark and is again **below** the 10:00 baseline. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute.

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
| Wake 14:07 | **382** | **87** | **+$55.25** | **$78.87** flat **LIVE** |
| RTP-20 @14:35 | **387** | **87** | **+$38.71** | cash **$56.75** / open **1** / mark **$57.53** |
| Wake / settle @15:08 | **391** | **87** | **+$45.94** | **$70.50** flat **LIVE** |
| Prior report @16:00:39 | **398** | **87** | **+$55.51** | **$79.90** flat **LIVE** |
| 1215 window @16:16 | **401** | **88** | **+$62.20** | **$86.26** flat **LIVE** |
| Prior report @17:38:40 | **402** | **88** | **+$66.39** | **$90.65** open1 **LIVE** |
| Prior report @18:06:00 | **404** | **88** | **+$74.85** | **$99.12** flat **LIVE** |
| Mid-hour @18:30:26 | **409** | **87** | **+$56.72** | **$83.57** flat **LIVE** |
| @19:05:08 | **411** | **86** | **+$49.74** | mark **$74.48** / cash **$63.32** open2 **LIVE** |
| **Latest @19:19:48 (this cron)** | **414** | **86** | **+$53.34** | **$77.96** open1 **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193** → nuke/rebound → recover **~$80 → ~$90 → ~$99** → giveback **~$78**.

Note: state-file resume counter can show **closed≈509** after restarts — that is a **different ledger**. Prefer continuous equity-line `closed` series (**404→414**). Ignore stray AUG03/AUG04 equity lines and mid-settle blips (e.g. `equity=$109.99` earlier).

---

## Hourly win / loss (2026-08-04 → 08-05 UTC)

Closed-trade PnL only unless noted as equity/cash. Late hours from equity/cash prints and settle lines.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured |
| … | … | … | (earlier hours unchanged; see prior reports) |
| **15:00–16:00** | closed **+7** (391→398) | mark **$70.50 → $79.90** (**+$9.40**); closed PnL **+$45.94 → +$55.51** (**+$9.56**) | recovery / print hour |
| **16:00–17:00** | closed **+3** (398→401) **3–0** | mark **$79.90 → $86.26** (**+$6.36**); closed PnL **+$55.51 → +$62.20** (**+$6.69**) | 1215 BNB/XRP/BTC closes |
| **17:00–18:00** | closed **+3** resolved (401→404) **3W–0L** (+$0 scratch) | mark **$86.26 → $99.12** (**+$12.86**); closed PnL **+$62.20 → +$74.85** (**+$12.65**) | printer-replay cutover + two 1400 settles |
| **18:00–19:20** | closed **+10** (404→414) | mark **$99.12 → $77.96** (**−$21.16**); closed PnL **+$74.85 → +$53.34** (**−$21.51**); replay **4W–4L / −$5.48** @18:30 | peak giveback; BNB 1430 loss −$7.07 |

### 18:00–19:20 path (this report)

- **18:06:00:** flat mark **$99.12** / closed **404 / +$74.85** / win% **88** (prior cron peak)
- **18:30:26:** SETTLE BTC 1430 NO **+$1.52** / SETTLE BNB 1430 YES **−$7.07** → equity **$83.57** / closed **409 / +$56.72** / win% **87**
- **@18:30:** printer-replay cumulative **`4W–4L WR=50% pnl=−$5.48`** (was **3W–0L / +$12.65** @18:06)
- **19:05:08:** mark **$74.48** / cash **$63.32** / open **2** / closed **411 / +$49.74** / win% **86**; **cash save armed** (`halt & SAVE_BANKROLL` when flat cash ≥ **$105**)
- **19:19:41–19:19:48:** live cash **$77.9643**; equity **$77.96** / open **1** / closed **414 / +$53.34** / win% **86**; still **LIVE**, floor **$20**, cash_target **$105**
- **19:20:08:** health ok — cash **77.9643**, high_water **99.1154**, halted=False

**Net 18–19 (through 19:20):** mark **−$21.16**; closed PnL **−$21.51**; +10 closes; win% **88 → 86**.

**Day pace (through last confirmed mark):** equity **−$15.79** vs 10:00 baseline ($93.75 → $77.96). Lifetime closed **~$53.34** net with **86%** WR across **414** closes. AUG05 formal calendar still **−$54.72** (stale).

### Risk / ops notes

- High-water still **~$99.12**; trail floor active (`halt_floor=$20 + 0.65×HW`).
- Edge model flipped to **cut_neg_edge** with negative EV on the last equity print — sizing cut vs the earlier 24% edge_kelly.
- Intermittent healthz flaps observed earlier; recovered by 19:20:08.
- Prefer equity-line closed (**414**) over state-file resume (**~509**).
