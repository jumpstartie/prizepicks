# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~22:06 UTC (automation cron)  
**Data freshness:** **STALE ~138 min** — newest full equity dump still **19:48:19 UTC** (`equity=$76.46`, `cash=$70.72`, open **1**, `closed=417`, win% **86**, pnl **+$49.16**). Newer cash-only print **$65.07** @19:53:36 (no matching equity/closed line). **No new equity, settle, fill, or closed-series lines after 19:48** in the DO OR DIE transcript (pull @22:02). Last healthz **ok** @19:20:08; healthz **503** @19:48:24. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last bot tools **~19:48:25** status / **~19:53:40** cash peek; last any tool **~19:54:33** diverted to autoquant). Runner last confirmed alive @19:53 (pid **213006**); **not re-verified after that**.  
**Source:** `runner_live.log` / live status via DO OR DIE transcript pull @22:02.  
**Bot status (last confirmed):** **LIVE / not halted** @19:53, mark **~$76.46** (cash **$65–$71** with open BTC), open **1** (`KXBTC15M-26AUG051600-00` NO @0.72). That BTC 1600 window almost certainly settled ~**20:00 UTC** — **settle outcome unknown** (data gap now spans **~2.3 hours**). Risk (last print): **halt_floor=$20**, trail **0.65×HW**, **cash_target=$105** SAVE_BANKROLL armed, risk **15% cut_neg_edge**. Lognormal gate **OFF**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$65.07** @19:53:36 (prior full print **$70.72** @19:48:19) — **halted=False** |
| **Mark equity** | **$76.46** @19:48:19 (open **1**) — **unchanged vs prior cron** |
| **Prior report (PR #31 / 21:00)** | mark **$76.46** / cash **$65–$71** open1 / closed **417 / +$49.16** (STALE @19:48) |
| **Δ vs prior report mark** | **$0.00** on last confirmed mark (**no newer print**) |
| **Δ closed PnL vs prior** | **$0.00** (**still +$49.16** / closed **417**) — **no new closes observed** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$17.29** at last mark (**$76.46**) |
| **Day equity vs halt-log start ($61.54)** | **+$14.92** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**) |
| **Lifetime closed (confirmed @19:48:19)** | **417 closes · 86% · +$49.16** |
| **Hourly 19:20–19:48** | mark **$77.96 → $76.46** (**−$1.50**); closed **414→417**; closed PnL **+$53.34→+$49.16** (**−$4.19**); restart bucket **2W–1L / −$4.19** |
| **Hourly 19:48–22:06** | **DATA GAP (~138 min)** — no equity/closed/settle lines; open BTC 1600 + any later windows unseen; cannot measure W–L or PnL |
| **vs prior hourly report (PR #31)** | numbers **unchanged**; ops risk **higher** (blackout extended ~76 → ~138 min; runner still unverified since 19:53) |

Last confirmed book is unchanged from the 20:00 and 21:00 crons. The material update is operational: **telemetry blackout now ~2.3 hours**, so BTC 1600 settle and any subsequent 15m windows are **unknown**. Treat headline PnL as **STALE / last-known**, not live.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @14:34 | **n=39** (wr 77%) | **−$54.72** | high — **still last formal** |
| Equity path @21:04 (prior cron) | — | **−$17.29** vs $93.75 ($76.46) | high (prior, still last mark) |
| Restart bucket @19:48:24 (since 19:19:41) | **2W–1L** | **−$4.19** | high (unchanged) |
| Since $105-arm (cumulative) | **n=6 / WR 83%** | **−$0.58** | high (unchanged) |
| **Equity path @22:06 (this cron)** | — | **−$17.29** mark ($76.46) | **stale — no new mark** |

Prefer marked equity for day P&L when fresh. Day equity print is **unchanged** vs the 20:00/21:00 crons; true mark after BTC 1600 (and later windows) is **unknown**. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute.

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
| **Latest confirmed @19:48:19** | **417** | **86** | **+$49.16** | **$76.46** / cash **$70.72** open1 **LIVE** |
| Cash-only @19:53:36 | *(no equity line)* | — | — | cash **$65.07** **halted=False** |
| **22:06 cron pull** | *(no newer line)* | — | — | **STALE — same as 19:48** |

Path: 10:00 baseline **$93.75** → ATH **$193** → recover **~$80 → ~$90 → ~$99** → giveback **~$78 → ~$76** → **gap after 19:48 (now ~138 min)**.

Note: state-file resume counter can show **closed≈512** after restarts — that is a **different ledger**. Prefer continuous equity-line `closed` series (**417** last confirmed). Ignore stray AUG03/AUG04 equity lines and mid-settle blips (e.g. earlier `equity~$643` on resume).

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
| **19:48–22:06** | **unknown** | **unknown** | **DATA GAP ~138 min** — agent IDLE; BTC 1600+ settles not observed |

### 19:48–22:06 path (this report)

- **19:48:18–19:48:19:** last equity — LIVE FILL BTC 1600 NO **7.96 @ ~0.72**; equity **$76.46** / cash **$70.72** / open **1** / closed **417 / +$49.16** / win% **86**
- **19:48:24:** since restart **2W–1L / −$4.19**; since $105-arm **n=6 WR=83% / −$0.58**; need **+$34.28** to cash-save; healthz **503**
- **19:53:36:** runner pid **213006** up; cash **$65.07** / halted=False (no new equity line)
- **19:53–19:54:** agent diverted to autoquant; bot runner left running
- **20:00–22:06:** **no transcript activity** — BTC 1600 market almost certainly settled; later 15m windows (1615/1630/…) may also have traded; mark/cash/closed **unconfirmed**

**Net since prior cron (21:00 → 22:06):** on confirmed prints, mark **$0.00** / closed PnL **$0.00** / closes **+0**. True hourly result **cannot be measured** until DO OR DIE (or another poll) returns a fresh equity line.

**Day pace (through last confirmed mark):** equity **−$17.29** vs 10:00 baseline ($93.75 → $76.46). Lifetime closed **~$49.16** net with **86%** WR across **417** closes. AUG05 formal calendar still **−$54.72** (stale).

### Risk / ops notes

- High-water still **~$99.12** (last print); trail floor active (`halt_floor=$20 + 0.65×HW`).
- Cash-save target **$105** still armed on last print; **~$34–$40** short depending on cash — not close to trigger then.
- Edge model still **cut_neg_edge** / negative EV on last equity print — 15% risk sizing.
- healthz **503** @19:48 after last **ok** @19:20 — monitor flake, and now a **~138 min** telemetry blackout.
- Prefer equity-line closed (**417**) over state-file resume (**~512**).
- **Primary alert:** agent IDLE after autoquant digression; **no runner confirmation after 19:53**. Blackout length makes last-known PnL increasingly unreliable. Wake DO OR DIE or poll `state_live.json` / `runner_live.log` before trusting any live mark.

---

## How the bot is working

**What's working**
- Through 19:53 the runner was still **LIVE** and not floor-halted after the 18:00 peak giveback.
- Risk stack (last print) holding: floor **$20** + trail, cash_target **$105**, cut_neg_edge 15%.
- Lifetime closed book still **417 @ 86% / +$49.16** on last confirmed equity line.

**What's not / risks**
- **Telemetry blackout ~138 min (~2.3 h)** — cannot confirm whether the bot is still trading, flat, or halted after BTC 1600 and later windows.
- Session still in drawdown from **~$99** HW → **~$76** last mark (**−$23** from peak); post-settle mark unknown.
- Day equity **−$17** vs 10:00 baseline (last mark); formal AUG05 calendar still **−$55** (stale).
- Agent left bot ops for autoquant @19:54; rely on runner/keep-alive, but this cron **could not re-verify** the process for a second consecutive hour.
- healthz flaky (503) — off-box alerts still the gap if the pod stalls.

**Bottom line:** Last-known book is **LIVE at ~$76 mark** with closed **417 @86% / +$49**. Confirmed hourly since 19:20 was **2W–1L / −$4.19**; the **19:48–22:06 window is a data gap**. Day equity still red (**−$17** vs $93.75) on the last mark. **Wake the live agent / re-poll runner logs** before acting on these numbers as current.
