# RTP-20 — Ratchet TP Printer (counter-strategy)

## Goal
Rebuild toward a day-1 style streak (high WR, compound to 2×+) without the nuke tails that erased today.

## What the live book proved

| Pattern | Result |
|--------|--------|
| Core (BNB/XRP/BTC) **flat + TP/fade** | **+$183 @ 100% WR** — the printer |
| Soft/mid **flat + settle** | **−$266** — the nuke |
| Tickets with **cost ≥ $15** | **−$41** despite ~90% WR |
| Agree-only (block flat entries) | ~19 trades, starved |
| ETH / SOL / NEAR / metals / setup_gov | expectancy drains |

Best win streak in book: **52** (AUG03). Peak recon HW ~**$215**. Today: TP/fade green, settle ~−$80.

## Failure modes to counter

1. **Settle ride** on soft/mid bn=flat (every pnl≤−$7 was settle; 18/21 bn=flat)
2. **Gate bypass** — entries ≥ soft_max skipped BN rules (91–92¢ BTC)
3. **Size tails** — large tickets keep high WR but negative $ expectancy
4. **Universe creep** — SOL/ETH/metals/NEAR / early-tip / gov hot stacks
5. **VM freeze** — whole stack sleeps; missed windows (keep_alive jump recovery)
6. **Ratchet without bank** — trail on marked equity / HW above cash → self-halt

## RTP-20 rules

### Entry (printer)
- Series: **BNB, XRP, BTC** only
- Band: **70–94.9¢** (skip ≥95¢)
- BN gate on **all** tradable (`SOFT_ENTRY_MAX=0.95`)
- bn=flat allowed at **×0.50**; agree ×1.20
- Max concurrent **3**, exposure ≤60%, ticket cost ≤**15%** equity

### Exit (anti-nuke) — non-negotiable
- TP abs **97¢**, soft spike **95¢**, spike-fade ON
- **Pre-settle flatten** at 60s for entry &lt;95¢ — no binary settle in the nuke band
- No stop-loss chop

### Ratchet (lock the climb)
- Static floor pad under book
- Trail **0.65 × flat high-water** (reanchor HW to cash on deploy so trail doesn’t halt a drawdown book)
- No setup_gov / series_gov hot multipliers

### Forbidden
- ETH, SOL, DOGE, NEAR, metals as core
- Early-tip live sharing wallet
- Riding soft/mid to settle
- Ticket &gt;15% / uncapped Kelly after outliers

## Operating phases

1. **Rebuild** (cash &lt; ~$90): RTP-20 as above; prioritize WR over frequency
2. **Compound** (cash $90–180): same exits; allow risk frac to press toward max when edge EV&gt;0
3. **Protect** (cash &gt; ~$180): trail binds harder; never re-enable settle rides or satellites until 50+ trade clean WR

## Success metrics
- Exit mix: TP/fade/pre_settle ≫ settle
- No single loss &gt; 15% of book
- Soft/mid+flat+settle PnL ≈ 0 (blocked)
- Rolling 30-trade WR ≥ ~90% on core

## 80%+ merge overlay (live)

On top of RTP-20 exits / sizing / core series:

| Gate | Setting |
|------|---------|
| Confirm polls | **2** |
| Time window | **secs_left ∈ [180, 780]** |
| Lognormal digital | `P(side) ≥ 0.65` and `edge ≥ 0.03` |
| σ | realized short-horizon lead vol → τ (ann floor 40%) |
| Venue | disagree blocked; flat ×0.50 still allowed |

Module: `bot/lognormal_gate.py` (driftless Φ(d2) vs `floor_strike` + lead spot).
Skips log as `skip_lognormal`. Toggle via `LOGNORMAL_GATE=0` to revert to plain RTP-20.
