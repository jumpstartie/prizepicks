# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~10:05 UTC (automation cron)  
**Data freshness:** **LIVE (slightly lagged)** — newest cash/health print **09:57:56 UTC** (`cash=120.0216`, `status=ok`); last DO OR DIE tool activity **09:58:22Z**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **IDLE** after external-monitor work; runner / keep-alive / watchdog were still up at last check.  
**Source:** `health.json` / WD HB / Kalshi balance via DO OR DIE transcript pull @10:04.  
**Bot status:** **LIVE / not halted**, flat **~$120.02**, open **0**. Favorite-maker + heartbeat watchdog + keep-alive + external_monitor. Risk: **halt_floor=$60 + trail 0.65×HW** (HW **$123.5837**), risk **15%** (`cut_neg_edge`), ticket-cost cap **~22%**, early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (latest)** | **$120.02** (open **0**, **halted=False**) @09:57:56 |
| **Session ATH (this window)** | **$123.58** cash @09:17–09:27 (HW **$123.5837**) |
| **Prior all-time session ATH** | **$193.22** @22:50–22:51 |
| **Prior report flat (PR #19 / 09:00)** | **$117.99** @09:04 |
| **Δ vs prior report flat** | **+$2.03** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$26.27** |
| **Day equity vs halt-log start ($61.54)** | **+$58.48** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (last equity print 09:04)** | **348 closes · 88% · +$93.43** — **not refreshed after 09:05** |
| **Hourly 09:00–10:00** | cash **$117.99 → $120.02** (**+$2.03**); mid-hour peak **$123.58** then **−$3.56** giveback |
| **vs prior hourly report (PR #19)** | **trading resumed**; keep-alive self-healed a ~10m WD stall @09:27 |

Bot is **alive and scanning** after the overnight freeze. Flat equity **~$120** (**+$2** vs last hour’s **$118**). Lifetime closed print still **348 / 88% / +$93** (stale — cash moved while flat, so some fills likely settled without a new equity rollup line).

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale — not refreshed) |
| Equity path @00:53 halt | — | **−$20.38** vs $93.75 | high (flat cash $73.37) |
| Equity path @02:00 | — | **+$29.40** vs $93.75 | high |
| Equity path @09:04 | — | **+$24.24** vs $93.75 | high |
| **Equity path @09:57 (latest)** | — | **+$26.27** vs $93.75 | **high** (flat cash $120.02) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity for day P&L; lifetime closed line is also stale since 09:04.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.
- Overnight → morning closed tally: **326 → 348** (+22 closes since 23:47 prior) through 09:04; post-09:05 closes not yet reprinted.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| ETH settle / prior 23:02 | **315** | **89** | **+$106.19** | **$104.68** flat |
| Prior report 23:47 | **326** | **88** | **+$98.75** | **$97.75** flat **LIVE** |
| Overnight bounce 00:16 | **331** | **88** | **+$101.78** | **$101.34** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Resume after tip settle 01:15 | **335** | **88** | **+$95.98** | **$118.96** flat |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Pre-WD-freeze 02:11 | *(open)* | — | — | cash **$112.41** open **2** |
| **WD freeze 02:11–09:02** | — | — | — | **no HB** (~7h) |
| Resume settle 09:02–09:04 | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |
| Mid-hour peak 09:17–09:27 | *(no new equity print)* | — | — | cash **$123.58** / HW **$123.5837** |
| **Latest confirmed 09:57:56** | **348*** | **88*** | **+$93.43*** | **$120.02** flat **LIVE** |

\*Lifetime closed/win%/pnl last printed @09:04:53 — cash moved +$2 while remaining flat/open=0, so closed book likely understated until next equity rollup.

Path: 10:00 baseline **$93.75** → ATH **$193.22** → ETH nuke **$104.68** → early-tip halt **$73.37** → tip settle / grind **$123.15** → WD freeze → resume **$117.99** → grind **$123.58** → latest **$120.02**.

---

## Hourly win / loss (2026-08-04 → 08-05 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. **No formal `by hour` dump after 19:43** — late hours from equity/cash prints and settle lines.

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
| **09:00–10:00** | cash path (closed print stale) | **+$2.03** net flat (**$117.99 → $120.02**); peak **$123.58** | LIVE again; WD self-heal @09:27 |

### 09:00–10:00 path (this report)

- **09:02–09:04:** resume after ~7h freeze; settle open2 → flat **$117.99**; closed print **348 · 88% · +$93.43**; keep-alive + timeout WD + IOC fallback deployed
- **09:04–09:17:** trading resumes; cash climbs to **$123.58** flat (open **0**); HW → **$123.5837**
- **09:17–09:27:** ~**581s** watchdog stall; keep_alive respawns WD @09:27:08; runner HB stayed fresh (~1s)
- **09:27–09:57:** cash retraces to **$120.02** while remaining flat / not halted
- **09:56–09:58:** external_monitor + health.json / `:9105/healthz` added; health **ok** @09:57:56; webhook/ping **not configured** yet
- **09:58 → 10:05:** agent **IDLE**; no new status poll in transcript (~7 min lag)

**Net this hour vs prior report ($117.99):** equity **+$2.03**. Mid-hour peak was **+$5.59** before a **~$3.56** giveback.

**Day pace (through latest):** equity ~+$1.1/hr since 10:00 ($93.75 → $120.02 over ~24h). Lifetime closed last print **~$93** net with **88%** WR across **348** closes (understated if post-09:05 settles occurred).

---

## How the bot is working

**What's working**
- Post-freeze stack is doing its job: bot stayed **LIVE**, keep-alive **respawned a stalled watchdog** (~10m) without human intervention.
- Flat equity recovered from freeze resume **$118 → $124 peak → $120** — still above the $60 floor / trail.
- Risk stack unchanged and healthy: floor **$60** + trail **0.65×HW**, early-tip **OFF**, ticket ~**22%**, cut_neg_edge.
- External monitor landed (`health.json` + local healthz); next step is wiring a webhook/ping URL outside the pod.

**What's not / risks**
- Agent is **IDLE** again — OK if keep-alive holds, but last confirmed health is **~7 min** before this cron (09:58).
- Lifetime closed / formal day W–L rollups are **stale** (09:04 / 17:38); cash moved without a new `closed=` equity line.
- Brief WD stall @09:17–09:27 shows the hang class of bugs isn’t fully gone — keep-alive mitigated it.
- External alerts not yet armed (`ping_configured=False`) — pod sleep would still be invisible off-box.

**Bottom line:** Bot is **LIVE at ~$120 flat** (**+$2** this hour; day equity **+$26** vs 10:00 baseline). Lifetime print still **348 @88% / +$93**. Ops hardening (keep-alive) proved out mid-hour; watch the next print for a refreshed closed-book rollup.
