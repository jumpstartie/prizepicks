# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-05 ~00:02 UTC (automation cron)  
**Data freshness:** Newest live book on trading VM ~**23:46:55–23:47:47 UTC** (flat cash after :45 triple settle; overnight restart scanning); agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) last message **~23:47 UTC**, status **IDLE** @00:00  
**Source:** `runner_live.log` / `state_live.json` / Kalshi balance via DO OR DIE transcript  
**Bot status (last confirmed):** **LIVE / not halted**, flat **$97.75**, open **0**. `kalshi-live` + `early_tip_live` both running after overnight-sprint restart (**HALT_FLOOR=$78**, **RISK_FRAC_MIN=0.18**, **TICKET_COST_CAP_FRAC=0.28**, **SKIP_ENTRY_RICH=0.92**). Early-tip **FORCE-armed** (5–4). No fills after 23:46 restart confirmed in transcript; scanning `:00` window (DOGE signals only).

---

## Headline

| Metric | Value |
|---|---|
| **Flat equity / cash (23:47)** | **$97.75** (open **0**, **halted=False**) |
| **Session ATH (still)** | **$193.22** @22:50–22:51 |
| **Prior report flat (23:02)** | **$104.68** |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$4.00** |
| **Day equity vs halt-log start ($61.54)** | **+$36.21** |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **still stale** |
| **Lifetime closed (23:46)** | **326 closes · 88% · +$98.75** |
| **Last hour path (23:02 → 23:47)** | Flat **$104.68 → $97.75** (**−$6.93**); interim peak **$106.86**; :45 triple settle **−$9.11** |
| **vs prior hourly report (PR #10 / 7446 / ~23:04)** | Flat **$105 → $98**; lifetime **315 / +$106 → 326 / +$99**; win% **89 → 88**; runner **killed → restarted overnight sprint** |

Day still barely green vs 10:00 baseline (**+$4**), but the post-nuke recovery stalled: book climbed only to **~$107**, then rich-NO scratches at :45 knocked it back under **$100**. Overnight sprint is **live** with a looser floor and fatter 70–90¢ bias.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale) |
| Equity path @23:02 | — | **+$10.93** vs $93.75 | high (prior) |
| **Equity path @23:47** | — | **+$4.00** vs $93.75 | **high** (flat cash) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines.

### Today since midnight (last formal)

- **177–24**, **+$104.86** (@17:38) — not refreshed after that.

### Lifetime (runner closed book)

| Marker | Closed | Win% | Closed PnL | Equity / cash |
|---|---|---|---|---|
| Prior report 22:09 | ≥305 | — | — | **$134.88** flat |
| ATH 22:50–22:51 | **314** | **89** | **+$194.73** | **$193.22** flat |
| ETH settle 23:00:22 / prior report | **315** | **89** | **+$106.19** | **$104.68** flat **HALTED** |
| Post-restart peak ~23:15–23:38 | **319–323** | **89** | **+$108.33 → +$107.85** | **$106.78–$106.86** |
| **:45 triple settle + restart 23:46** | **326** | **88** | **+$98.75** | **$97.75** flat **LIVE** |

Path: 10:00 baseline **$93.75** → ATH **$193.22** → ETH nuke **$104.68** → weak bounce **$106.86** → :45 scratches **$97.75**.

---

## Hourly win / loss (2026-08-04 → 08-05 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. **No formal `by hour` dump after 19:43** — 20:00–00:00 reconstructed from equity/cash prints and settle lines.

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
| 19:00–20:00 | n=17 partial → giveback | closed ≈+$10.18 then equity giveback | prior |
| 20:00–21:00 | no full bucket | near-floor scare → ratchet | prior |
| 21:00–22:00 | no full bucket | → flat **$134.88** | prior |
| 22:00–23:00 | no full bucket | flat **$135 → $105**; peak **$193**; ETH **−$88.54** | prior report |
| **23:00–00:00** | **≈7–4** post-restart (+ ETH already in prior) | flat **$105 → $98**; closed **+$106 → +$99** | see below |

