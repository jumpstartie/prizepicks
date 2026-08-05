# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~11:05 UTC (automation cron)  
**Data freshness:** **LIVE / FRESH** — newest cash/state print **11:05:33 UTC** (`cash=72.1206`, `halted=False`, filled closes **369**, closed PnL **+$48.9**). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **RUNNING**.  
**Source:** `state_live.json` / `health.json` / runner equity lines via DO OR DIE transcript pull @11:05.  
**Bot status:** **LIVE / not halted**, flat **~$72.12**, open **0**. Favorite-maker + heartbeat watchdog + keep-alive + external_monitor. Risk: **halt_floor=$50** (trail reanchored; session HW **$81.43**), soft BN flat-block on, early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (latest)** | **$72.12** (open **0**, **halted=False**) @11:05:33 |
| **Session HW (reanchored)** | **$81.43** (lifetime peak HW **$123.58** abandoned after morning bleed) |
| **Prior report flat (PR #20 / 10:00)** | **$120.02** @09:57 |
| **Δ vs prior report flat** | **−$47.90** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$21.63** |
| **Day equity vs halt-log start ($61.54)** | **+$10.58** |
| **AUG05 calendar closed book** | **15–6** (71% WR) **−$44.52** @11:05 |
| **Lifetime closed (fresh @11:05)** | **369 closes · ~87% · +$48.90** |
| **Hourly 10:00–11:00** | cash **$120.02 → $72.12** (**−$47.90**); nukes ETH/BTC −$38.76 + SOL −$10.21 |
| **vs prior hourly report (PR #20)** | sharp reversal from +$2 grind into **−$48** hour |

Bot took a **hard drawdown this hour**. Flat equity fell from **~$120 → ~$72** on large ETH/BTC/SOL losers after the overnight freeze recovery. Lifetime closed book finally refreshed: **369 / ~87% / +$49** (was stale **348 / 88% / +$93**). Still **LIVE** and above the new **$50** floor.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| **AUG05 calendar @11:05** | **15–6** | **−$44.52** | **high** (fresh python rollup) |
| Equity path @09:57 | — | **+$26.27** vs $93.75 | high (prior) |
| **Equity path @11:05 (latest)** | — | **−$21.63** vs $93.75 | **high** (flat cash $72.12) |

Prefer marked/flat equity for day P&L. The AUG05 ticker-day rollup (**15–6 / −$44.52**) captures the morning nuke window; the older “since 10:00 formal” 107–18 line is still stale.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — not refreshed as a midnight rollup.
- Lifetime closed path overnight→morning: **326 → 348** (freeze resume) → **369** (+21 closes since 09:04), with closed PnL **+$93.43 → +$48.90**.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| ETH settle / prior 23:02 | **315** | **89** | **+$106.19** | **$104.68** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Resume settle 09:02–09:04 | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |
| Prior report 09:57 | **348*** | **88*** | **+$93.43*** | **$120.02** flat **LIVE** |
| Post ETH/BTC nuke 10:17 | **359** | **88** | **+$56.59** | **$81.62** flat |
| Post SOL nuke 10:51 | **367** | **87** | **+$48.17** | **$71.42** flat |
| **Latest confirmed 11:05:33** | **369** | **~87** | **+$48.90** | **$72.12** flat **LIVE** |

\*prior lifetime print was stale through 09:04; now refreshed after morning fills/settles.

Path: 10:00 baseline **$93.75** → ATH **$193.22** → early-tip low **$73.37** → freeze resume **$118–$124** → prior hour **$120** → **morning nukes → $72**.

---

## Hourly win / loss (2026-08-04 → 08-05 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. Late hours from equity/cash prints and settle lines.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | reconstructed |
| 14–15 | uncertain split | ≈+$6.3 (to 14:52) | then into 15:00 drawdown |
| 15:00–15:30 | 5–2 | −$17.46 | ETH/BNB hits |
| 15:30–16:43 | 23–2 | +$16.11 | post Kelly/stack bump |
| 16:00–17:00 | n=15 | **+$10.95** | diagnostic 100% WR |
| 17:00–18:00 | n=18 | **−$16.73** | HOT_TICKET / soft bleed |
| 18:00–19:00 | n=24 | **+$25.38** | diagnostic 100% WR |
| 19:00–20:00 | n=17 partial → giveback | closed ≈+$10 then equity giveback | prior |
| 20:00–21:00 | no full bucket | near-floor scare → ratchet | prior |
| 21:00–22:00 | no full bucket | → flat **$134.88** | prior |
| 22:00–23:00 | no full bucket | flat **$135 → $105**; peak **$193**; ETH **−$88.54** | prior |
| 23:00–00:00 | ≈7–4 post-restart | flat **$105 → $98**; closed **+$106 → +$99** | prior report |
| **00:00–01:00** | closed **+9** (326→335) | closed **−$2.76**; flat **$98 → $73** | early-tip halt |
| **01:00–02:00** | closed **+8** (335→343) | closed **+$2.58**; flat **$73 → $123** | tip settle + grind |
| **02:00–03:00** | closed **+5** by 09:04 (343→348); freeze @02:11 | flat **$123 → $112** cash w/ open2; then dark | traded ~11 min then WD freeze |
| **03:00–08:00** | **frozen** | **no new HB** | watchdog stuck on hung API |
| **08:00–09:00** | **frozen** | **no new HB** | still inside freeze |
| **09:00–10:00** | cash path | **+$2.03** (**$117.99 → $120.02**); peak **$123.58** | LIVE again; WD self-heal |
| **10:00–11:00** | closed **+21** (348→369); AUG05 slice heavy L | cash **−$47.90** (**$120.02 → $72.12**) | ETH/BTC/SOL nukes |

### 10:00–11:00 path (this report)

- **09:57 → 10:02:** still near **$120**; BNB NO fill starts size back up
- **10:08–10:17:** large ETH YES + BTC NO fills; settles **ETH −$18.00**, **BTC −$20.76** → cash **$81.62**; closed **359 / 88% / +$56.59**
- **10:18–10:29:** health blip / stack restart; OG #3 restore; HW **reanchored** to ~**$80.72–$81.43**; halt floor cut toward **$55** then **$50**
- **10:51:** SOL YES settle **−$10.21** → cash **$71.42**; closed **367 / 87% / +$48.17**; then BNB+XRP fills to cash **$65.10** (open)
- **10:52–10:53:** morning-sprint restart (`halt_floor=$50`, soft BN strict); health **ok**
- **11:05:** BNB/XRP `:00` settles small wins; flat **$72.12**; filled closes **369**; closed PnL **+$48.9**; AUG05 **15–6 / −$44.52**; bnflat_block skipping soft `:15` signals

**Net this hour vs prior report ($120.02):** equity **−$47.90**. Closed-book PnL dropped roughly **$93 → $49** as the stale print caught up to realized losses.

**Day pace (through latest):** equity **−$21.63** vs 10:00 baseline ($93.75 → $72.12). Lifetime closed **~$49** net with **~87%** WR across **369** closes.

---

## How the bot is working

**What's working**
- Stack stayed **alive through the bleed**: runner + watchdog + keep-alive + external_monitor healthy @11:05 (`runner_hb_age_s≈2.5`, health **ok**).
- Lifetime closed / day calendar rollups **refreshed** (no longer stuck at the 09:04 / 17:38 stale prints).
- Soft BN flat-block is active post-sprint — skipping flat soft `:15` entries after the nuke hour.
- Still **above** the lowered **$50** halt floor; not halted.

**What's not / risks**
- **Worst hour since the overnight tip halt:** **−$48** flat equity in one hour on concentrated crypto favorites (ETH/BTC/SOL).
- HW trail effectively **reset** ($123 → $81) after reanchor — less protection vs the prior peak.
- Halt floor cut **$60 → $50** increases room to keep trading into further drawdowns.
- External alerts still **unarmed** (`ping_configured=False`) — off-box visibility still missing.
- Agent spent ~12m in strategy Q&A around `:00` settle (ops gap), though tools re-read live state @11:05.

**Bottom line:** Bot is **LIVE at ~$72 flat** after a **−$48** hour (**day equity −$22** vs 10:00 baseline). Lifetime closed now **369 @~87% / +$49**. Ops stack healthy; the trading book is the problem this hour — watch the next cycle under the tighter soft-BN / $50-floor sprint config.
