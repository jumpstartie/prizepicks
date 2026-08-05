# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~13:03 UTC (automation cron)  
**Data freshness:** **STALE ~61 min** — newest cash/equity print still **12:02:20 UTC** (`cash=$81.20`, `open=0`, `halted=False`, filled closes **376**, closed PnL **+$57.49**). No runner / health / settle dumps after **12:02:29**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) remains **IDLE** (last message activity **12:02:34**; metadata `updatedAt` **12:55** with no new tool prints).  
**Source:** `state_live.json` / `health.json` / `runner_live.log` via DO OR DIE transcript pull @13:04 (same last prints as the 12:00 report).  
**Bot status (last confirmed):** **LIVE / not halted**, flat **~$81.20**, open **0**. Favorite-maker TP printer + heartbeat watchdog + keep-alive + external_monitor. Risk: **halt_floor=$48**, session HW **$81.43**, soft BN strict on, early-tip **off**. Core book **BNB / XRP / BTC only**.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (latest confirmed)** | **$81.20** (open **0**, **halted=False**) @12:02:20 |
| **Session HW** | **$81.43** (unchanged; still below abandoned lifetime peak **$123.58**) |
| **Prior report flat (PR #22 / 12:00)** | **$81.20** @12:02 |
| **Δ vs prior report flat** | **$0.00** (no newer flat print) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$12.55** (unchanged vs last confirmed) |
| **Day equity vs halt-log start ($61.54)** | **+$19.66** |
| **AUG05 calendar closed book** | **n=23 / −$43.80** @11:09 (partial); formal 15–6/−$44.52 @11:05 — **still not refreshed** |
| **Lifetime closed (last confirmed @12:02)** | **376 closes · 88% · +$57.49** |
| **Hourly 12:00–13:00** | **unconfirmed / STALE** — last known flat **$81.20**; closed book unchanged at last dump; **no fills** after 12:01 core lock while watching coin-flip 0815 mids |
| **vs prior hourly report (PR #22)** | no measurable change in confirmed metrics |

Bot **idle-flat at last contact** after the prior hour’s **+$9** rebound. Lifetime closed book still **376 / 88% / +$57**. Cannot confirm whether the runner kept trading 0815→0900 windows — agent went quiet and no new HB/equity dumps reached the transcript.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @11:05 | **15–6** | **−$44.52** | high (was fresh then) |
| AUG05 @11:09 | **n=23** (W–L not broken out) | **−$43.80** | medium (partial print) |
| Equity path @12:02 | — | **−$12.55** vs $93.75 | **high** (flat cash $81.20) |
| **Equity path @13:03 (this cron)** | — | **−$12.55** vs $93.75 | **stale** (same last print) |

Prefer marked/flat equity for day P&L when fresh. This hour has **no new closed-book delta** in the transcript.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — still not refreshed as a midnight rollup.
- Lifetime closed path: **348** (freeze resume) → **369** (post-nuke) → **376** (@12:02), closed PnL **+$57.49** — **unchanged in this report window**.

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
| **Last confirmed 12:02:20** | **376** | **88** | **+$57.49** | **$81.20** flat **LIVE** |
| **This cron 13:03** | **376*** | **88*** | **+$57.49*** | **$81.20*** (**STALE**) |

\*same last confirmed dump; not re-verified after 12:02.

Path: 10:00 baseline **$93.75** → ATH **$193.22** → early-tip low **$73.37** → freeze resume **$118–$124** → nuke hour **$72** → rebound **$81** → **no confirmed move this hour**.

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
| **12:00–13:00** | **unconfirmed** | **$0 known** at last dump (**$81.20** flat); **no post-12:02 prints** | agent IDLE; 0815 watched as coin-flip then silence |

### 12:00–13:00 path (this report)

- **12:00:42:** runner resume — equity **$90.21** / cash **$81.20** open **2**; settles **ETH 0730 NO WIN +$1.23**, **BNB 0730 NO WIN +$2.22** → flat **$81.20**; closed **376 / 88% / +$57.49**
- **12:01:** satellites cleared — **BNB/XRP/BTC only**; Kelly ~24%; health **ok** (`runner_hb_age_s≈1.1`)
- **12:01–12:02:** watching **0815** BNB/XRP/BTC — all mids **&lt;0.70 / coin-flip**; **no fills**
- **12:02:20:** last equity print — still flat **$81.20** / open **0** / closed **376**
- **12:02:34 → 13:03:** agent **IDLE**; **no further** cash, settle, fill, or health dumps in transcript (metadata touch @12:55 without new tool output)

**Net this hour vs prior report ($81.20):** confirmed equity **$0.00** (STALE). Closed-book PnL unchanged at last contact (**+$57.49**).

**Day pace (through last confirmed):** equity **−$12.55** vs 10:00 baseline ($93.75 → $81.20). Lifetime closed **~$57** net with **88%** WR across **376** closes.

---

## How the bot is working

**What's working (as of last contact)**
- Prior hour’s rebound held on the books: flat **$81.20**, closed **+$57.49**, win rate back to **88%**.
- Book already trimmed to the historically best slice: **BNB/XRP/BTC only (~+$125 @ ~91% WR** in series analysis).
- At 12:01–12:02 the ops stack was healthy: runner + watchdog + keep-alive + external_monitor; HB ages fresh (~1–8s).
- Still above **$48** halt floor; not halted. HW **$81.43** nearly tags cash — trail protection tight.

**What's not / risks**
- **Visibility gap:** ~**61 minutes** with no new runner dumps — same failure mode class as the overnight freeze (agent IDLE while we cannot prove HB continuity).
- Day equity still **−$12.55** vs the 10:00 baseline; AUG05 calendar still deeply red (~**−$44** last formal).
- External alerts still **unarmed** (`ping_configured=False` / webhook unset).
- 0815 window was all coin-flip at last look — idle grind expected until ≥70¢ favorites, but later windows (0830/0845/0900) are **unverified**.
- Halt floor **$48** and ~24% Kelly size leave room for another concentrated loser if a core ticket rides to a bad settle while unsupervised.

**Bottom line:** Last confirmed state is **LIVE at ~$81 flat** with lifetime closed **376 @88% / +$57**. This hourly cron finds **no new PnL movement in the transcript** — treat **12:00–13:00 as STALE / unconfirmed**, not as a proven flat hour. Needs a DO OR DIE nudge (or fresh `state_live` / `health.json` dump) before the next cron to restore live visibility.