**23:00 hour path (this report):**
- 23:00:22: ETH NO settle **LOSS −$88.54** → **$104.68** / closed **315 · +$106.19** / **HALTED** (already in prior cron)
- 23:03:38: **unhalt + restart** bankroll **$104.68**, floor **$95**, ticket-cost cap live, risk pinned **13%** (`cut_neg_edge`)
- 23:09–23:15: small :15 favorites (BTC/BNB/ETH/XRP etc.) → closed **319 · +$108.33**, flat **~$106.78**
- 23:18–23:30: more :30 tickets; **ETH YES LOSS −$1.36** @23:30:21
- ~23:38: closed **323 · +$107.85**, flat **$106.86** (peak post-nuke)
- 23:40–23:45: stacked rich NOs (DOGE/XRP/ETH @89–94¢, bn=flat)
- **23:45:20–21: triple SETTLE LOSS** −$3.04 / −$4.86 / −$1.21 (**−$9.11**) → flat **$97.75** / closed **326 · +$98.75** / win% **88**
- 23:45:40–23:46:54: stop + overnight restart — **HALT_FLOOR 95→78**, **RISK_FRAC_MIN→0.18**, **TICKET_COST_CAP=0.28**, **SKIP_ENTRY_RICH=0.92**; soft ice reopened
- 23:47: both runners up; scanning new window; **no new fill** yet in transcript

**Post-restart closed sample (315→326, after prior report):**
- Approx **7 wins / 4 losses** (flats excluded): small TP scratch wins on :15/:30, then ETH −$1.36 + :45 triple −$9.11
- Closed PnL **+$106.19 → +$98.75** (**−$7.45**)
- Flat cash **$104.68 → $97.75** (**−$6.93**)

**Day pace:** equity ~+$0.3/hr since 10:00 ($93.75 → $97.75 over ~13.8h). Lifetime closed still **+$99** net with **88% WR** across **326** closes — down from the **+$195** peak before the ETH nuke.

---

## How the bot is working

**What's working**
- Restart after the ETH nuke **did** complete; ticket-cost cap (**28%**) is hot — no repeat 101-contract ticket this hour.
- Post-restart favorites printed a short green stretch (**$104.68 → $106.86**, closed **+$108.33** peak).
- Overnight config explicitly targets the regime that built the **$190** book: **70–90¢ + Binance lead**, ice sizing (not hard block), room under floor (**$78**).
- Early-tip module **FORCE-armed**; dual process (`runner` + `early_tip_live`) confirmed @23:47.

**What hurt / watch**
- Recovery failed to compound: **~$2** of bounce, then **−$9** on three rich flat-lead NOs at once.
- Kelly/edge still damaged by the −$88 outlier (`cut_neg_edge`, negative EV sample) — agent raised prior strength / risk floor to force size back up; that is aggressive overnight.
- Formal day/midnight W–L still frozen since **17:38**.
- **No transcript proof after 23:47** — agent is IDLE; tmux may still be trading, but this automation cannot see live files on the VM.

**What changed since prior hourly report**
- Flat **$104.68 → $97.75**; lifetime closed **315 → 326**; closed PnL **+$106 → +$99**; win% **89 → 88**.
- Runner **restarted** with overnight sprint knobs (floor **$78**, risk min **18%**, rich skip **0.92**, ticket cap **0.28**).
- Day equity vs 10:00 **+$11 → +$4**.

**Watch items**
- Next cron: did overnight sprint fill the `:00`/`:15` windows, and did cash leave **$97.75**?
- Confirm no second oversized ticket (cap should bind ≤28% of book ≈ **$27**).
- Re-run formal `since 10:00` / midnight rollups when trading agent is awake.
- Trailing floor will re-arm off new HW once equity climbs; current static pad is **$78**.

---

## Methodology

```text
rows = closed trades in state_live.json with close_ts in window
wins   = pnl > 0
losses = pnl < 0
pnl    = sum(pnl)   # flats (pnl==0) excluded from W–L
equity = Kalshi cash + open 15m exposure (separate from closed PnL)
```

Post-17:38 estimates use flat-to-flat cash deltas, equity `closed`/`pnl` log lines, settle lines, and the post-nuke closed dump from the trading agent.

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR #10 / 7446 / ~23:04):** flat **$104.68 → $97.75**; lifetime closed **315 / +$106 → 326 / +$99**; day equity **+$11 → +$4** vs $93.75; day formal W–L unchanged at **107–18 +$45.91**; hour = weak bounce then :45 **−$9.11** scratches; runner **restarted overnight sprint @~$98**.
