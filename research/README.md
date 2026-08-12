# Kalshi 15-minute crypto market research

Empirical study of Kalshi's 15-minute crypto up/down markets (BTC, ETH, SOL,
XRP, DOGE, ZEC, NEAR, HYPE, BNB) using the public market-data API. Sample:
2,874 settled intervals per asset (31 days, Jul 4 - Aug 3 2026), minute-level
candles = ~25,866 markets / ~388k market-minutes.

## Scripts

| script | what it does |
|---|---|
| `fetch_data.py` | downloads settled markets + 1-min candles into `data/*.jsonl` |
| `swing_frequency.py` | standalone: counts intra-interval price flips per asset (fetches its own data) |
| `calibration.py` | settle rate vs contract price, bucketed by price x time remaining |
| `strategies.py` | backtests: cross-asset lead-lag, momentum, near-expiry favorite (taker and maker execution, Kalshi fees) |
| `consistency.py` | day-by-day / per-asset stability of the two surviving edges |
| `daily_pnl.py` | 30-day daily P&L series, positive-day rate, drawdown, half-vs-half decay check |

Run order: `fetch_data.py` first, then any of the analysis scripts.

## Findings (as of the sampled window)

1. **Swing frequency is the same everywhere.** All assets flip through the
   strike ~0.5x per interval (65/35 debounced); ~25% of intervals see a full
   80c->20c round trip. Asset choice doesn't buy you more swings — every
   interval starts at-the-money by construction. Liquidity differs 100x:
   BTC ~$1.6M/interval at 0.8c spread, alts $10-115k at 1-3.4c spreads.

2. **Buying the crashed side of a swing loses.** After a 75c->25c collapse,
   the crashed side recovered less often than its price implied (BTC: paid
   17.1c avg, won 14.3%). Reversal odds are already in the price, and then
   fees/spread take more. Longshots are systematically overpriced.

3. **Cross-asset lead-lag does not work at 1-min granularity.** Buying an
   asset whose contract lags the 8-asset consensus loses ~4.5c/contract as
   taker and ~1c as maker. Divergence is genuine, not staleness.

4. **The mirror of longshot bias is real: near-expiry favorites are cheap.**
   Buying the 90-97c side in minutes 11-13 at mid (maker fill, no fee), over
   the full 31 days: +0.71c/contract on ~314 trades/day, ~95% win rate,
   positive on 24 of 31 days (77%), positive in both halves of the month
   (edge did not decay to zero but weakened: +43.5 first half vs +25.6
   second, in EV units per 1 contract/trade). Daily Sharpe ~0.43; worst
   day -9.6 units; max drawdown 18.8 units (~8 average days). Per-asset EV
   concentrates in BNB (+2.4c), SOL (+1.6c), XRP (+1.5c); BTC/ETH/NEAR are
   ~zero and DOGE slightly negative. Excluding BTC+DOGE: +0.96c/contract,
   daily Sharpe 0.53. As taker the strategy is negative: crossing the
   spread destroys it.

5. **Momentum-following as maker is marginally positive** (+1.0 to +1.6c per
   contract on the 5-day window, ~1.5-1.9 sigma). Weaker evidence than (4).

6. **The bullish-overpricing fade was a regime artifact.** Buying NO at mid
   made +1.4c/contract over Jul 29 - Aug 3 but exactly 0.0c over the full
   31 days (55% positive days, huge variance). A lesson in why multi-week
   validation matters before trading anything.

## Caveats

- Maker fills are modeled as "filled at last close, no fee" — optimistic.
  Real resting orders suffer adverse selection (you get filled more when the
  market is about to move against you). Live paper trading with the actual
  order book is required before trusting the maker EVs.
- 5 days is one regime. Re-run `fetch_data.py` periodically and check
  stability before sizing up.
- Same-window trades across assets share crypto beta; reported standard
  errors understate true variance.
