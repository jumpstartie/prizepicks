# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~18:03 UTC  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** Running — `halted=False` after 17:43 trailing-floor halt and 17:48 restart (Kelly 0.33, floor $95)

---

## Headline

| Metric | Value |
|---|---|
| **Day session (since 10:00 UTC, measured ~17:30)** | **107–18** (+$45.91) |
| **Win rate (day @ 17:30)** | **85.6%** |
| **Equity (latest 18:02)** | **$112.26** (cash $98.13, 4 open) |
| **Lifetime closed book (18:02)** | **245 closes · 89% win · +$118.13** |
| **vs prior hourly report (~17:00)** | Day PnL **−$12.3**; equity **~$140 → $112** |

Bot is still net profitable on the day and lifetime, but the last hour was a real drawdown: hot-ticket cluster → trailing halt → smaller risk restart. Safety systems worked; edge still printing post-restart.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Notes |
|---|---|---|---|
| ~15:58 (prior report) | **97–15** | **+$58.22** | peak day closed book |
| **~17:30 (latest full rollup)** | **107–18** | **+$45.91** | after 17:30 NEAR/SOL/DOGE hits |
| ~18:02 (estimated) | **~114–21** | **~+$44** | +4 closes into halt (2W/2L) then +6 post-restart (~+$2.78 closed) |

No fresh full `since 10:00` rollup after 17:30; 18:02 estimate uses lifetime closed deltas from log lines.

### Today since midnight (~17:30)

- **177–24**, **+$104.86**

### Post risk-bump / late windows

| Window | W–L | PnL | Rate |
|---|---|---|---|
| Since 15:30 bump → ~15:58 | 23–2 | +$16.11 | ~+$13.19/hr |
| Since Pyth restart 17:00 → ~17:30 | 10–3 | **−$12.31** | drawdown |
| Since 17:15 → halt | 5–3 | **−$20.69** | hot tickets |
| Halt settles 17:43–17:46 | 2–2 | ≈−$4.4 | ETH/BTC TP vs XRP/BNB settle losses |
| Restart 17:48 → 18:02 | ~6 closes | **+$2.78** closed | equity $108.28 → $112.26 |

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity |
|---|---|---|---|---|
| ~15:30 UTC | 201 | 90 | +$120.86 | $137.47 flat |
| ~15:43 UTC | 204 | 90 | +$127.78 | ~$126–144 marked |
| Prior report ~17:00 | — | — | — | **~$140** |
| Halt flat 17:46 | 239 | 88 | +$115.35 | **$108.28** |
| **Latest 18:02** | **245** | **89** | **+$118.13** | **$112.26** |

Path: ~$20 start → overnight ~$67 → 10:00 baseline ~$94 → session HW **$151.45** → halt re-anchor **$108.28** → now **$112.26**.

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only (excludes open MTM). Hours after 13:40 partly reconstructed from cumulative snapshots / block rollups.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured (best hour) |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | reconstructed; first 40m 13–3 +$8.32 |
| 14–15 | uncertain split | ≈+$6.3 (to 14:52) | then into 15:00 drawdown |
| 15:00–15:30 | 5–2 | −$17.46 | ETH −$16.96 / BNB −$11.54 |
| 15:30–16:43 | 23–2 | +$16.11 | measured post Kelly/stack bump |
| 16:43–17:00 | — | — | equity climb to ~$140 (Pyth restart) |
| 17:00–17:30 | 10–3 | **−$12.31** | measured block; HOT_TICKET_LOSS alerts |
| 17:30–18:00 | ~4–2 then halt | ≈−$4 to −$8 closed | trailing halt @ 17:43; flat $108.28 |
| 18:00–18:02 | part of +6 | small + | back to $112.26 with 4 opens |

**Day pace:** ~+$5.7–6.1/hr closed since 10:00 through mid/late afternoon (down from ~$8.5/hr at the +$58 peak).

**Through 13:40 (measured):** 49–10, +$35.99 — avg win ≈ +$1.54, avg loss ≈ −$3.93

---

## How the bot is working

**What's working**
- Still clearly +EV on the day (+$46 closed @ 17:30) and lifetime (+$118 closed / ~$112 equity from ~$20).
- Trailing halt did its job: stopped the bleed when equity $104.21 ≤ floor $106.01 off HW $151.45.
- Post-halt recovery is orderly: Kelly cut 0.40→0.33, floor $100→$95, HW re-anchored, runner+journal back up, +$4 equity in ~15m.
- Multi-venue lead + series governor (SOL demoted) still the core stack.

**What hurt this hour**
- **17:30 hot-ticket cluster at 26% risk:** NEAR −$12.58, SOL −$7.29, DOGE −$9.36 — journal `HOT_TICKET_LOSS` / `BIG_LOSS`.
- Loss asymmetry remains the main risk: avg loss still ~2–3× avg win; one boosted basket erased a chunk of the afternoon.
- Day closed PnL gave back ~$12 from the 97–15 / +$58 high-water report.

**Watch items**
- Keep stack/hot-ticket caps honest at higher risk % — the 1.5× cap did not fully prevent the 17:30 hit size.
- SOL remains weak; demotion should stay.
- Open MTM at 18:02 (NEAR/SOL/ETH/DOGE YES on 14:15 window) — trust closed PnL + cash over marked equity spikes.
- This automation cannot read live `state_live.json` on the trading VM; figures lag the last DO OR DIE transcript pull (~18:02).

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

**Delta vs prior automation report (PR #4 / ~17:00):** day 97–15 +$58 → 107–18 +$46; equity ~$140 → $112; new trailing-halt cycle documented.
