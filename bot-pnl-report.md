# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~20:02 UTC  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** Trading runner **alive** in tmux after **20:01:45** redeploy. Cursor agent was actively operating around the hour. `halted=False`, floor raised to **$105**, bankroll **$123.19**, risk **13.0%** edge Kelly (~$16.01/trade). Sprint price band **[0.85, 0.999)**; metals OFF; SOL/NEAR out; core BNB/XRP/ETH/BTC + DOGE satellite.

---

## Headline

| Metric | Value |
|---|---|
| **Flat cash (20:00 state read)** | **$127.32** (open 0, halted=False) |
| **Runner bankroll (20:01:45 boot)** | **$123.19** |
| **Day equity PnL (vs ~$94 @ 10:00)** | **≈ +$33** ($127.32) / **≈ +$29** ($123.19) |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) |
| **Day closed book (est. through ~19:43)** | **≈ 147–24** (~+$77) — reconstructed |
| **Lifetime closed (last equity line 19:42)** | **280 closes · 89% · +$150.91** |
| **Last hour (19:00–20:00 flat equity)** | **−$10.42** ($137.74 → $127.32) |
| **19:00Z closed bucket (partial @~19:43)** | **n=17 · +$10.18 · 76% WR** then gave back |
| **vs prior hourly report (~19:01)** | Equity **$138 → $127**; lifetime closed **249 / +$124 → 280 / +$151** |

Giveback hour after the strong 18:00 recovery. Still solidly green on the day vs the ~$94 10:00 baseline, with lifetime closed book at a new high (+$150.91 @19:42). Ops responded by cutting risk and raising the halt floor to $105.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** |
| ~19:00 (prior automation est.) | **≈ 126–24** | **≈ +$70** | low–medium |
| **~19:43 (reconstructed)** | **≈ 147–24** | **≈ +$77** | medium-low |
| Equity path @20:00 | — | **≈ +$33** vs $94 | **high** (cash) |

No fresh `since 10:00` tool rollup after 17:38. Post-17:38 W–L chains diagnostic hourly buckets + lifetime closed deltas; prefer cash/equity for the 19:00 hour story.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.
- Reconstructed through ~19:43: **≈ 217–30 / ~+$136** (low–medium confidence).

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| Halt flat 17:46 | 239 | 88 | +$115.35 | **$108.28** |
| Prior report 18:02 | 245 | 89 | +$118.13 | **$112.26** (4 open) |
| Metals restart 18:15 | 249 | 89 | +$123.60 | **$117.66** flat |
| Prior report 19:00 | — | — | — | **$137.74** flat |
| **Latest equity line 19:42** | **280** | **89** | **+$150.91** | **$131.82** (3 open) |
| Flat 19:45 | — | — | — | **$131.12** |
| **State read ~20:00** | — | — | — | **$127.32** flat |
| **Sprint redeploy 20:01** | — | — | — | **$123.19** bankroll |

Path: ~$20 start → overnight ~$67 → 10:00 baseline ~$94 → session HW **$151.45** → halt re-anchor **$108.28** → peak recovery **$137.74** @19:00 → **$127.32** @20:00 → **$123.19** sprint boot.

14h realized path @~19:43: cum **+$91.70**, peak **+$101.96** @19:30, giveback from peak **−$13.74**.

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed.

| Hour (UTC) | W–L | PnL | Notes |
|---|---|---|---|
| 10–11 | 16–2 | +$2.57 | measured |
| 11–12 | 4–2 | +$2.77 | measured |
| 12–13 | 16–3 | +$22.33 | measured (best early hour) |
| 13–14 | ≥13–3 (partial) | ≈+$25.63 | reconstructed |
| 14–15 | uncertain split | ≈+$6.3 (to 14:52) | then into 15:00 drawdown |
| 15:00–15:30 | 5–2 | −$17.46 | ETH/BNB hits |
| 15:30–16:43 | 23–2 | +$16.11 | post Kelly/stack bump |
| 16:00–17:00 | n=15 | **+$10.95** | diagnostic 100% WR |
| 17:00–18:00 | n=18 | **−$16.73** | HOT_TICKET / soft bleed |
| 18:00–19:00 | n=24 | **+$25.38** | diagnostic 100% WR; flat cash ≈+$28 |
| **19:00–20:00** | **n=17 partial → giveback** | **closed ≈+$10.18 then equity −$10.42** | see below |

