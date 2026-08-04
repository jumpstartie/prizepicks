# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~23:04 UTC (automation cron)  
**Data freshness:** Newest live book on trading VM ~**23:02:02–23:02:20 UTC** (flat cash after ETH settle); agent tools through **~23:03:25 UTC**  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** **HALTED** and **flat**. ETH NO ticket settled **LOSS −$88.54 @23:00:22**. Live runner **`kalshi-live` killed @23:03:21** while agent patches a 30% ticket-cost cap (`TICKET_COST_CAP_FRAC=0.30`, commit `bf6e0ed`); runners swept to **ZERO** at transcript end. Paper `kalshi-observer` / `kalshi-early` not re-verified after kill. Early-tip module last seen **DISARMED 3–0** (need 5–0). Floor last armed at **$135.25** off HW **$193.22** (breached). Agent was preparing unhalt/restart on **$104.68** — **not finished** in this pull.

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (23:02)** | **$104.68** (open **0**, **HALTED**) |
| **Session ATH (22:50–22:51)** | **$193.22** flat (then false cash-halt → ETH fill → settle loss) |
| **Prior report flat (22:09)** | **$134.88** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$10.93** |
| **Day equity vs halt-log start ($61.54)** | **+$43.14** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (23:01–23:02)** | **315 closes · 89% · +$106.19** |
| **Last hour path (22:09 → 23:02)** | Flat **$134.88 → $104.68** (**−$30.20**); peaked **$193.22**; big ETH ticket **−$88.54** |
| **vs prior hourly report (PR #9 / 1047 / ~22:23)** | Flat **$135 → $105**; lifetime closed **305 / +$176 → 315 / +$106**; HW **$161 → $193** then breached; runner **up → killed for restart** |

Day still **green vs 10:00 baseline**, but the 22:00 hour erased the prior report’s +$41 day equity down to ~+$11 and cut lifetime closed PnL by ~$70 after the ETH NO wipeout. Bot is **halted / not trading** pending restart with a hard ticket-size cap.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale) |
| Ratchet since 20:17 @21:40 | **15–0** | **+$27.51** | high (slice only; not refreshed) |
| Equity path @22:09 | — | **+$41.13** vs $93.75 | high (prior report) |
| **Equity path @23:02** | — | **+$10.93** vs $93.75 | **high** (flat cash) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines for the 22:00 hour.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| Halt flat 17:46 | 239 | 88 | +$115.35 | **$108.28** |
| Prior report 20:22 | 290 | 88 | +$148.27 | **$128.73** eq / **$105.39** cash (5 open) |
| Prior report 21:36 | 305 | 89 | +$175.78 | **$125.16** eq / **$110.26** cash (1 open) |
| Prior report 22:09 | ≥305 | — | — | **$134.88** flat / 0 open / HW **$161.32** |
| ATH halt ~22:31 | **310** | **89** | **+$186.13** | **$181.39** flat **HALTED** |
| Unhalt / restart 22:39 | — | — | — | **$181.39** bankroll, floor **$126.97** |
| Soft spot ~22:48 | — | — | — | **$142.32** flat (dual-runner chaos suspected) |
| New ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat; floor **$135.25** |
| False halt + ETH fill 22:51–22:58 | 314 | 89 | +$194.73 | cash **$104.68** / eq **$193.22** / **1 open** **HALTED** |
| **ETH settle LOSS 23:00:22** | **315** | **89** | **+$106.19** | **$104.68** flat **HALTED** |

Path: ~$20 start → overnight ~$67 → 10:00 baseline **$93.75** → session HW state **$193.22** → prior flat **$134.88** @22:09 → ATH **$193.22** @22:50 → **ETH −$88.54** → **flat $104.68** @23:02.

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. **No formal `by hour` dump after 19:43** — 20:00–23:00 reconstructed from equity/cash prints and settle lines.

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
| 18:00–19:00 | n=24 | **+$25.38** | diagnostic 100% WR |
| 19:00–20:00 | n=17 partial → giveback | closed ≈+$10.18 then equity giveback | prior reports |
| 20:00–21:00 | no full bucket | near-floor scare → ratchet 15–0 starts | prior |
| 21:00–22:00 | no full bucket | path → flat **$134.88**; lifetime **305 / +$176** | prior |
| **22:00–23:00** | **no full bucket** | flat **$135 → $105**; peak **$193**; ETH **−$88.54** | see below |

