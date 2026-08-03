# Favorite-maker live runner

Paper/live bot for the near-expiry favorite strategy researched in `research/`.

## $20 test sizing

```
bankroll≈$21  unit≈4.5 contracts/trade
risk/trade≈$4.00 (~20% of bankroll; $3–5 band)
max concurrent≈2–3 core books
halt if equity <= $15.00
stop-loss OFF — hold favorites to settlement; log W/L and iterate
```

~20% of equity per trade (~$4 on a $21 book). Unit auto-resizes as equity
changes. Override with `RISK_FRACTION=0.15` (~$3) or `0.25` (~$5).

## Run paper (no API keys)

```bash
START_EQUITY=20 MODE=paper python3 bot/runner.py
```

Profit-first default: BNB/SOL/XRP only, hold to settlement, stop-loss off.
In the final 3 minutes,
if either side is at 90–97¢ for 2 consecutive polls with ≥60s left, rests a
simulated maker order at the touch. Settles against the real Kalshi result.
State in `bot/state.json`, trade log in `bot/trades.jsonl`.

`PAPER_FILL=backtest` fills on the next poll (research mid-fill assumption).
`PAPER_FILL=touch` only fills when a new trade prints at the touch.

## Run live

```bash
export KALSHI_API_KEY_ID='...'
export KALSHI_PRIVATE_KEY_PATH=/path/to/kalshi.key
START_EQUITY=20 MODE=live python3 bot/runner.py
```

## Config env vars

| var | default | meaning |
|---|---|---|
| `START_EQUITY` | `20` | starting bankroll for sizing / halt |
| `MODE` | `paper` | `paper` or `live` |
| `SERIES` | `KXBNB15M,KXSOL15M,KXXRP15M` | core markets (proven live) |
| `SATELLITE_SERIES` | _(empty)_ | optional half-size exploratories |
| `SATELLITE_SIZE_MULT` | `0.5` | size multiplier for satellites |
| `WINDOW_SEC` | `180` | earliest signal window before close |
| `MIN_SECS_LEFT` | `60` | no new entries inside final minute |
| `CONFIRM_POLLS` | `2` | same-side band must hold this many polls |
| `PRICE_LO` / `PRICE_HI` | `0.90` / `0.97` | favorite price band |
| `STOP_LOSS_PCT` | `0` | stop-loss disabled (set e.g. `0.20` to enable) |
| `STOP_DISABLE_SECS` | `60` | if stop enabled, disable in final N seconds |
| `TAKE_PROFIT_ABS` | `0.98` | spike exit if mark ≥ this (on top of settle path) |
| `TAKE_PROFIT_GAIN` | `0` | optional: exit if mark ≥ entry + this ($); 0=off |
| `TAKE_PROFIT_MULT` | `0` | optional Nx entry; **off** by default |
| `TAKE_PROFIT_CAP` | `0.99` | max TP price on a $1 binary |
| `HALT_FLOOR` | `15.0` | stop the run if equity ≤ this ($) |
| `MAX_CONCURRENT` | `7` | max simultaneous open orders/positions |
| `MAX_EXPOSURE_FRAC` | `0.50` | max fraction of equity committed at once |
| `MAX_REQUOTES` | `3` | post-only-cross requote attempts |
| `POLL_SEC` | `5` | market poll interval |
| `BINANCE_LEAD` | `1` | use Binance spot to lean/filter Kalshi side |
| `BINANCE_LEAD_MODE` | `filter` | `filter` (block opposite), `strict` (require agree), `off` |
| `BINANCE_LEAD_WINDOW_SEC` | `20` | lookback window for Binance return |
| `BINANCE_LEAD_PCT` | `0.0008` | min \|return\| to count as up/down lean (~0.08%) |
| `BINANCE_API_BASE` | `https://data-api.binance.vision` | Binance REST base (fallbacks built-in) |

### Binance → Kalshi direction lean (all bot markets)

Background poller reads Binance spot for **every series the bot trades**
(currently `BNBUSDT`, `SOLUSDT`, `XRPUSDT`; also maps BTC/ETH/DOGE if added).
Public REST only — no Binance key. Over the last ~20s it classifies
**up / down / flat**.

Goal: **see Binance before Kalshi finishes adjusting**, then use that intel.

- Logs `binance INTEL` when spot already leaned up/down but Kalshi mid is still stale
- Kalshi **YES** = underlying UP; Kalshi **NO** = underlying DOWN
- **filter** (default): skip new favorites when Binance has a **strong opposite** lean
- **strict**: only enter when Binance lean matches the Kalshi side
- **Unfilled rests:** cancel if Binance flips strongly against the order
- **Filled positions:** log CONFIRM/WARN vs Binance (still hold to settle / spike TP)
- Events: `binance_intel`, `binance_block`, `binance_cancel` in the trade jsonl

```bash
python3 bot/binance_lead.py   # smoke-test the feed alone
```

### Why not BTC?

31-day favorite-maker EV was ~0 on BTC and slightly negative on DOGE — those
books are too efficient. Edge concentrates in thinner alt books (BNB/SOL/XRP;
ZEC/HYPE added as secondary). Override `SERIES` only if you accept flat EV.

### Stop-loss / take-profit

- **Stop:** **off by default**. Live: every settle was a win; both stops lost money.
- **Take-profit:** spike layer on the settle strategy — sell if **mark ≥ 0.98**.
  2× / gain multipliers are **off**. No spike → hold to settlement.
