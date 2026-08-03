# Favorite-maker live runner

Paper/live bot for the near-expiry favorite strategy researched in `research/`.

## $20 test sizing

```
bankroll=$20.00  unit=1.07 contracts/trade
risk/trade=$1.00 (5.0% of bankroll)
max concurrent=4 (locks ~$3.98)
halt if equity <= $10.00
```

Derived from quarter-Kelly on the 31-day backtest (full Kelly ~28% is far too
aggressive given edge uncertainty). Unit auto-resizes as equity changes.

## Run paper (no API keys)

```bash
START_EQUITY=20 MODE=paper python3 bot/runner.py
```

Watches BNB/SOL/XRP/ZEC/HYPE 15m markets by default. In the final 3 minutes,
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
| `SERIES` | `KXBNB15M,KXSOL15M,KXXRP15M,KXZEC15M,KXHYPE15M` | markets to trade |
| `WINDOW_SEC` | `180` | earliest signal window before close |
| `MIN_SECS_LEFT` | `60` | no new entries inside final minute |
| `CONFIRM_POLLS` | `2` | same-side band must hold this many polls |
| `PRICE_LO` / `PRICE_HI` | `0.90` / `0.97` | favorite price band |
| `STOP_LOSS_PCT` | `0.20` | exit if mark falls this fraction under entry |
| `STOP_DISABLE_SECS` | `60` | disable stop in final N seconds (hold to settle) |
| `TAKE_PROFIT_MULT` | `3.0` | exit if mark ≥ entry × mult (per trade) |
| `TAKE_PROFIT_CAP` | `0.99` | max TP price on a $1 binary |
| `MAX_REQUOTES` | `3` | post-only-cross requote attempts |
| `POLL_SEC` | `5` | market poll interval |

### Why not BTC?

31-day favorite-maker EV was ~0 on BTC and slightly negative on DOGE — those
books are too efficient. Edge concentrates in thinner alt books (BNB/SOL/XRP;
ZEC/HYPE added as secondary). Override `SERIES` only if you accept flat EV.

### Stop-loss / take-profit

- **Stop:** mark drops **20% below entry** → IOC exit (disabled in final 60s).
- **Take-profit:** mark reaches **3× entry** → IOC exit. On a $0–$1 binary that
  only fires when entry ≤ 33¢. Our 90–97¢ favorites settle at $1 (~1.05–1.1×),
  so TP is n/a on those trades and we hold to settlement instead.
