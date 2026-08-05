# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~20:02 UTC (automation cron)  
**Data freshness:** **FRESH ~9–14 min** — newest full equity dump **19:48:19 UTC** (`equity=$76.46`, `cash=$70.72`, open **1**, `closed=417`, win% **86**, pnl **+$49.16**). Newer cash-only print **$65.07** @19:53:36 (no matching equity/closed line). Last healthz **ok** @19:20:08; healthz **503** @19:48:24 (monitor flake). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last bot tools **~19:48:24**; last any tool **~19:54:32** diverted to autoquant). Runner still alive @19:53.  
**Source:** `runner_live.log` / live status via DO OR DIE transcript pull @20:02.  
**Bot status (last confirmed):** **LIVE / not halted**, mark **~$76.46** (cash **$65–$71** with open BTC), open **1** (`KXBTC15M-26AUG051600-00` NO @0.72). Risk: **halt_floor=$20**, trail **0.65×HW**, **cash_target=$105** SAVE_BANKROLL armed (not triggered), risk **15% cut_neg_edge** (edge_wr ~77%, EV negative). Lognormal gate **OFF**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$65.07** @19:53:36 (prior full print **$70.72** @19:48:19) — **halted=False** |
| **Mark equity** | **$76.46** @19:48:19 (open **1**) |
| **Prior report (PR #29 / 19:00)** | mark **$77.96** / cash **$77.96** open1 / closed **414 / +$53.34** (FRESH @19:19) |
| **Δ vs prior report mark** | **−$1.50** (**$77.96 → $76.46**) |
| **Δ closed PnL vs prior** | **−$4.19** (**+$53.34 → +$49.16**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$17.29** at last mark (**$76.46**) |
| **Day equity vs halt-log start ($61.54)** | **+$14.92** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**) |
| **Lifetime closed (confirmed @19:48:19)** | **417 closes · 86% · +$49.16** |
| **Hourly 18:00–19:20** | mark **$99.12 → $77.96** (**−$21.16**); closed **404→414**; closed PnL **+$74.85→+$53.34** (**−$21.51**) |
| **Hourly 19:20–19:48** | mark **$77.96 → $76.46** (**−$1.50**); closed **414→417**; closed PnL **+$53.34→+$49.16** (**−$4.19**); restart bucket **2W–1L / −$4.19** |
| **vs prior hourly report (PR #29)** | small further giveback; still **LIVE** under $105 cash-save arm; day equity still **red** |

Bot stayed **LIVE** after the sharp 18–19 giveback. Mark slipped another **~$1.50** (**$77.96 → $76.46**) with **+3** closes (**2W–1L / −$4.19** since the 19:19 restart). Cash under open BTC sits lower (**~$65–$71**). Day equity still red vs the 10:00 baseline (**−$17.29**). Treat as **FRESH**.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @14:34 | **n=39** (wr 77%) | **−$54.72** | high — **still last formal** |
| Equity path @19:30 (prior cron) | — | **−$15.79** vs $93.75 ($77.96) | high (prior) |
| Restart bucket @19:48:24 (since 19:19:41) | **2W–1L** | **−$4.19** | high |
| Since $105-arm (cumulative) | **n=6 / WR 83%** | **−$0.58** | high |
| **Equity path @20:02 (this cron)** | — | **−$17.29** mark ($76.46) | **high / fresh** |

Prefer marked equity for day P&L. Day equity fell another **−$1.50** vs the 19:00 cron mark and remains **below** the 10:00 baseline. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Resume settle 09:02–09:04 | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |
| Prior report 12:02 | **376** | **88** | **+$57.49** | **$81.20** flat **LIVE** |
| Wake 14:07 | **382** | **87** | **+$55.25** | **$78.87** flat **LIVE** |
| Wake / settle @15:08 | **391** | **87** | **+$45.94** | **$70.50** flat **LIVE** |
| Prior report @16:00:39 | **398** | **87** | **+$55.51** | **$79.90** flat **LIVE** |
| 1215 window @16:16 | **401** | **88** | **+$62.20** | **$86.26** flat **LIVE** |
| Prior report @18:06:00 | **404** | **88** | **+$74.85** | **$99.12** flat **LIVE** |
| Mid-hour @18:30:26 | **409** | **87** | **+$56.72** | **$83.57** flat **LIVE** |
| Prior report @19:19:48 | **414** | **86** | **+$53.34** | **$77.96** open1 **LIVE** |
| **Latest @19:48:19 (this cron)** | **417** | **86** | **+$49.16** | **$76.46** / cash **$70.72** open1 **LIVE** |
| Cash-only @19:53:36 | *(no equity line)* | — | — | cash **$65.07** **halted=False** |

Path: 10:00 baseline **$93.75** → ATH **$193** → recover **~$80 → ~$90 → ~$99** → giveback **~$78 → ~$76**.

Note: state-file resume counter can show **closed≈512** after restarts — that is a **different ledger**. Prefer continuous equity-line `closed` series (**414→417**). Ignore stray AUG03/AUG04 equity lines and mid-settle blips (e.g. earlier `equity~$643` on resume).

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
| **17:00–18:00** | closed **+3** resolved (401→404) **3W–0L** | mark **$86.26 → $99.12** (**+$12.86**); closed PnL **+$62.20 → +$74.85** (**+$12.65**) | printer-replay cutover |
| **18:00–19:20** | closed **+10** (404→414) | mark **$99.12 → $77.96** (**−$21.16**); closed PnL **+$74.85 → +$53.34** (**−$21.51**); replay **4W–4L / −$5.48** @18:30 | peak giveback |
| **19:20–19:48** | closed **+3** (414→417) **2W–1L** | mark **$77.96 → $76.46** (**−$1.50**); closed PnL **+$53.34 → +$49.16** (**−$4.19**) | XRP 1530 loss; BNB tiny win; BTC open |

### 19:20–19:53 path (this report)

- **19:19:48:** prior cron mark **$77.96** / closed **414 / +$53.34** / win% **86** / open **1**
- **19:20:08:** health ok — cash **77.9643**, high_water **99.1154**, halted=False
- **~19:30:** `pre_settle` BNB 1530 NO **+$1.56**; `settle` XRP 1530 NO **−$5.76**
- **~19:45:** `settle` BNB 1545 NO **+$0.01**
- **19:48:18–19:48:19:** resume/fill — LIVE FILL BTC 1600 NO **7.96 @ ~0.72**; equity **$76.46** / cash **$70.72** / open **1** / closed **417 / +$49.16** / win% **86**
- **19:48:24:** since restart **2W–1L / −$4.19**; since $105-arm **n=6 WR=83% / −$0.58**; need **+$34.28** to cash-save; healthz **503**
- **19:53:36:** runner still up; cash **$65.07** / halted=False (no new equity line)
- **19:53–19:54:** agent diverted to autoquant; bot runner left running

**Net 19–20 (through 19:48 equity):** mark **−$1.50**; closed PnL **−$4.19**; +3 closes; win% holds **86**.

**Day pace (through last confirmed mark):** equity **−$17.29** vs 10:00 baseline ($93.75 → $76.46). Lifetime closed **~$49.16** net with **86%** WR across **417** closes. AUG05 formal calendar still **−$54.72** (stale).

### Risk / ops notes

- High-water still **~$99.12**; trail floor active (`halt_floor=$20 + 0.65×HW`).
- Cash-save target **$105** still armed; **~$34–$40** short depending on cash print — not close to trigger.
- Edge model still **cut_neg_edge** / negative EV on last equity print — 15% risk sizing.
- healthz **503** @19:48 after last **ok** @19:20 — monitor flake, not a trading halt.
- Prefer equity-line closed (**417**) over state-file resume (**~512**).
- Agent IDLE after autoquant digression; runner process was still alive as of 19:53.

---

## How the bot is working

**What's working**
- Still **LIVE** and filling after the 18:00 peak giveback — no floor halt, cash-save not tripped.
- Restart bucket since 19:19 is small (**3** closes) and contained (**−$4.19**).
- Risk stack holding: floor **$20** + trail, cash_target **$105**, cut_neg_edge 15%.

**What's not / risks**
- Session still in drawdown from **~$99** HW → **~$76** mark (**−$23** from peak).
- Day equity **−$17** vs 10:00 baseline; formal AUG05 calendar still **−$55** (stale).
- Cash under open inventory drifted to **~$65** @19:53 — watch next settle on BTC 1600.
- Agent left bot ops for autoquant @19:54; rely on runner/keep-alive, not agent IDLE status.
- healthz flaky (503) — off-box alerts still the gap if the pod stalls.

**Bottom line:** Bot is **LIVE at ~$76 mark** (**−$1.50** this hour; closed **417 @86% / +$49**). Hourly closed book **2W–1L / −$4.19**. Day equity still red (**−$17** vs $93.75). Cash-save at **$105** remains the recovery arm.
