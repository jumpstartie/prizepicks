# Polymarket Copy Trade Scout

A lightweight static dashboard for screening Polymarket wallets before adding
them to a copy-trading watchlist. It mirrors the terminal-style leaderboard in
the reference with win rate, trade count, 15-day max drawdown, risk, flags, and
a calculated copy score.

## Run locally

First change into the repository folder on your machine:

```bash
cd path/to/prizepicks
```

Then start the static site:

```bash
npm start
```

Then open <http://localhost:4173>.

You can also run it without npm:

```bash
python3 -m http.server 4173
```

## Validate the JavaScript

From the repository root:

```bash
npm test
```

`app.js` is loaded by `index.html` in the browser. If you run
`node --check app.js` from another directory, Node will look for `app.js` in
that directory, which causes errors like `Cannot find module '/Users/brian/app.js'`.

## What is included

- Top-wallet leaderboard styled like a trading terminal
- Filters for minimum win rate, maximum risk, minimum trades, and search
- Risk and behavior flags (`clean`, `posVol`, `susWR`)
- Copy-score ranking that rewards trade depth and win edge while penalizing
  drawdown, risk, and suspicious flags
- In-page watchlist toggles for candidate copy-trade wallets

## Connecting real data

The sample data lives in `app.js` as the `wallets` array. Replace that array
with a Polymarket analytics feed that provides:

- wallet address
- win rate over the target scan window
- trade count
- max drawdown
- risk tier
- wallet behavior flags
