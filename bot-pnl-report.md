# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~18:12 UTC (automation cron)  
**Data freshness:** **FRESH ~6 min** — newest confirmed dump **18:06:00 UTC** (`equity=$99.12`, `cash=$99.12`, open **0**, `closed=404`, win% **88**, pnl **+$74.85**). Live balance **$99.1154** @18:05:59 (`halted=False`). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last tools **~18:06:28**; last bot log **18:06:02**).  
**Source:** `runner_live.log` / healthz via DO OR DIE transcript pull @18:12.  
**Bot status (last confirmed):** **LIVE / not halted**, mark **~$99.12**, open **0** (flat), **RTP-20 printer replay** on core **BNB / XRP / BTC**. Risk: **halt_floor=$20**, trail **0.65×HW**, risk sizing **24% edge_kelly**. Lognormal gate **OFF**. Early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$99.12** (live **$99.1154**, **halted=False**) @18:05–18:06 |
| **Mark equity** | **$99.12** @18:06:00 |
| **Prior report (PR #27 / 17:00)** | mark **$90.65** / cash **$90.65** open1 / closed **402 / +$66.39** (FRESH @17:38) |
| **Δ vs prior report mark** | **+$8.47** (**$90.65 → $99.12**) |
| **Δ closed PnL vs prior** | **+$8.47** (**+$66.39 → +$74.85**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$5.37** at last mark (**$99.12**) |
| **Day equity vs halt-log start ($61.54)** | **+$37.58** (last mark) |
| **AUG05 calendar closed book** | last formal **n=39 / 77% / −$54.72** @14:34 (**not refreshed**; lifetime +2 closes since prior cron, both green settles) |
| **Lifetime closed (confirmed @18:06:00)** | **404 closes · 88% · +$74.85** |
| **Hourly 16:00–17:00** | mark **$79.90 → $86.26** (**+$6.36**); closed **398→401**; closed PnL **+$55.51→+$62.20** (**+$6.69**); **3–0** |
| **Hourly 17:00–18:00** | mark **$86.26 → $99.12** (**+$12.86**); closed **401→404**; closed PnL **+$62.20→+$74.85** (**+$12.65**); printer-replay **3W–0L** (+scratch $0) |
| **vs prior hourly report (PR #27)** | recovery continued; flat **~$99.12**; closed book **+$8.47**; day equity now **green** vs 10:00 baseline |

Bot kept recovering: **~$90 → ~$99** since the 17:00 cron. Lifetime closed **+$74.85 @88%** across **404** closes — new session high for closed PnL since the midday nuke. Day equity flipped green vs the 10:00 baseline (**+$5.37**). Treat as **FRESH**.

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
| Equity path @17:00 (prior cron) | — | **−$3.10** vs $93.75 ($90.65) | high |
| **Equity path @18:12 (this cron)** | — | **+$5.37** mark ($99.12) | **high / fresh** |

Prefer marked equity for day P&L. Day equity improved **+$8.47** vs the 17:00 cron mark and is now **above** the 10:00 baseline. AUG05 formal day-book still shows **−$54.72** (stale @14:34); do not invent a new calendar total without a recompute. Implied improvement from +2 lifetime closes since prior cron (BTC/BNB 1400 settles) is not yet formalized.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38 prior-day formal) — still not refreshed as a midnight rollup.
- Lifetime closed path: **402** (@17:38) → **404** (@18:06), closed PnL **+$74.85**.

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
| Prior report @17:38:40 | **402** | **88** | **+$66.39** | **$90.65** open1 **LIVE** |
| **Latest @18:06:00 (this cron)** | **404** | **88** | **+$74.85** | **$99.12** flat **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193** → nuke/rebound **$72→$88** → peak **~$92** → settle bleed **~$57** → recover **~$80 → ~$90 → ~$99**.

Note: state-file resume counter can show **closed≈498** after restarts — that is a **different ledger**. Prefer continuous equity-line `closed` series (**402→404**). Also ignore stray AUG04 / `closed≈200` equity lines and mid-settle blip `equity=$109.99` (reconciled to **$99.12**).

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
| **17:00–18:00** | closed **+3** resolved (401→404) **3W–0L** (+$0 scratch) | mark **$86.26 → $99.12** (**+$12.86**); closed PnL **+$62.20 → +$74.85** (**+$12.65**) | printer-replay cutover + two 1400 settles |

### 17:00–18:00 path (this report)

- **16:40–17:32:** mark held **$86.26** / closed **401 / +$62.20** (lognormal fill starvation ~35m)
- **17:38:26:** FULL ENGINE RESTART — **RTP-20 printer replay**: `LOGNORMAL_GATE=0`, `HALT_FLOOR=20`, `CONFIRM_POLLS=1`, `MIN_SECS_LEFT=25`
- **17:38:40:** TAKE PROFIT BNB 1345 YES **+$4.19** → cash/eq **$90.65** / closed **402 / +$66.39** / open **1** / win% **88**
- **17:39:17:** health ok cash **90.6496**; agent briefly IDLE
- **~17:45:** BTC 1345 YES scratch **+$0.00** (empty exit; not counted as a real L)
- **17:50:58:** LIVE FILL BTC 1400 YES @0.71 → cash **~$79.77** open inventory
- **18:05:46:** LIVE FILL BNB 1400 YES @0.73 → cash **$99.12** (post prior settle path)
- **18:05:52:** SETTLE BTC 1400 YES **+$4.44** / SETTLE BNB 1400 YES **+$4.02** → equity **$99.12** / closed **404 / +$74.85** / open **0**
- **18:05:59:** live balance **$99.1154**; resume `halted=False`; cfg still lognormal OFF / floor $20
- **18:06:00:** same equity line confirmed; resting BTC 1415 NO @0.73 (`fill=0.0`)

**Net 17–18:** mark **+$12.86**; closed PnL **+$12.65**; printer-replay resolved **3W–0L** (BNB TP + BTC/BNB settles; excludes $0 scratch).

**Day pace (through last confirmed mark):** equity **+$5.37** vs 10:00 baseline ($93.75 → $99.12). Lifetime closed **~$74.85** net with **88%** WR across **404** closes. AUG05 formal calendar still **−$54.72** (stale).

---

## How the bot is working

**What's working**
- **Third recovery leg:** book climbed **~$90 → ~$99** since the prior cron; lifetime closed PnL **+$74.85** (best since midday nuke).
- Printer-replay stack (**floor $20**, lognormal **OFF**, confirm=1, min_left=25) is printing: **3W–0L / +$12.65** since 17:38 cutover.
- Clean settle hour on 1400 window: BTC **+$4.44** + BNB **+$4.02**.
- Core still **BNB/XRP/BTC only**; edge_kelly **24%**.
- Day equity flipped **green** vs 10:00 baseline (**+$5.37**).

**What's not / risks**
- **HALT_FLOOR still $20** — wide drawdown room vs earlier $42/$50 floors; trail 0.65×HW only soft-protects.
- Agent **IDLE** again after 18:06 while runner was healthy — VM/agent gaps remain a theme (runner can keep trading while Cursor agent sleeps).
- AUG05 formal day-book still **−$54.72** last compute; needs refresh.
- Dual closed counters (equity-line **404** vs state-file **~498**) — always prefer equity-line series.
- Mid-settle equity blip (**$109.99**) during BTC settle — ignore; cash reconciled to **$99.12**.
- External alerts still **unarmed** (webhook unset).
- Resting BTC 1415 NO @0.73 unfilled at last print — next window not yet realized.

**Bottom line:** Bot is **LIVE and recovering hard**. Last confirmed book: **404 @88% / +$74.85**, mark **~$99.12**, floor **$20**. The 17:00 hour was a strong **up hour** (**+$12.86** mark / **+$12.65** closed / printer-replay **3W–0L**). Day equity **+$5** vs 10:00 baseline / **+$38** vs halt-log start. Needs a fresh AUG05 calendar recompute.

---

## Proof lines (from DO OR DIE transcript)

```
[17:38:26] === FULL ENGINE RESTART ===
HALT_FLOOR=20  LOGNORMAL_GATE=0  CONFIRM_POLLS=1  MIN_SECS_LEFT=25
[17:38:40] TAKE PROFIT KXBNB15M-26AUG051345-45 YES entry=0.70 mark=0.99 exit~0.99 pnl=+4.1874 cash=$90.65
[17:38:40] equity=$90.65 cash=$90.65 open=1 closed=402 win%=88 pnl=+66.3867  unit=23.39  risk=24.0%(edge_kelly)
health ok cash 90.6496 issues []
[17:50:58] LIVE FILL YES … @ ~0.71 on KXBTC15M-26AUG051400-00  cash~$79.77
[18:05:46] LIVE FILL YES 14.90 @ ~0.73 on KXBNB15M-26AUG051400-00 status=executed cash=$99.12
[18:05:52] SETTLE KXBTC15M-26AUG051400-00 YES WIN pnl=+4.4428 cash=$99.12
[18:05:52] SETTLE KXBNB15M-26AUG051400-00 YES WIN pnl=+4.0230 cash=$99.12
[18:05:52] equity=$99.12 cash=$99.12 open=0 closed=404 win%=88 pnl=+74.8525
[18:05:59] live balance cash=$99.1154 (equity~$99.1154)  halted=False
[18:06:00] equity=$99.12 cash=$99.12 open=0 closed=404 win%=88 pnl=+74.8525
[18:06:02] LIVE order ask 16.29 @ 0.2700 on KXBTC15M-26AUG051415-15 fill=0.0
printer replay since 17:38:33 — closed 3 · WR=100% (3W-0L) · pnl=$+12.65  (excludes $0 scratch)
26AUG05: n=39 wr=77% pnl=-54.72 tp=+20.12 fade=+4.67 settle=-79.52   # last formal @14:34
```
