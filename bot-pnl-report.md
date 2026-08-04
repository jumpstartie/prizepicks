# Kalshi 15m Bot — PnL Update

**As of:** 2026-08-04 ~22:23 UTC (automation cron)  
**Data freshness:** Newest live book read on trading VM ~**22:09:00 UTC** (`state_live` flat cash); last hard `equity=` print **21:36:55 UTC**; agent last active **~22:19–22:20 UTC**  
**Source:** Live runner on agent [DO OR DIE](https://cursor.com/agents/bc-2f9f466b-ae51-4aa8-b5f1-be662ba91ecb) (`runner_live.log` / `state_live.json` via transcript)  
**Bot status (last confirmed):** `kalshi-live` tmux runner **alive** since **20:17:40** ratchet redeploy (PID 107098). Cursor agent **IDLE** after ~22:20 (was actively monitoring through 22:19). `halted=False`. Floor **$95 + 0.70×HW** → effective floor **$112.92** at HW **$161.32**. Risk **13.0%** edge Kelly (+ halt_cap when near floor). Price band **[0.70, 0.999)**; metals OFF; core BNB/XRP/ETH/BTC + DOGE. Paper `kalshi-observer` running; new `kalshi-early` early-tip module **DISARMED** (3–0, need 5–0) — not live-trading yet.

---

## Headline

| Metric | Value |
|---|---|
| **Marked / flat equity (22:09)** | **$134.88** (cash **$134.88**, **0 open**) |
| **Last hard equity print (21:36:55)** | **$125.16** (cash **$110.26**, **1 open**) |
| **Ratchet bankroll (20:17:45 boot)** | **$112.92** |
| **High-water (state)** | **$161.32** (first seen @21:37; no `equity=$161` print) |
| **Day equity PnL (vs $93.75 @ 10:00:40)** | **+$41.13** ($134.88 flat) |
| **Day closed book (last formal @17:38)** | **107–18** (+$45.91) — **stale** |
| **Lifetime closed (last equity line 21:36)** | **305 closes · 89% · +$175.78** |
| **Ratchet slice (since 20:17 @21:40)** | **15–0 · 100% · +$27.51** |
| **Last ~2h vs prior report (~20:22 → 22:09)** | Flat/marked **$128.73 → $134.88** (**+$6.15**); closed book **+$27.51** (290→305) then more untallied settles |
| **vs prior hourly report (PR #8 / d333 / ~21:20)** | Equity **$129 → $135** flat; lifetime closed **290 / +$148 → 305 / +$176**; HW **$139 → $161**; floor effective **$95 → $112.92** |

Still green on the day. After the 20:00 near-floor scare, the ratchet session printed a clean **15–0 / +$27.51** through 21:40, pushed state HW to **$161**, then finished the 21:00 hour **flat at $134.88** with no open risk. Formal day W–L is still stuck at 17:38 — trust marked/flat equity and lifetime closed lines.

---

## Total win / loss

### Day session (closed trades with `close_ts` ≥ 10:00 UTC)

| Checkpoint | W–L | Net PnL | Confidence |
|---|---|---|---|
| ~15:58 (earlier report) | **97–15** | **+$58.22** | high |
| **~17:38 (latest formal rollup)** | **107–18** | **+$45.91** | **high** (stale) |
| Ratchet since 20:17 @21:40 | **15–0** | **+$27.51** | high (slice only) |
| Equity path @22:09 | — | **+$41.13** vs $93.75 | **high** (flat cash) |

No fresh `since 10:00` tool rollup after 17:38. Prefer marked/flat equity and lifetime closed lines for the 21:00–22:00 window.

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
| Prior report 20:22 | **290** | **88** | **+$148.27** | **$128.73** eq / **$105.39** cash (**5 open**) |
| Filtered closes ~20:36 | **293** | ~89 | ≈ +$149.9 | — |
| **Latest equity line 21:36** | **305** | **89** | **+$175.78** | **$125.16** eq / **$110.26** cash (**1 open**) |
| Ratchet rollup 21:40 | ≥305 | — | ratchet **+$27.51** (15–0) | cash **$68.68** / **3 open** / floor **$112.92** |
| **Latest book 22:09** | **?** (post-305 untallied) | — | — | **$134.88** flat / **0 open** / HW **$161.32** |

Path: ~$20 start → overnight ~$67 → 10:00 baseline **$93.75** → session HW state **$161.32** → halt re-anchor **$108.28** → recovery peak **$137.74** @19:00 → near-floor **~$96** @20:11 → marked **$128.73** @20:22 → hard print **$125.16** @21:36 → **flat $134.88** @22:09.

---

## Hourly win / loss (2026-08-04 UTC)

Closed-trade PnL only unless noted as equity/cash. Hours after 13:40 partly reconstructed. **20:00 and 21:00 hours lack formal W–L buckets** (last `by hour` dump @19:43).

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
| **20:00–21:00** | **no full bucket** | path below; ratchet 15–0 spans into 21h | see below |
| **21:00–22:00** | **no full bucket** | marked **$125 → flat $135**; mid-hour cash **$69** w/ 3 open | see below |

**20:00 hour path:**
- 20:00:53 flat **$127.32**
- 20:01 sprint boot → 20:11 near-floor cash **~$96** → 20:15 flat **$107.79** → 20:17 ratchet boot **$112.92**
- 20:18–20:22: marked **$128.73** / cash **$105.39** / **5 open** / closed **290 · +$148.27**
- 20:36: filled closes **293** (no cash print)
- 20:36–21:00: **blind gap** — HW later prints **$161.32**, so a large mark-up / settle run occurred without equity polls

**21:00 hour path:**
- 21:36:55: equity **$125.16** / cash **$110.26** / open **1** / closed **305 · 89% · +$175.78** (`edge_kelly+halt_cap`)
- 21:37: HW **$161.32**, effective floor **$112.92**, halted=False
- 21:40: cash **$68.68** / **3 open**; ratchet since 20:17 = **15–0 / +$27.51** (BNB/DOGE/ETH/XRP/BTC all green)
- 21:40–22:09: no FILL/SETTLE lines captured in transcript; opens cleared; cash → **$134.88** flat
- 22:09: **$134.88** / open **0** / HW still **$161.32** / halted=False
- 22:19: `kalshi-live` still listed; `kalshi-early` disarmed 3–0

**Hourly net vs prior report anchor ($128.73 @20:22):**
- To 22:09 flat **$134.88**: **≈ +$6.15** marked/flat over ~1h45m
- Closed-book lifetime **+$148.27 → +$175.78** through 21:36: **+$27.51** (matches ratchet 15–0); post-21:40 settles not rolled up

**Day pace:** equity ~+$3.3/hr since 10:00 ($93.75 → $134.88 over ~12.1h). Closed-book lifetime off its prior 19:42 local peak narrative but now at a **new closed high (+$175.78)** with state HW **$161.32**.

---

## How the bot is working

**What's working**
- Day still green: **+$41** equity vs 10:00 baseline.
- Ratchet mode delivered a clean **15–0 / +$27.51** on BNB/DOGE/ETH/XRP/BTC through 21:40 — the best verified post-redeploy slice.
- Lifetime closed book at last print: **89% WR**, **+$176** across **305** closes.
- Finished the latest hour **flat with zero open risk** at **$134.88**.
- Trailing floor ratcheted up to **$112.92** (locks more of the day than the old $95 static).
- Live runner still up ~2h after the 20:17 redeploy; early-tip module staged but not armed.

**What hurt / watch**
- Mid 21:00 hour cash dipped to **$68.68** with 3 open while floor sat at **$112.92** — inventory risk, not a halt trip, but a sharp mark-to-cash swing.
- State HW **$161.32** has **no matching equity= print**; treat as state watermark, not a verified flat peak (does not reconcile cleanly with ratchet +$27 from $112.92).
- Formal day/midnight W–L frozen since **17:38** — headline W–L understates the post-halt recovery.
- Post-21:40 closed count unknown; **$134.88** flat is the book, but lifetime closed PnL may be above **+$175.78**.
- Gap **20:23–21:36** with almost no polls — hourly W–L for that stretch cannot be split cleanly.

**What changed since prior hourly report**
- Strong ratchet closes: **+15 closed / +$27.51** through 21:40; book later flat **$134.88**.
- Effective floor up with HW: **$112.92**.
- `kalshi-early` auto-arming early-tip module deployed (**disarmed**, paper arming gate 5–0).
- Observer still paper-only; live runner untouched.

**Watch items**
- Next cron should re-poll `state_live` / `equity=` — confirm whether $134.88 held and whether closed count moved past 305.
- If HW $161 is real, trailing floor at $112.92 is the new leash; another soft cluster into 3–4 opens can retest it quickly (see $68 cash @21:40).
- Re-run formal `since 10:00` / midnight rollups when the trading agent is awake — day W–L is badly stale.
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

Post-17:38 estimates use flat-to-flat cash deltas, equity `closed`/`pnl` log lines, ratchet slice rollups, and markout hourly buckets when a full window rollup was not re-run.

Live paths on the trading agent: `bot/state_live.json`, `bot/trades_live.jsonl`, `bot/trade_journal.jsonl`, `bot/runner_live.log`.

**Delta vs prior automation report (PR #8 / d333 / ~21:20):** flat/marked **$128.73 → $134.88**; lifetime closed **290 / +$148 → 305 / +$176**; day equity **≈ +$35 → +$41**; day formal W–L unchanged at **107–18 +$45.91**; ratchet slice **15–0 +$27.51**; HW **$139 → $161**; effective floor **$95 → $112.92**; runner confirmed up @22:19.
