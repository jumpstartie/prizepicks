# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~09:06 UTC (automation cron)  
**Data freshness:** **LIVE** — newest equity print **09:04:53 UTC**; Kalshi API cash **117.9915** @ **09:05:00Z**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) is **RUNNING** again (last message ~09:02:24; tools through ~09:05).  
**Source:** `runner_live.log` / watchdog HB / Kalshi balance via DO OR DIE transcript pull @09:05.  
**Bot status:** **LIVE / not halted**, flat **$117.99**, open **0**. Favorite-maker + heartbeat watchdog + keep-alive restarted ~09:04 after a **~7h watchdog freeze (02:11→09:02)**. Risk: **halt_floor=$60 + trail 0.65×HW** (HW **$123.1533**), risk **15%** (`cut_neg_edge`), ticket-cost cap **~22%**, early-tip **off**.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (latest)** | **$117.99** (open **0**, **halted=False**) @09:04:53 |
| **Session ATH (overnight flat peak)** | **$123.15** @02:00 (session HW **$123.1533**) |
| **Prior all-time session ATH** | **$193.22** @22:50–22:51 |
| **Prior report flat (PR #18 / 08:00)** | **$123.15** (stale @02:00) |
| **Δ vs prior report flat** | **−$5.16** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$24.24** |
| **Day equity vs halt-log start ($61.54)** | **+$56.45** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (09:04)** | **348 closes · 88% · +$93.43** |
| **Δ closed since 02:00** | **+5 closes · closed PnL −$5.14** |
| **Hourly 08:00–09:00** | **frozen** (inside 02:11–09:02 WD freeze) — no new fills observed |
| **Hourly 09:00–09:05 (partial)** | resume + settle → flat **$117.99**; closed **348** |
| **vs prior hourly report (PR #18)** | **fresh book**; gap explained (freeze, not silent trading) |

Bot is **back online** after the freeze. Flat equity is **~$118** (down **~$5** from the $123 restart peak). Lifetime closed still **~$93** net at **88%** WR across **348** closes. Stack hardened with keep-alive + timeout-proof watchdog + IOC fallback at resume.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale — not refreshed) |
| Equity path @00:53 halt | — | **−$20.38** vs $93.75 | high (flat cash $73.37) |
| Equity path @02:00 | — | **+$29.40** vs $93.75 | high |
| **Equity path @09:04 (latest)** | — | **+$24.24** vs $93.75 | **high** (flat cash $117.99) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.
- Overnight → morning closed tally: **326 → 348** (+22 closes since 23:47 prior); lifetime closed PnL **+$98.75 → +$93.43**.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| ETH settle / prior 23:02 | **315** | **89** | **+$106.19** | **$104.68** flat |
| Prior report 23:47 | **326** | **88** | **+$98.75** | **$97.75** flat **LIVE** |
| Overnight bounce 00:16 | **331** | **88** | **+$101.78** | **$101.34** flat |
| Early-tip halt 00:53 | **335** | **88** | **+$95.98** | **$73.37** **HALTED** |
| Resume after tip settle 01:15 | **335** | **88** | **+$95.98** | **$118.96** flat |
| Pre-freeze 01:29 | **340** | **88** | **+$98.34** | **$111.95** flat |
| Post-freeze flat 01:56 | **340** | **88** | **+$98.34** | **$122.92** flat |
| Restart flat 02:00 | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| Pre-WD-freeze 02:11 | *(open)* | — | — | cash **$112.41** open **2** |
| **WD freeze 02:11–09:02** | — | — | — | **no HB** (~7h) |
| Resume settle 09:02–09:04 | — | — | — | **$112.41** open2 → **$117.99** flat |
| **Latest confirmed 09:04:53** | **348** | **88** | **+$93.43** | **$117.99** flat **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193.22** → ETH nuke **$104.68** → early-tip halt **$73.37** → tip settle / grind **$123.15** → brief trade then **WD freeze** → resume flat **$117.99**.

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
| **02:00–03:00** | closed **+5** overall by 09:04 (343→348); freeze @02:11 | flat **$123 → $112** cash w/ open2; then dark | traded ~11 min then WD freeze |
| **03:00–04:00** | **frozen** | **no new HB** | watchdog stuck on hung API |
| **04:00–05:00** | **frozen** | **no new HB** | — |
| **05:00–06:00** | **frozen** | **no new HB** | — |
| **06:00–07:00** | **frozen** | **no new HB** | — |
| **07:00–08:00** | **frozen** | **no new HB** | — |
| **08:00–09:00** | **frozen** | **no new HB** | still inside freeze |
| **09:00–09:05** | settle + restart | flat **$112.41** open2 → **$117.99**; closed **348 · +$93.43** | user nudge; stack hardened |

### 02:00–09:05 path (this report)

- **02:00:14–02:00:36:** :00 settle → flat **$123.15**, closed **343 · 88% · +$98.56**; favorite-maker + heartbeat WD restart
- **02:09–02:11:** live inventory — cash **$103.48** open **4** → **$112.41** open **2**; HW **$123.1533**
- **02:11:40 → 09:02:26:** **watchdog freeze** (~7h) — no heartbeats; open inventory held through freeze
- **09:02:** user: “Run system and keep it going…”; agent resumes
- **09:02:26–09:02:37:** HB returns — cash **$112.41** open **2** → **$117.99** open **0** (positions settled)
- **09:04:07–09:04:53:** runner restart; equity **$117.99 · closed=348 · 88% · pnl=+93.4259**; keep-alive + timeout-proof WD + IOC fallback deployed
- **09:05:** Kalshi API confirms cash **117.9915**, open `[]`, paused **False**; tmux `kalshi-live` / `kalshi-watchdog` / `kalshi-keepalive` / `kalshi-observer` up; scanning (e.g. DOGE/BTC “too cheap”)

**Net since last confirmed flat ($123.15 @02:00):** equity **−$5.16**; closed book **+5** trades for **−$5.14** closed PnL (those closes net losers; WR still rounds to 88%).

**Day pace (through latest):** equity ~+$1.1/hr since 10:00 ($93.75 → $117.99 over ~23h). Lifetime closed **~$93** net with **88%** WR across **348** closes.

---

## How the bot is working

**What's working**
- Overnight recovery from **$73 → $123** was real; post-freeze resume left the book flat at **~$118** with **no floor halt**.
- Risk stack still on: floor **$60** + trail **0.65×HW**, early-tip **OFF**, ticket ~**22%**, cut_neg_edge.
- After the freeze, agent hardened the ops stack: **keep-alive**, timeout-proof watchdog, IOC fallback — intended so IDLE agent ≠ dead runner.
- Win rate holding **~88%** on the lifetime closed book.

**What's not / risks**
- **~7h blind spot** from watchdog freeze on hung API — prior hourly crons correctly flagged “unobserved,” not zero PnL.
- Closed PnL slipped **+$98.56 → +$93.43** across the 5 closes since 02:00 (**−$5**).
- Formal day W–L rollups still stuck at **17:38** (107–18 / +$45.91); use equity path for day P&L.
- Fresh runner just restarted @09:04 — scanning but **no new fills yet** in the 09:04–09:05 window; next hour will show whether the keep-alive fix holds.

**Bottom line:** Bot is **LIVE again at ~$118 flat**, lifetime **348–@88% / +$93**, day equity **+$24** vs 10:00 baseline. Last hour was mostly **frozen**, not actively winning/losing; the **−$5** vs $123 is from the brief 02:09–02:11 window + settle of those open legs.
