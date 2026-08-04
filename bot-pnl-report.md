# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~21:20 UTC (automation cron)  
**Data freshness:** Last hard live read on trading VM ~**20:22:48 UTC** (DO OR DIE agent went IDLE ~20:43; no equity polls after ~20:23)  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** `kalshi-live` tmux runner **alive** after **20:17:45** ratchet redeploy. Cursor agent **IDLE** since ~20:43 (observer/research only). `halted=False`, floor **$95** + 0.70×HW trail, bankroll boot **$112.92**, risk **13.0%** edge Kelly. Price band **[0.70, 0.999)**; metals OFF; SOL/NEAR out; core BNB/XRP/ETH/BTC + DOGE×0.5.

---

## Headline

| Metric | Value |
|---|---|
| **Marked equity (last print 20:22:48)** | **$128.73** (cash **$105.39**, **5 open**) |
| **Ratchet bankroll (20:17:45 boot)** | **$112.92** |
| **Flat cash path this hour** | **$127.32** @20:00 → dip **~$96.24** @20:11 → flat **$107.79** @20:15 → stop print **$132.20** (recon quirk) → ratchet **$112.92** |
| **Day equity PnL (vs ~$94 @ 10:00)** | **≈ +$35** ($128.73 marked) |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) |
| **Lifetime closed (last equity line 20:22)** | **290 closes · 88% · +$148.27** |
| **Last hour (20:00 → 20:22 marked)** | **≈ +$1.41** equity ($127.32 → $128.73) with 5 open; closed book **≈ −$2.64** (+$150.91 → +$148.27) |
| **vs prior hourly report (~20:02)** | Flat cash **$127 → marked $129**; lifetime closed **280 / +$151 → 290 / +$148**; floor **$105 → $95**; band **0.85 → 0.70** |

Roughly flat-to-slightly-up marked equity after a near-floor scare (~$96 cash vs $95 halt). Closed-book lifetime slipped ~$2.6 while +10 closes printed — recent settles were a net drag. Ops widened the price band and lowered the floor into **ratchet** mode; runner still up, but this report has **no post-20:23** live confirmation.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** |
| ~19:43 (prior reconstructed) | **≈ 147–24** | **≈ +$77** | medium-low |
| **~20:22 (lifetime delta only)** | formal still **107–18** | closed book **≈ −$2.64** vs 19:42 | low for day W–L |
| Equity path @20:22 | — | **≈ +$35** vs $94 | **high** (marked equity) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked equity / lifetime closed lines for the 20:00 hour.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| Halt flat 17:46 | 239 | 88 | +$115.35 | **$108.28** |
| Metals restart 18:15 | 249 | 89 | +$123.60 | **$117.66** flat |
| Prior report 19:00 | — | — | — | **$137.74** flat |
| Prior report 19:42 | **280** | **89** | **+$150.91** | **$131.82** (3 open) |
| Prior report ~20:00 | — | — | — | **$127.32** flat |
| Sprint redeploy 20:01 | — | — | — | **$123.19** bankroll |
| Near-floor 20:11 | — | — | — | cash **~$96.24** (3 open) |
| Flat stop 20:15 | — | — | — | cash **$107.79** / stop print **$132.20** |
| Ratchet boot 20:17 | — | — | — | bankroll **$112.92**, HW **$139.18** |
| **Latest equity line 20:22** | **290** | **88** | **+$148.27** | **$128.73** eq / **$105.39** cash (**5 open**) |
| Closed analysis ~20:36 | **293** filled | flat pocket ~89% | **≈ +$148.28** | — |

Path: ~$20 start → overnight ~$67 → 10:00 baseline ~$94 → session HW **$151.45** → halt re-anchor **$108.28** → recovery peak **$137.74** @19:00 → **$127.32** @20:00 → near-floor **~$96** @20:11 → marked **$128.73** @20:22 with 5 open.

HW watermark last seen **$139.18** (down from **$151.45** @17:38).

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. **20:00 hour incomplete** (last live print 20:22).

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
| 19:00–20:00 | n=17 partial → giveback | closed ≈+$10.18 then equity **−$10.42** | prior report |
| **20:00–21:00** | **incomplete / no full bucket** | **marked eq ≈ +$1.41** to 20:22; closed ≈ **−$2.64** | see below |

