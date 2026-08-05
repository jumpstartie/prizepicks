# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~14:03 UTC (automation cron)  
**Data freshness:** **STALE ~41 min** — newest confirmed dump **13:22:22 UTC** (`health.json` cash **$65.46**, open **2**, `halted=False`, high_water **$87.65**). Last closed-book print **13:21:50** (`closed=378`, win% **88**, pnl **+$63.99**). No equity/settle dumps after **13:22:22**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** (last message **13:22:39**; metadata touch ~**13:28**).  
**Source:** `state_live.json` / `health.json` / `runner_live.log` via DO OR DIE transcript pull @14:01.  
**Bot status (last confirmed):** **LIVE / not halted**, cash **~$65.46** with **2 opens** (mark ~**$87.90**), favorite-maker TP printer + heartbeat watchdog + keep-alive + external_monitor. Risk: **halt_floor=$48**, session HW **$87.65**, soft BN strict on, early-tip **off**. Core book **BNB / XRP / BTC only**.

---

## Headline

| Metric | Value |
|---|---|
| **Cash (latest confirmed)** | **$65.46** (open **2**, **halted=False**) @13:22:22 |
| **Last flat equity** | **$87.65** @13:21:50 (before 0930 window fills) |
| **Mark equity (approx)** | **~$87.90** (cash $65.46 + pv ~$22.44) @13:22 |
| **Session HW** | **$87.65** (up from **$81.43** prior report) |
| **Prior report flat (PR #23 / 13:00)** | **$81.20** @12:02 (was STALE) |
| **Δ vs prior report (last flat)** | **+$6.45** (**$81.20 → $87.65**) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **−$6.10** at last flat (**$87.65**); ~**−$5.85** at last mark |
| **Day equity vs halt-log start ($61.54)** | **+$26.11** (last flat) |
| **AUG05 calendar closed book** | **n=30 / −$29.43** @13:22 (**refreshed**; was n=23/−$43.80) |
| **Lifetime closed (last confirmed @13:21:50)** | **378 closes · 88% · +$63.99** |
| **Hourly 12:00–13:00** | cash **+$6.45** (**$81.20 → $87.65**); closed **376→378**; closed PnL **+$6.50** — then ~**65m VM freeze** |
| **Hourly 13:00–14:00** | wake @13:21 → **2 LIVE fills** (cash **$87.65 → $65.46**); mark still ~**$87.90**; **0930 settle unconfirmed** after 13:22 |
| **vs prior hourly report (PR #23)** | visibility restored briefly; flat peak **+$6.45**; closed book **+2 / +$6.50**; AUG05 improved **~$14** |

Bot **reprinted +$6.45** after the prior STALE gap (two ~0.73 TP favorites), then **froze ~12:16–13:21**, woke into a **BTC+XRP 0930** ticket, and went quiet again with opens still live. Lifetime closed **378 / 88% / +$64**. Treat post-13:22 as **STALE** — 0930 settle outcome unknown.

---

## Total win / loss

### Day session (closed / equity)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~17:38 (prior formal since-10:00) | **107–18** | **+$45.91** | stale (not refreshed) |
| AUG05 calendar @11:05 | **15–6** | **−$44.52** | high (was fresh then) |
| AUG05 @11:09 | **n=23** | **−$43.80** | medium (partial) |
| AUG05 @13:22 | **n=30** (W–L not broken out) | **−$29.43** | **high** (refreshed) |
| Equity path @12:02 | — | **−$12.55** vs $93.75 | high (then) |
| Equity path last flat @13:21 | — | **−$6.10** vs $93.75 | **high** |
| **Equity path @14:03 (this cron)** | — | **−$6.10** flat / ~**−$5.85** mark | **stale** (~41m; settle pending) |

Prefer marked/flat equity for day P&L when fresh. Closed-book day slice improved: AUG05 **−$43.80 → −$29.43** (**+$14.37**) as the two TP closes printed.

### Today since midnight (context)

- Prior formal midnight tally **177–24 / +$104.86** (@17:38) — still not refreshed as a midnight rollup.
- Lifetime closed path: **348** (freeze resume) → **369** (post-nuke) → **376** (@12:02) → **378** (@12:15 / 13:21), closed PnL **+$63.99**.

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
| Prior report 12:02 | **376** | **88** | **+$57.49** | **$81.20** flat **LIVE** |
| Rebound print 12:15 | **378** | **88** | **+$63.99** | **$87.65** flat **LIVE** |
| Wake + fills 13:21–13:22 | **378** | **88** | **+$63.99** | cash **$65.46** / open **2** / mark ~**$87.90** |
| **This cron 14:03** | **378*** | **88*** | **+$63.99*** | **$65.46*** cash / open2 (**STALE**) |

\*same last confirmed dump; 0930 window settle not observed after 13:22.

Path: 10:00 baseline **$93.75** → ATH **$193.22** → early-tip low **$73.37** → freeze resume **$118–$124** → nuke hour **$72** → rebound **$81 → $88** → freeze → wake with risk on.

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
| **12:00–13:00** | closed **+2** (376→378) | cash **+$6.45** (**$81.20 → $87.65**); closed PnL **+$6.50**; then **~65m freeze** | BTC/XRP TP ~+$3.27 / +$3.22 |
| **13:00–14:00** | **0 closed confirmed** | cash **−$22.19** into inventory (**$87.65 → $65.46**); mark ~flat; **settle TBD** | wake + BTC/XRP 0930 fills @13:21 |

### 12:00–13:00 path (reconstructed this report)

- **12:02:20:** flat **$81.20** / open **0** / closed **376 / 88% / +$57.49** (prior STALE baseline)
- **~12:12–12:15:** two TP favorites print — inferred **BTC yes@0.73 +$3.27**, **XRP yes@0.73 +$3.22** → flat **$87.65**, closed **378 / 88% / +$63.99**, HW still **$81.43** on early HB then later reanchored
- **~12:16 → 13:21:** **VM / runner freeze** — watchdog heartbeat stale **~3953s**; cash stuck **$87.65** flat; no fills

### 13:00–14:00 path (this report)

- **13:21:50:** wake confirm — still flat **$87.65** / closed **378 / +$63.99**
- **13:21:52:** health briefly **down** (`watchdog_heartbeat_stale_3953s`) while cash still **87.647** in blob
- **13:21:53–58:** **LIVE fills** — BTC YES **13.60 @0.82**, XRP YES **13.44 @0.84** on `…0930-30` → cash **$65.46**, open **2**, mark ~**$87.90**
- **13:22:22:** health **ok** again; HW **$87.647**; halt_floor **$48**; runner/watchdog/keep_alive up
- **13:22:39 → 14:03:** agent **IDLE**; **no further** cash, settle, fill, or health dumps (0930 window should have settled ~13:30 — **unobserved**)

**Net this hour vs prior report last flat ($81.20):** confirmed rebound to **$87.65** (**+$6.45**), then inventory open at last contact. Closed-book PnL **+$57.49 → +$63.99** (**+$6.50**). Post-13:22 settle **unknown**.

**Day pace (through last confirmed flat):** equity **−$6.10** vs 10:00 baseline ($93.75 → $87.65). Lifetime closed **~$64** net with **88%** WR across **378** closes. AUG05 calendar still red but improved to **−$29.43**.

---

## How the bot is working

**What's working**
- Strategy edge still shows when live: **+$6.45 / +2 closes / +$6.50** closed PnL in the brief 12:02–12:15 window on core favorites.
- Core trim to **BNB/XRP/BTC** continues to print (those two TPs were BTC+XRP).
- After the freeze, ops stack recovered: health **ok**, HB fresh, watchdog + keep-alive up @13:22; still above **$48** halt floor.
- AUG05 closed book healed **~$14** off the nuke lows (**−$43.80 → −$29.43**).
- Session HW reanchored to **$87.65** — trail protection tighter than the $81 era.

**What's not / risks**
- **Recurring visibility / freeze pattern:** traded ~10–15 min after 12:02, froze ~65 min, woke, then agent went IDLE again with **opens live** and **~41 min** without dumps. Same class as overnight WD freeze.
- **0930 settle unknown** — last contact left **~$22** cash in BTC+XRP inventory; PnL of that ticket not confirmed.
- Day equity still **red vs 10:00 baseline** (~**−$6**); AUG05 still **−$29**.
- External alerts still **unarmed** (webhook unset) — freeze/open-risk events won't page.
- Halt floor **$48** with ~26% Kelly leaves room for another concentrated loser if unsupervised.

**Bottom line:** Bot is **LIVE and still edge-positive on the closed book** (**378 @88% / +$64**, last flat **$87.65**), but ops reliability is the constraint — **freeze → brief trade → IDLE with risk on**. This hour’s confirmed story is **+$6.45 rebound then inventory entry**; treat **13:00–14:00 settle as STALE / unconfirmed**. Needs a DO OR DIE nudge (or fresh `state_live` / settle dump) before the next cron.

---

## Proof lines (from DO OR DIE transcript)

```
[12:02:20] equity=$81.20 cash=$81.20 open=0 closed=376 win%=88 pnl=+57.4932
[12:15:27] equity=$87.65 cash=$87.65 open=0 closed=378 win%=88 pnl=+63.9913
[13:21:50] equity=$87.65 cash=$87.65 open=0 closed=378 win%=88 pnl=+63.9913
[13:21:53] LIVE order bid 13.60 @ 0.8200 on KXBTC15M-26AUG050930-30
[13:21:58] LIVE FILL YES 13.44 @ ~0.84 on KXXRP15M-26AUG050930-30 ... cash=$65.46
AUG05 pnl -29.43 n 30
"ts": "2026-08-05T13:22:22Z", "status": "ok", "cash": 65.4554, "high_water": 87.647, "halted": false
HALT_FLOOR=48
```
