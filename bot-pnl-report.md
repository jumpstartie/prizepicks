# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~12:02 UTC (automation cron)  
**Data freshness:** **LIVE / FRESH** — newest cash/equity print **12:02:20 UTC** (`cash=$81.20`, `open=0`, `halted=False`, filled closes **376**, closed PnL **+$57.49**). Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last tools ~12:02) while the tmux runner stays **LIVE**.  
**Source:** `state_live.json` / `health.json` / `runner_live.log` via DO OR DIE transcript pull @12:02–12:04.  
**Bot status:** **LIVE / not halted**, flat **~$81.20**, open **0**. Favorite-maker TP printer + heartbeat watchdog + keep-alive + external_monitor. Risk: **halt_floor=$48**, session HW **$81.43**, soft BN strict on, early-tip **off**. Core book locked to **BNB / XRP / BTC only** (satellites dropped @12:01).

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (latest)** | **$81.20** (open **0**, **halted=False**) @12:02:20 |
| **Session HW** | **$81.43** (unchanged; still below abandoned lifetime peak **$123.58**) |
| **Prior report flat (PR #21 / 11:00)** | **$72.12** @11:05 |
| **Δ vs prior report flat** | **+$9.08** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$12.55** |
| **Day equity vs halt-log start ($61.54)** | **+$19.66** |
| **AUG05 calendar closed book** | **n=23 / −$43.80** @11:09 (partial); formal 15–6/−$44.52 @11:05 — **not fully refreshed @12:02** |
| **Lifetime closed (fresh @12:02)** | **376 closes · 88% · +$57.49** |
| **Hourly 11:00–12:00** | cash **$72.12 → $81.20** (**+$9.08**); closed **369 → 376** (**+$8.59** closed PnL) |
| **vs prior hourly report (PR #21)** | rebound after the **−$48** nuke hour |

Bot **stabilized and ground back ~$9** this hour after the morning ETH/BTC/SOL bleed. Lifetime closed book improved to **376 / 88% / +$57**. Ops stack healthy; agent IDLE but runner LIVE watching the 0815 window (mids still too cheap / coin-flip for the ≥70¢ filter).

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @11:05 | **15–6** | **−$44.52** | high (was fresh then) |
| AUG05 @11:09 | **n=23** (W–L not broken out) | **−$43.80** | medium (partial print) |
| Equity path @11:05 | — | **−$21.63** vs $93.75 | high (prior) |
| **Equity path @12:02 (latest)** | — | **−$12.55** vs $93.75 | **high** (flat cash $81.20) |

Prefer marked/flat equity for day P&L. AUG05 formal rollup was not re-run at 12:02; use lifetime closed delta (**+$8.59** on **+7** closes) for this hour’s realized book.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — still not refreshed as a midnight rollup.
- Lifetime closed path: **348** (freeze resume) → **369** (post-nuke) → **376** (+7 this hour), closed PnL **+$48.90 → +$57.49**.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Resume settle 09:02–09:04 | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |
| Prior report 09:57 | **348*** | **88*** | **+$93.43*** | **$120.02** flat **LIVE** |
| Post ETH/BTC nuke 10:17 | **359** | **88** | **+$56.59** | **$81.62** flat |
| Post SOL nuke 10:51 | **367** | **87** | **+$48.17** | **$71.42** flat |
| Prior report 11:05 | **369** | **~87** | **+$48.90** | **$72.12** flat **LIVE** |
| Working 11:09 (opens) | **369*** | — | — | cash **~$63–67** (not flat) |
| **Latest confirmed 12:02:20** | **376** | **88** | **+$57.49** | **$81.20** flat **LIVE** |

\*mid-hour working cash with open inventory; flat baseline remains the 11:05 / 12:02 prints.

Path: 10:00 baseline **$93.75** → ATH **$193.22** → early-tip low **$73.37** → freeze resume **$118–$124** → nuke hour **$72** → **this hour rebound → $81**.

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
| **11:00–12:00** | closed **+7** (369→376) | cash **+$9.08** (**$72.12 → $81.20**); closed PnL **+$8.59** | hot-streak rebound; core trim |

### 11:00–12:00 path (this report)

- **11:05:** flat **$72.12**; closed **369 / ~87% / +$48.90**; AUG05 **15–6 / −$44.52**; HW **$81.43**; halt_floor was **$50**
- **11:06:** hot-streak / TP-printer restart — bankroll **$72.12**, **halt_floor → $48**, TP **97¢** / soft spike **95¢**, bn=flat at **half size**, core BNB/XRP/BTC + DOGE/ETH satellites, **no SOL**
- **11:07–11:09:** 0715 fills — ETH YES 3.51@0.82, XRP YES 7.90@0.73, BNB YES 4.02@0.93; working cash **~$60–67**; AUG05 **n=23 / −$43.80**; health **ok**
- **11:10–12:00:** agent quiet; runner continued (transcript gap). By resume, cash back to **~$81** with inventory
- **12:00:42:** runner resume — state equity **$90.21** / cash **$81.20** open **2**; settles **ETH 0730 NO WIN +$1.23**, **BNB 0730 NO WIN +$2.22** → flat **$81.20**; closed **376 / 88% / +$57.49**
- **12:01:** user/agent locked **BNB/XRP/BTC only** (dropped DOGE/ETH satellites); Kelly ~24%; health **ok** (`runner_hb_age_s≈1.1`)
- **12:02:** still flat **$81.20** / open **0**; watching 0815 mids (all &lt;0.70 / coin-flip — no new tickets yet)

**Net this hour vs prior report ($72.12):** equity **+$9.08**. Closed-book PnL **+$48.90 → +$57.49**.

**Day pace (through latest):** equity **−$12.55** vs 10:00 baseline ($93.75 → $81.20). Lifetime closed **~$57** net with **88%** WR across **376** closes.

---

## How the bot is working

**What's working**
- **Rebound hour** after the nuke: flat equity **+$9** and closed PnL **+$8.59** with **+7** fills settled.
- Stack stayed alive: runner + watchdog + keep-alive + external_monitor healthy @12:01–12:02.
- Strategy focus tightened to the best book slice: **BNB/XRP/BTC only (~+$125 @ ~91% WR** in series analysis) — ETH/SOL demoted after fat-tail settles.
- TP-printer config live (97¢ TP / 95¢ soft spike / spike-fade ON); soft BN strict still on.
- Still **above** **$48** halt floor; not halted. HW **$81.43** nearly tags current cash — trail protection tight again.

**What's not / risks**
- Day equity still **−$12.55** vs the 10:00 baseline; AUG05 calendar still deeply red (~**−$44** last formal).
- Agent is **IDLE** again — runner keep-alive must carry the next windows (same failure mode as the overnight freeze if HB/API hangs).
- External alerts still **unarmed** (`ping_configured=False` / webhook unset).
- 0815 window currently all coin-flip mids — idle grind until ≥70¢ favorites appear.
- Halt floor **$48** and ~24% Kelly size leave room for another concentrated loser if a core ticket rides to a bad settle.

**Bottom line:** Bot is **LIVE at ~$81 flat** after a **+$9** recovery hour (**day equity −$13** vs 10:00 baseline). Lifetime closed now **376 @88% / +$57**. Book trimmed to **BNB/XRP/BTC**; watch whether the TP printer compounds from here without another settle nuke.