**20:00 hour path (through last live print):**
- 20:00:53 flat **$127.32**, halted=False
- 20:01:45 sprint boot bankroll **$123.19**, floor **$105**, band **[0.85, 0.999)**
- 20:08–20:11: cash **123.16 → 96.24** (3–4 open) — within ~$1 of $95 floor
- 20:15:05–20:15:29: flat cash **$107.79**, stop print **$132.20** (mark-to-cash recon quirk at shutdown)
- 20:17:45 ratchet boot: bankroll **$112.92**, floor **$95**+trail, band **[0.70, 0.999)**, series BNB/XRP/ETH/BTC/DOGE
- 20:18–20:22: equity stuck **$128.73** / cash **$105.39** / **5 open** / closed **290 · 88% · +$148.27**
- After **20:23**: agent did observer/research only — **no further equity polls** through IDLE @20:43; runner tmux still listed @20:41

**Why marked +$1 ≠ closed −$2.6:** open MTM on 5 positions and the mid-hour stop/redeploy cash reconciliation dominate the hour; closed-book lifetime slipped while marked equity held near the 20:00 flat print.

**Day pace:** equity ~+$3.2/hr since 10:00 ($94 → $129 over ~10.4h). Lifetime closed book off its 19:42 high (**+$150.91 → +$148.27**).

---

## How the bot is working

**What's working**
- Still green on the day vs the ~$94 10:00 baseline (**≈ +$35** marked).
- Lifetime closed book still ~**88%** WR and ~**+$148** realized across **290** closes.
- Near-floor scare (~$96 cash) did **not** trip halt; runner survived into ratchet redeploy.
- Core crypto favorites (BNB/XRP/ETH/BTC + DOGE) remain the book; metals/SOL/NEAR stay out.
- Safety stack still engaged: risk floored ~**13%**, trailing floor **0.70×HW**, static floor **$95**.

**What hurt this hour**
- Cash path **$127 → ~$96** mid-window — largest intra-hour drawdown since the 17:00 bleed.
- Lifetime closed PnL gave back **~$2.64** from the 19:42 high while printing +10 closes.
- Multiple redeploys (sprint @20:01 → ratchet @20:17) while capital was working; stop-flat cash print (**$132.20**) disagreed with prior flat (**$107.79**) — treat mid-redeploy cash with caution.
- Edge sample on the prior sprint boot had already cooled (WR ~83.7%, EV ~+$0.36).

**What changed this hour**
- 20:01 sprint: floor **$105**, band **[0.85, 0.999)**, bankroll **$123.19**.
- 20:15–20:17 ratchet: floor back to **$95**+trail, band widened to **[0.70, 0.999)**, `SOFT_BN_FLAT_MULT=0`, Kelly frac **0.40** / risk max **0.30** (runtime still ~13% on edge sample), bankroll **$112.92**.
- ~20:41: `kalshi-observer` paper-only on BTC/ETH/XRP/BNB/DOGE/SOL/NEAR — **zero live orders** from observer; live runner left untouched.

**Watch items**
- **Data lag:** last hard equity line is **~20:23**; this 21:20 cron cannot confirm whether the 5 opens settled green or whether the runner is still healthy after agent IDLE.
- Day formal W–L still stuck at 17:38 (**107–18**); trust marked equity / lifetime closed lines until next rollup.
- Floor **$95** with cash last seen **$105.39** and 5 open — leash is loose again vs the $105 sprint floor; another soft cluster can retest halt.
- HW **$139.18** vs session peak **$151.45** — still ~$12 under watermark.
- This automation cannot read live `state_live.json` on the trading VM; figures lag the last DO OR DIE transcript pull.

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

**Delta vs prior automation report (PR #7 / ac23 / ~20:02):** marked equity **$127 flat → $129** (5 open); lifetime closed **280 / +$151 → 290 / +$148**; day formal W–L unchanged at **107–18 +$45.91**; last hour flipped from equity **−$10** to marked **≈ +$1** (incomplete); floor **$105 → $95**; price band **0.85 → 0.70** (ratchet).
