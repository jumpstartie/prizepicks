# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~19:01 UTC  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** Trading runner **alive** after 19:00 redeploy (Cursor agent IDLE). `halted=False`, floor **$95**, bankroll **$137.74**, risk ~**18.9%** edge Kelly, unit **$27.99**. Soft iced; SOL/NEAR dropped; BTC→core; hot×1.3.

---

## Headline

| Metric | Value |
|---|---|
| **Flat cash / bankroll (19:00)** | **$137.74** (open 0) |
| **Day equity PnL (vs ~$94 @ 10:00)** | **≈ +$44** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) |
| **Day closed book (est. @19:00)** | **≈ 126–24** (~+$70) — reconstructed |
| **Lifetime closed (last equity line 18:15)** | **249 closes · 89% · +$123.60** |
| **Last hour (18:00–19:00 est.)** | **≈ +$28** on ≥20 closes |
| **vs prior hourly report (~18:03)** | Equity **$112 → $138**; lifetime closed PnL **+$118 → +$124** |

Strong recovery hour after the 17:43 trailing halt. Bot is flat, profitable on the day, and was just redeployed with tighter series selection (drop SOL/NEAR, ice soft).

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** |
| ~17:46 after 1345 settles | **110–20** | **≈ +$41.49** | high (named closes) |
| ~18:15 after post-halt batch | **~118–22** | **≈ +$50** | medium |
| **~19:00 (reconstructed)** | **≈ 126–24** | **≈ +$70** | low–medium |

No fresh `since 10:00` tool rollup after 17:38; post-17:38 figures chain equity `closed`/`pnl` deltas + flat-to-flat cash.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| Halt flat 17:46 | 239 | 88 | +$115.35 | **$108.28** |
| Prior report 18:02 | 245 | 89 | +$118.13 | **$112.26** (4 open) |
| **Metals restart 18:15** | **249** | **89** | **+$123.60** | **$117.66** flat |
| setup_gov restart 18:28 | — | — | — | **$130.23** flat |
| **Latest 19:00** | — | — | — | **$137.74** flat |

Path: ~$20 start → overnight ~$67 → 10:00 baseline ~$94 → session HW **$151.45** → halt re-anchor **$108.28** → **$137.74** now.

12h slice @18:55: **165 closes · 87.3% WR · +$81.52** (XRP 24–3 +$33.1; SOL still weak 16–8 −$19.6).

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only (excludes open MTM). Hours after 13:40 partly reconstructed.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured (best early hour) |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | reconstructed |
| 14–15 | uncertain split | ≈+$6.3 (to 14:52) | then into 15:00 drawdown |
| 15:00–15:30 | 5–2 | −$17.46 | ETH/BNB hits |
| 15:30–16:43 | 23–2 | +$16.11 | post Kelly/stack bump |
| 16:43–17:00 | — | — | equity climb to ~$140 |
| 17:00–17:30 | 10–3 | **−$12.31** | HOT_TICKET cluster |
| 17:30–18:00 | ~4–2 + halt | ≈−$4 to −$8 | trailing halt 17:43; flat $108.28 |
| **18:00–19:00** | **~18–2 (est.)** | **≈ +$28** | recovery: $112→$138; ≥20 closes |

**Day pace:** equity ~+$4.9/hr since 10:00 ($94 → $138 over ~9h). Closed-book pace higher (~+$7–8/hr est.) because some closes were open before the 10:00 baseline.

**18:00 hour breakdown (est.):**
- 17:48–18:15: +10 closes, **+$8.25** lifetime closed PnL
- 18:15–18:27: cash **$117.66 → $130.23** (**+$12.57**)
- 18:28–19:00: cash **$130.23 → $137.74** (**+$7.51**)

---

## How the bot is working

**What's working**
- Clear recovery after the 17:43 trailing halt: **+$29.5** cash from halt flat ($108.28) to now ($137.74) in ~75 minutes.
- Safety stack did its job (halt → Kelly 0.33 → floor $95 → HW re-anchor) then let edge resume.
- Lifetime closed book still ~**89%** win rate and **+$123.60** realized (last equity line).
- Series read still sane: XRP carrying 12h book; SOL weak → dropped again on 19:00 redeploy.
- No new `HOT_TICKET_LOSS` / `BIG_LOSS` after the 17:30 cluster.

**What changed this hour**
- Metals satellites enabled (~18:15); small positive in 12h (GOLD 2–0 +$1.4, SILVER 1–0 +$0.3).
- `setup_gov` live @18:28 (soft iced, mid/rich hot).
- 19:00 redeploy: ice soft, drop SOL/NEAR, BTC→core, hot press ×1.3, ~19% risk/trade.

**Watch items**
- Day formal W–L still stuck at 17:38 (**107–18**); trust cash/equity for the recovery story until next rollup.
- Loss asymmetry remains: one bad basket can still erase an hour (see 17:30).
- Cursor agent is **IDLE** while runner keeps going in tmux — monitoring depends on someone (or next cron) re-attaching to that VM.
- This automation cannot read live `state_live.json` on the trading VM; figures lag the last DO OR DIE transcript pull (~19:00:51).

---

## Methodology

```text
rows = closed trades in state_live.json with close_ts in window
wins   = pnl > 0
losses = pnl < 0
pnl    = sum(pnl)   # flats (pnl==0) excluded from W–L
equity = Kalshi cash + open 15m exposure (separate from closed PnL)
```

Post-17:38 estimates use flat-to-flat cash deltas and equity `closed`/`pnl` log lines when a full window rollup was not re-run.

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR on e72b / ~18:03):** cash/equity **$112 → $138**; lifetime closed **245 / +$118 → 249 / +$124**; day formal W–L unchanged at **107–18 +$45.91** (no new rollup); recovery hour **≈ +$28** documented; 19:00 redeploy noted.
