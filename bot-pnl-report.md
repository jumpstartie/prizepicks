# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~04:07 UTC (automation cron)  
**Data freshness:** Newest live book on trading VM still **02:00:36 UTC** — **no new equity/closed prints after ~02:00:40**. Agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) remains **IDLE** (~2h since last tool activity @02:00:51).  
**Source:** `runner_live.log` / Kalshi balance via DO OR DIE transcript (last tool end **02:00:40Z**)  
**Bot status (last confirmed):** **LIVE / not halted**, flat **$123.15**, open **0**. Favorite-maker + heartbeat watchdog restarted @02:00:35 with **halt_floor=$60 + trail 0.65×HW** (effective ~$61.58), risk **15%** (`cut_neg_edge`), ticket-cost cap **~22%**, early-tip **off**. Intended to keep trading after agent IDLE — **unconfirmed** for 02:01–04:07.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (last confirmed)** | **$123.15** (open **0**, **halted=False**) @02:00 |
| **Session ATH (still)** | **$193.22** @22:50–22:51 |
| **Prior report flat (PR #13 / 03:00)** | **$123.15** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$29.40** (unchanged vs last report) |
| **Day equity vs halt-log start ($61.54)** | **+$61.61** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (02:00)** | **343 closes · 88% · +$98.56** |
| **Hourly 02:00–03:00 (observed)** | **no new transcript data** — flat/closed **unknown** |
| **Hourly 03:00–04:00 (observed)** | **no new transcript data** — flat/closed **unknown** |
| **vs prior hourly report (PR #13)** | **unchanged last-known book**; +1h of **unobserved** runtime (now **~2h** gap) |

Last confirmed book is unchanged from the 02:00 report. Overnight recovery to **~$123** still stands; lifetime closed PnL remains ~**+$99** at **88%** WR. This hour’s report is a **stale-data hold** — DO OR DIE has not printed since the watchdog restart (~2h ago).

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale) |
| Equity path @23:47 | — | **+$4.00** vs $93.75 | high (prior) |
| Equity path @00:53 halt | — | **−$20.38** vs $93.75 | high (flat cash $73.37) |
| **Equity path @02:00 (still latest)** | — | **+$29.40** vs $93.75 | **high** (flat cash); **no refresh @03:00 or @04:00** |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.
- Overnight closed tally through last print: **326 → 343** (+17 closes); lifetime closed PnL **+$98.75 → +$98.56**.

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
| **Latest confirmed 02:00** | **343** | **88** | **+$98.56** | **$123.15** flat **LIVE** |
| **03:00 cron pull** | *no new print* | — | — | **unknown** (agent IDLE) |
| **04:00 cron pull** | *no new print* | — | — | **unknown** (agent IDLE ~2h) |

Path: 10:00 baseline **$93.75** → ATH **$193.22** → ETH nuke **$104.68** → :45 scratches **$97.75** → early-tip halt **$73.37** → tip settle resume **$118.96** → grind/freeze/settle **$123.15** → **??? after 02:00** (now ~2h dark).

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
| **02:00–03:00** | **unobserved** | **unknown** | last print @02:00:36; agent IDLE |
| **03:00–04:00** | **unobserved** | **unknown** | still no transcript after 02:00:40 |

### 02:00–04:00 path (this report)

- **02:00:14–02:00:30:** :00 settle — cash **$106.81 → $123.15**, open **3 → 0** FLAT
- **02:00:35–36:** restart favorite-maker + heartbeat watchdog; equity line **closed=343 · 88% · +$98.56**
- **02:00:40–02:00:51:** last tool/log activity; agent final: “Back up at ~$123, scanning”
- **02:01–04:07:** **no transcript evidence** of fills, closes, freezes, or halts (~**2h** dark). Tmux runner + watchdog were left running at restart, but this automation VM cannot see live files.

**Day pace (through last confirm):** equity ~+$1.7/hr since 10:00 ($93.75 → $123.15 over ~16h). Lifetime closed still **~$99** net with **88% WR** across **343** closes.

---

## How the bot is working

**What's working (as of last confirm @02:00)**
- Overnight recovery from **$73 → $123** held through the 02:00 settle/restart.
- Anti-nuke stack still the plan: ticket-cost cap (**22%**), floor **$60+trail**, early-tip **off**, risk ~**15%**.
- Heartbeat + stale-kill watchdog (**≥90s**) deployed after the **01:30–01:56** stuck-alive freeze.

**What hurt / watch**
- **Data gap now ~2h:** agent IDLE since **02:00:51** with no live VM access from this cron — cannot say if the bot printed, froze, or halted after 02:00.
- Early-tip **FORCE** on the shared account remains the overnight villain (drain under **$78** floor).
- Watchdog deployed but **not yet observed** firing a real stale-kill in production.
- Lifetime closed PnL still capped near **+$99** (ETH **−$88.54** @23:00 dominates).
- Formal day/midnight W–L still frozen since **17:38**.

**What changed since prior hourly report (03:00 / PR #13)**
- **Nothing measurable** in last-known book (still **$123.15 / 343 / +$98.56 / 88%**).
- Data gap extended from ~1h → **~2h** of unobserved runtime; treat 02–04 hourly W–L as **unknown**, not flat zero.

**Watch items**
- Wake DO OR DIE (or pull `state_live.json` / Kalshi balance) to refresh post-02:00 path — **critical**, now two consecutive stale hourly reports.
- Confirm heartbeat watchdog kills stale runners if another freeze hits.
- Keep early-tip **off** (or separate bankroll) while floor is tight.
- Re-run formal `since 10:00` / midnight W–L rollup when interactive.

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

**04:00 caveat:** this report’s freshest primary source ends at **02:00:40Z**. Numbers above that are carried forward and labeled. Two consecutive hourly crons (03:00 and 04:00) saw no new live prints.