**22:00 hour path (this report):**
- 22:09: flat **$134.88** / open **0** / HW **$161.32** / halted=False (prior report)
- ~22:31: equity/cash **$181.39** / closed **310 · +$186.13** / **HALTED** (floor trip after HW ~$177)
- 22:36–22:39: unhalt; HW re-anchored **$181.39**; floor **$126.97**; bankroll restart **$181.39** @ **23.1%** risk
- ~22:48: flat **$142.32** (~−$39 from ATH restart); dual-runner kill/restart suspected
- 22:50–22:51: new ATH **$193.22** flat / closed **314 · +$194.73** / floor **$135.25** / risk **~27.8%**
- 22:51:58: **HALT** on cash-only print **$104.68 ≤ floor $135.25** (race); then **LIVE FILL** ETH NO **101.77 @ ~0.87**
- 22:52–22:58: marked equity **$193.22** / cash **$104.68** / open **1** / still **HALTED**
- **23:00:22: SETTLE ETH NO LOSS −$88.54** → cash/equity **$104.68** / open **0** / closed **315 · +$106.19**
- 23:03: ticket-cost cap patched; **`kalshi-live` killed**; runners **ZERO**

**Hourly net vs prior report anchor ($134.88 @22:09):**
- To 23:02 flat **$104.68**: **≈ −$30.20** marked/flat
- Closed-book lifetime **+$175.78 → +$106.19**: **−$69.59** (includes ETH −$88.54 after interim +$18.95 to +$194.73)
- Peak-to-trough this hour: **$193.22 → $104.68** (**−$88.54**)

**Day pace:** equity ~+$0.8/hr since 10:00 ($93.75 → $104.68 over ~13.0h) — sharply slower after the 22:00 wipeout. Closed-book lifetime still **+$106** net with **89% WR** across **315** closes.

---

## How the bot is working

**What's working**
- Still green on the day vs 10:00 baseline (**+$11** equity) and vs halt-log start (**+$43**).
- Through 22:50 the book had printed a **new ATH $193.22** and lifetime closed peak **+$194.73** — proof the ratchet / favorite-maker engine can compound hard when tickets stay small.
- Win rate held **89%** even after the ETH loss (315 closes).
- Agent responded with a concrete fix: **`TICKET_COST_CAP_FRAC=0.30`** so a single stacked ticket cannot eat ~half the book again.

**What hurt / watch**
- **ETH NO −$88.54** was the hour’s entire story: ticket ~**$88–89** notional (~**46% of book** via size-mult stacking past halt-cap intent).
- False **cash-vs-floor halt race** at 22:51 left the bot halted *with* a huge open; settle then crystallized the loss with no active risk management.
- Dual-runner chaos ~22:48–22:51 makes the **$181 → $142 → $193** path hard to trust as pure alpha.
- Formal day/midnight W–L still frozen since **17:38**.
- **Live runner is down** at report time — no new edge until unhalt + restart completes.

**What changed since prior hourly report**
- Climbed **$135 → $193** ATH, then gave it all back plus more on one ETH ticket → **$105**.
- Lifetime closed **305 → 315**; closed PnL **+$176 → +$106**.
- Effective floor briefly **$135.25** off HW **$193**; now breached / halted.
- Whale-harvest + halt-confirm-polls + early-tip module were in play earlier in the hour; ticket-cap patch is the newest live-code change.
- Runner stopped for restart @23:03.

**Watch items**
- Next cron: confirm whether agent **unhalted / restarted** and at what bankroll/floor.
- Verify ticket-cost cap is hot in the new process (cap was committed but prior halt process did not load it).
- Re-run formal `since 10:00` / midnight rollups when trading agent is awake.
- Treat HW **$193.22** as real flat ATH (printed with open=0) — recovery target, not current floor basis while halted.
- This automation cannot read live files on the trading VM; figures lag the last DO OR DIE transcript pull.

---

## Methodology

```text
rows = closed trades in state_live.json with close_ts in window
wins   = pnl > 0
losses = pnl < 0
pnl    = sum(pnl)   # flats (pnl==0) excluded from W–L
equity = Kalshi cash + open 15m exposure (separate from closed PnL)
```

Post-17:38 estimates use flat-to-flat cash deltas, equity `closed`/`pnl` log lines, settle lines, and markout hourly buckets when a full window rollup was not re-run.

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR #9 / 1047 / ~22:23):** flat **$134.88 → $104.68**; lifetime closed **305 / +$176 → 315 / +$106**; day equity **+$41 → +$11** vs $93.75; day formal W–L unchanged at **107–18 +$45.91**; hour dominated by ETH settle **−$88.54**; runner **alive → halted → killed for ticket-cap restart**.
