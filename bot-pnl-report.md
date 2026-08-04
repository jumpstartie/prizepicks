# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~17:00 UTC  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`state_live.json` closed trades)  
**Bot status (last confirmed):** Running — runner + journal monitor in tmux; `halted=False`; flat after Pyth restart

---

## Headline

| Metric | Value |
|---|---|
| **Day session (since 10:00 UTC)** | **97–15** (+$58.22) |
| **Win rate (day)** | **86.6%** |
| **Equity (latest)** | **~$140** |
| **Post risk-bump (since 15:30)** | **23–2** (+$16.11, ~$13/hr) |
| **Lifetime closed PnL** | **~$121–128** (from ~$20 start) |

Bot is working: high win rate, positive day PnL, healthy after the 15:30 Kelly/stack-cap bump. Equity climbed from ~$94 at the 10:00 baseline to ~$140 by 17:00.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

- **Wins:** 97  
- **Losses:** 15  
- **Record:** 97–15  
- **Net PnL:** **+$58.22**  
- Snapshot time: **16:43 UTC** (most complete W/L pull)

### Post risk-bump window (since 15:30 UTC)

- **23–2**, **+$16.11** (~**+$13.19/hr**)  
- Clean stretch after Kelly → 0.40 and stack-cap 1.5×

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity |
|---|---|---|---|---|
| ~15:30 UTC | 201 | 90% | +$120.86 | $137.47 |
| ~15:43 UTC | 204 | 90% | +$127.78 | ~$137–144 |
| ~17:00 UTC (Pyth restart) | — | — | — | **~$140.07** |

Original live start ~$20 → overnight ~$67 → 10:00 baseline ~$94 → current ~$140.

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only (excludes open MTM). Hours after 13:40 partly reconstructed from cumulative snapshots.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured (best hour) |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | PnL reconstructed; first 40m was 13–3 +$8.32 |
| 14–15 | uncertain split | ≈+$6.3 (to 14:52) | then into 15:00 drawdown |
| 15:00–15:30 | 5–2 | −$17.46 | ETH −$16.96 / BNB −$11.54 hits |
| 15:30–16:43 | 23–2 | +$16.11 | measured block after bump |
| 16:43–17:00 | — | — | equity only (~$131 → ~$140); no new W/L pull |

**Through 13:40 (measured):** 49–10, +$35.99 — avg win ≈ +$1.54, avg loss ≈ −$3.93

---

## How the bot is working

**What's working**
- Near-expiry favorite maker on 15m crypto (BNB / SOL / XRP core + satellites) stays +EV on the day.
- Multi-venue lead (Binance + OKX/Kraken/Pyth) filtering bad entries.
- Series governor cutting SOL (demoted / cold) after morning bleed; ETH/BNB/XRP carried the book earlier.
- Post-15:30 risk bump: strong 23–2 stretch, no fresh journal alerts in that window.
- Trailing halt floor (70% of high-water) + spike TP / peak-fade locking gains.

**Watch items**
- Loss size still larger than avg win (~2–3× when it hits) — bankroll swings on single big tickets.
- SOL was the weak series (day: 4–5, −$17 earlier); keep demoted.
- Midday equity mark spikes (~$185) were open-position accounting noise; trust closed PnL + cash.
- This automation cannot read live `state_live.json` directly (gitignored on another agent VM); figures lag the last DO OR DIE transcript pull.

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
