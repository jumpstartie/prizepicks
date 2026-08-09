# Pump.fun quality sniper (Axiom-ready)

Snipe **higher-quality** Pump.fun coins that show a real community signal — Twitter/X profile with followers, a live project website, and Pump.fun chat activity — then paper-trade or execute small live buys with a **Phantom-exported** keypair via PumpPortal’s local transaction API.

## What it does

1. Polls Pump.fun for new / actively traded coins  
2. Hard-filters junk: status-link spam, missing site, NSFW, mcap outside band, low replies  
3. Scores community via `api.fxtwitter.com` (followers/bio/posts) + website HTTP check  
4. Buys only when quality score clears the bar  
5. Exits on take-profit / stop-loss (mcap multiple)  

Optional: set Axiom access/refresh tokens for balance helpers / SDK Pulse later.

## Safety defaults

- **`SNIPER_MODE=paper`** — no real trades  
- Small `BUY_SOL` for live tests  
- Secrets stay in `secrets/` (gitignored)  
- Never paste your Phantom seed or private key into chat  

Memecoins are extremely high risk. This is tooling, not financial advice.

## Setup

```bash
pip install -r sniper/requirements.txt
cp sniper/secrets.env.example secrets/sniper.env
```

### Hook up Phantom

1. In Phantom: **Settings → Security & Privacy → Export Private Key** (prefer a **fresh trading wallet**, not your main stash)  
2. Put the base58 key in either:
   - `secrets/phantom.key` (file containing only the key), or  
   - `PHANTOM_PRIVATE_KEY=...` inside `secrets/sniper.env`  
3. Verify:

```bash
python3 -u sniper/connect_wallet.py
```

4. Send a **small** SOL amount from Phantom to the printed address for live tests.

### Optional Axiom

In `secrets/sniper.env`:

```env
AXIOM_ACCESS_TOKEN=...
AXIOM_REFRESH_TOKEN=...
```

Discovery works without Axiom (Pump.fun public feed).

## Run

Paper (recommended first):

```bash
bash sniper/start_paper.sh
# single scan:
python3 -u sniper/runner.py --once --verbose
```

Live (real SOL):

```bash
# edit secrets/sniper.env → SNIPER_MODE=live, BUY_SOL=0.02
bash sniper/start_live.sh
```

## Quality gates (env)

| Var | Default | Meaning |
|---|---|---|
| `MIN_TWITTER_FOLLOWERS` | 50 | Min X followers on a **profile** (not a status link) |
| `REQUIRE_WEBSITE` | 1 | Must have a live non-aggregator website |
| `MIN_PUMP_REPLIES` | 5 | Pump.fun chat activity |
| `MIN_USD_MCAP` / `MAX_USD_MCAP` | 8k / 250k | Avoid dust + late chase |
| `MIN_QUALITY_SCORE` | 55 | Combined community score 0–100 |
| `BUY_SOL` | 0.05 | Size per entry |
| `TAKE_PROFIT_X` / `STOP_LOSS_X` | 2.0 / 0.55 | Exit multiples vs entry mcap |

## Files

- `runner.py` — main loop  
- `community.py` — Twitter/website scoring  
- `pumpfun_client.py` — Pump.fun feed  
- `trader.py` — paper + PumpPortal live  
- `wallet.py` — Phantom key load  
- `axiom_client.py` — optional Axiom bridge  

State: `sniper/state.json`, fills: `sniper/trades.jsonl`
