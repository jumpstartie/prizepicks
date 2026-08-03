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

Watches BNB/SOL/XRP 15m markets by default. In the final 3 minutes, if either
side is at 90–97¢, rests a simulated maker order at the touch. Settles against
the real Kalshi result. State in `bot/state.json`, trade log in `bot/trades.jsonl`.

`PAPER_FILL=backtest` (recommended for the $20 test) fills on the next poll,
matching the research mid-fill assumption. `PAPER_FILL=touch` (default if unset
in code path — pass explicitly) only fills when a new trade prints at the
touch or the book crosses you — much closer to live maker reality, and much
sparser, especially on the NO side.

## Run live

1. Create an API key at https://kalshi.com/account/profile
2. Fund the account with $20
3. Export credentials and start:

```bash
export KALSHI_API_KEY_ID='...'
export KALSHI_PRIVATE_KEY_PATH=/path/to/kalshi.key   # or KALSHI_PRIVATE_KEY='PEM...'
START_EQUITY=20 MODE=live python3 bot/runner.py
```

Use `KALSHI_DEMO=1` against the demo environment first if you want.

## Config env vars

| var | default | meaning |
|---|---|---|
| `START_EQUITY` | `20` | starting bankroll for sizing / halt |
| `MODE` | `paper` | `paper` or `live` |
| `SERIES` | `KXBNB15M,KXSOL15M,KXXRP15M` | comma-separated series |
| `WINDOW_SEC` | `180` | signal window before close |
| `PRICE_LO` / `PRICE_HI` | `0.90` / `0.97` | favorite price band |
| `POLL_SEC` | `5` | market poll interval |
