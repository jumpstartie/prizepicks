# PrizePicks MLB Props Finder

A lightweight static dashboard that ranks the day's PrizePicks MLB player props
so you can quickly find the best over/under plays and build a prop slip. Each
prop is scored by model **edge** (projection vs. the posted line), **matchup
softness**, and **recent form**, then labeled with an Over/Under lean and a
High/Medium/Low confidence tier.

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

`app.js` and `data.js` are loaded by `index.html` in the browser. If you run
`node --check app.js` from another directory, Node will look for the file in
that directory, which causes errors like `Cannot find module '/Users/you/app.js'`.

## What is included

- A value-ranked MLB props board styled like a trading terminal
- Filters for stat type, Over/Under lean, minimum value score, and search
- A per-prop **value score** (0-100) with Over/Under lean and confidence tier
- A **prop slip** builder so you can assemble a PrizePicks-style entry

## How the value score works

For each prop the finder computes:

- `edge = projection - line` (positive leans Over, negative leans Under)
- a bounded bonus when the opponent matchup is soft
- a bonus when the last-10-game average agrees with the lean

These blend into a 0-100 `valueScore`. Scores of 70+ are labeled **High**
confidence, 50-69 **Medium**, and the rest **Low**.

## Connecting real PrizePicks data

The slate lives in `data.js` as the `MLB_PROPS` array. It ships as
representative sample data because `api.prizepicks.com` is protected by a bot
challenge (DataDome / captcha) and cannot be fetched directly from the browser
or a plain server request.

To run against the live board, replace `MLB_PROPS` with a PrizePicks MLB
projections feed that provides, per prop:

- player name and team
- opponent and game time
- stat type (for example Total Bases, Hits, Hits+Runs+RBIs, Pitcher Strikeouts)
- the posted line
- a projection for the stat
- the player's last-10-game average
- the opponent's rank for allowing that stat (1 = toughest, 30 = softest)

Once the array is populated with live values, the ranking, filters, and slip
builder work unchanged.