**19:00 hour path (flat / near-flat cash):**
- 19:00:27 flat **$137.74**
- 19:35–19:42 equity prints **$128.69 → $131.82** (closed 277→280, lifetime closed PnL **+$147.72 → +$150.91**)
- 19:45:24 flat **$131.12** (redeploy, risk cut to 13%)
- ~20:00 state **$127.32** flat → hour equity **−$10.42**
- 20:01:45 sprint boot bankroll **$123.19** (floor **$105**)

**Why closed +$10 early ≠ equity −$10 full hour:** early 19:00Z bucket (+$10.18 on 17 closes @76% WR through ~19:43) was offset by later soft/metals giveback, open MTM, and post-19:45 drift. Last-1h diagnostic around then showed **19–4 / +$14.35** on a rolling window that still included late 18:00 winners.

**Day pace:** equity ~+$3.3/hr since 10:00 ($94 → $127 over ~10h). Closed-book lifetime pace still stronger (+$150.91 realized).

---

## How the bot is working

**What's working**
- Lifetime closed book still ~**89%** WR and pushed to **+$150.91** / **280** closes (@19:42) — best realized mark of the session.
- Mid/rich favorites remain the edge pocket; XRP/BTC/ETH carried recent diagnostics; SOL/NEAR already removed.
- Safety stack still engaged: risk cut 18.9%→13%, then floor **$95 → $105** after the giveback hour — locks most of the day gain vs $94 baseline.
- 18:00 hour (+$25.38 closed / ~+$28 cash) proved the strategy can recover hard after the 17:00 bleed.

**What hurt this hour**
- Flat equity **$137.74 → $127.32** (**−$10.42**); sprint bankroll print **$123.19**.
- Soft band and leftover metals/satellites still create loss asymmetry (diagnostic soft pocket negative over 5h).
- Edge WR on the 20:01 boot slipped to **83.7%** (n=30) with EV **+$0.363** — softer than the 19:00 boot (90.9% / +$0.769).

**What changed this hour**
- 19:00 redeploy: ice soft, drop SOL/NEAR, ~19% risk (from prior report).
- 19:45 redeploy: risk **13%**, bankroll **$131.12**.
- 20:01 sprint redeploy: bankroll **$123.19**, floor **$105**, price **[0.85, 0.999)**, metals OFF, series BNB/XRP/ETH/BTC + DOGE×0.5.

**Watch items**
- Day formal W–L still stuck at 17:38 (**107–18**); trust cash/equity for the last two hours until next rollup.
- Floor at **$105** now sits only ~$18–22 under current bankroll — tighter leash, fewer free swings.
- Giveback from 14h peak (−$13.74 @19:43 diagnostic) continued into the 20:00 print; next hour decides if the sprint band stabilizes or bleeds further.
- This automation cannot read live `state_live.json` on the trading VM; figures lag the last DO OR DIE transcript pull (~20:01:45).

---

## Methodology

```text
rows = closed trades in state_live.json with close_ts in window
wins   = pnl > 0
losses = pnl < 0
pnl    = sum(pnl)   # flats (pnl==0) excluded from W–L
equity = Kalshi cash + open 15m exposure (separate from closed PnL)
```

Post-17:38 estimates use flat-to-flat cash deltas, equity `closed`/`pnl` log lines, and markout hourly buckets when a full window rollup was not re-run.

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR on 68aa / ~19:01):** cash/equity **$138 → $127** (sprint bankroll **$123**); lifetime closed **249 / +$124 → 280 / +$151**; day formal W–L unchanged at **107–18 +$45.91**; last hour flipped from **≈ +$28** to **−$10** equity; floor raised **$95 → $105**.
