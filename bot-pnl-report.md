# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~02:04 UTC (automation cron)  
**Data freshness:** Newest live book on trading VM ~**02:00:36 UTC** (flat cash after :00 settle + runner restart); agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) last tool activity **~02:00:40 UTC**, status **IDLE** @02:04  
**Source:** `runner_live.log` / `state_live.json` / Kalshi balance via DO OR DIE transcript  
**Bot status (last confirmed):** **LIVE / not halted**, flat **$123.15**, open **0**. Favorite-maker restarted @02:00:35 with **halt_floor=$60 + trail 0.65×HW**, risk **15%** (`cut_neg_edge`), ticket-cost cap **~22%**, early-tip **off**. Heartbeat + stale-kill watchdog deployed after a **01:30–01:56** freeze. Scanning post-restart; no transcript proof after 02:00:40.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (02:00)** | **$123.15** (open **0**, **halted=False**) |
| **Session ATH (still)** | **$193.22** @22:50–22:51 |
| **Prior report flat (23:47)** | **$97.75** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$29.40** |
| **Day equity vs halt-log start ($61.54)** | **+$61.61** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (02:00)** | **343 closes · 88% · +$98.56** |
| **Last ~2h path (23:47 → 02:00)** | Flat **$97.75 → $123.15** (**+$25.40**); dipped to **$73.37** halt @00:53 |
| **vs prior hourly report (PR #11 / 5022 / ~00:02)** | Flat **$98 → $123**; lifetime **326 / +$99 → 343 / +$99**; day equity **+$4 → +$29** |

Strong recovery hour-plus after the overnight early-tip halt. Book is back above **$120**, day equity vs 10:00 is **+$29**, and lifetime closed PnL is essentially flat vs the 23:47 mark (**+$98.75 → +$98.56**) while cash healed from the shared-account drain.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale) |
| Equity path @23:47 | — | **+$4.00** vs $93.75 | high (prior) |
| Equity path @00:53 halt | — | **−$20.38** vs $93.75 | high (flat cash $73.37) |
| **Equity path @02:00** | — | **+$29.40** vs $93.75 | **high** (flat cash) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.
- Overnight closed tally (runner): **326 → 343** (+17 closes); lifetime closed PnL **+$98.75 → +$98.56**.

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
| **Latest 02:00** | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193.22** → ETH nuke **$104.68** → :45 scratches **$97.75** → early-tip halt **$73.37** → tip settle resume **$118.96** → grind/freeze/settle **$123.15**.

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

### 00:00 hour path (this report)

- 23:46 restart overnight sprint @ **$97.75** (`HALT_FLOOR=$78`, risk min 18%, ticket cap 0.28)
- 00:16:50: flat **$101.34** / closed **331 · +$101.78** (favorites grinding)
- ~00:30: BNB settle hit (~**−$7.18**) → book ~**$102** then soft
- 00:47: early-tip **FORCE** fills (BTC NO / BNB YES / NEAR) drained ~**$28–29** cash from the shared account
- **00:53:32: HALT** — equity **$73.37** ≤ floor **$78**; closed **335 · +$95.98**; runner stopped/paused
- Hour: flat **−$24.38**; closed PnL **−$2.76**; halt caused by early-tip cash yank, not a favorite-maker nuke

### 01:00 hour path (this report)

- 01:15:51: early-tip positions paid → cash **$118.96**; resume with **HALT_FLOOR=$60**, ticket cap **0.22**, early-tip **off**, risk ~15%
- 01:20–01:29: favorites filled (DOGE/BNB/XRP/BTC); XRP TP **+$0.925**; closed **335→340**, pnl **+$95.98→+$98.34**, flat **$111.95**
- **01:30–01:56: runner freeze** (~26m stuck-alive, missed a 15m window); by 01:56 flat **$122.92** / closed still **340**
- 01:56–02:00: rich YES fills (XRP/BNB ~98–99¢) then :00 settle → **$123.15** / closed **343 · +$98.56**
- 02:00:35: restart with heartbeat watchdog; HW **$122.92**, floor **$60 + trail**
- Hour: flat **+$49.78** (mostly tip-settle recovery **$73→$119**); closed PnL **+$2.58**

**Day pace:** equity ~+$1.8/hr since 10:00 ($93.75 → $123.15 over ~16h). Lifetime closed still **~$99** net with **88% WR** across **343** closes — far below the **+$195** peak before the ETH nuke, but cash has rebuilt from the **$73** overnight low.

---

## How the bot is working

**What's working**
- Overnight recovery from **$73 → $123** without another ETH-sized nuke.
- Anti-nuke stack holding: ticket-cost cap (**22%**), lower floor (**$60**), early-tip **disabled** after the drain, risk pinned ~**15%**.
- Mid/rich favorite grind + TP still prints (XRP **+$0.925** @01:28; closed book +5 in ~10m after resume).
- Ops response to freeze: heartbeat file + stale-kill watchdog (≥90s) deployed @02:00 restart.

**What hurt / watch**
- Early-tip **FORCE** on the shared Kalshi account remains the overnight villain: pulled the book under the **$78** floor while favorite-maker was flat.
- **01:30–01:56 freeze** missed a full window — process looked alive; watchdog is the fix, not yet battle-tested across multiple hours.
- Lifetime closed PnL still capped near **+$99** (ETH **−$88.54** @23:00 dominates); cash recovery ≠ closed-book repair.
- Formal day/midnight W–L still frozen since **17:38**.
- **No transcript proof after 02:00:40** — agent IDLE; tmux may still be trading.

**What changed since prior hourly report (00:02 / PR #11)**
- Flat **$97.75 → $123.15**; lifetime closed **326 → 343**; closed PnL still ~**+$99**; win% **88**.
- Day equity vs 10:00 **+$4 → +$29**.
- Hit overnight halt @**$73.37**, then resumed with floor **$78→$60**, early-tip off, heartbeat watchdog on.
- Note: the **01:00** automation cron pod failed immediately (`ERROR` / empty transcript); this **02:00** run covers both hours.

**Watch items**
- Confirm heartbeat watchdog actually kills stale runners on the next freeze.
- Keep early-tip **off** (or on a separate bankroll) while floor is tight.
- Re-run formal `since 10:00` / midnight W–L rollup when DO OR DIE is interactive.
- Trust flat cash + closed counters over open MTM when rich YES tickets are on.

---

## Methodology

```text
rows = closed trades in state_live.json with close_ts in window
wins   = pnl > 0
losses = pnl < 0
pnl    = sum(pnl)   # flats (pnl==0) excluded from W–L
equity = Kalshi cash + open 15m exposure (separate from closed PnL)
```

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR #11 / ~00:02):** flat **$98 → $123**; day equity **+$4 → +$29**; lifetime closed **326 → 343** (PnL still ~+$99); overnight early-tip halt + resume + freeze fix documented.
