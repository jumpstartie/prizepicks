# Favorite-maker live runner

Paper/live bot for the near-expiry favorite strategy researched in `research/`.

## Quant stack (current)

1. **Instrument** — every signal/fill/settle logs mid, spread, secs left, Binance lean, risk %
2. **Fast lead** — Binance trade WebSocket + vol-adjusted threshold + Coinbase confirm
3. **Mispricing gates** — skip too-rich entries / wide spreads unless Binance agrees
4. **Edge sizing (#5)** — fractional Kelly from live WR/EV; cut when edge decays; halt-buffer cap
5. **Markout report** — `python3 bot/markout_report.py`

## $20 test sizing (edge-aware)

```
bankroll≈$21
risk/trade ≈ 8–22% of equity (EDGE_SIZING), halt-capped to survive ~3 losses to $15
stop-loss OFF — hold favorites to settlement / spike TP ≥ 0.98
binance lead ON (ws + filter)
```

`EDGE_SIZING=1` (default) sets risk from recent settles (quarter-Kelly, shrunk to prior),
floored at `RISK_FRAC_MIN` and capped at `RISK_FRAC_MAX`. Negative live EV → min size.

## Run paper (no API keys)

```bash
pip3 install websocket-client   # for Binance trade stream
START_EQUITY=20 MODE=paper python3 bot/runner.py
```

## Run live

```bash
export KALSHI_API_KEY_ID='...'
export KALSHI_PRIVATE_KEY_PATH=/path/to/kalshi.key
START_EQUITY=20 MODE=live \
  EDGE_SIZING=1 RISK_FRACTION=0.20 \
  BINANCE_LEAD=1 BINANCE_WS=1 COINBASE_CONFIRM=1 \
  python3 -u bot/runner.py
```

## Config env vars

| var | default | meaning |
|---|---|---|
| `START_EQUITY` | `20` | starting bankroll for sizing / halt |
| `MODE` | `paper` | `paper` or `live` |
| `SERIES` | `KXBNB15M,KXSOL15M,KXXRP15M` | core markets |
| `WINDOW_SEC` | `180` | earliest signal window before close |
| `MIN_SECS_LEFT` | `60` | no new entries inside final minute |
| `CONFIRM_POLLS` | `2` | same-side band must hold this many polls |
| `PRICE_LO` / `PRICE_HI` | `0.90` / `0.97` | favorite price band |
| `SKIP_ENTRY_RICH` | `0.965` | skip entries ≥ this unless Binance agrees |
| `MAX_SPREAD` | `0.04` | skip if yes ask−bid wider than this |
| `STOP_LOSS_PCT` | `0` | stop-loss disabled |
| `TAKE_PROFIT_ABS` | `0.98` | spike exit if mark ≥ this |
| `HALT_FLOOR` | `15.0` | stop the run if equity ≤ this ($) |
| `RISK_FRACTION` | `0.20` | base risk when blending / EDGE_SIZING off |
| `EDGE_SIZING` | `1` | dynamic risk from live edge |
| `RISK_FRAC_MIN` / `MAX` | `0.08` / `0.22` | hard band for edge sizer |
| `EDGE_LOOKBACK` | `30` | recent filled closes for WR/EV |
| `EDGE_MIN_SAMPLES` | `8` | below this, blend toward base risk |
| `EDGE_KELLY_FRAC` | `0.25` | fraction of full Kelly to use |
| `HALT_LOSS_BUFFER` | `3` | size so ~N full losses stay above halt |
| `BINANCE_LEAD` | `1` | enable lead intel/filter |
| `BINANCE_LEAD_MODE` | `filter` | `filter` / `strict` / `off` |
| `BINANCE_WS` | `1` | use Binance trade WebSocket |
| `BINANCE_LEAD_WINDOW_SEC` | `15` | lookback for spot return |
| `BINANCE_LEAD_PCT` | `0.0008` | base lean threshold |
| `BINANCE_LEAD_VOL_MULT` | `1.25` | vol-adjust multiplier |
| `COINBASE_CONFIRM` | `1` | tag leans with Coinbase same-way check |

### Edge sizing (#5)

```
risk ≈ clamp( quarter_Kelly(live WR, avg win/loss), MIN, MAX )
       then min(risk, room_to_halt / (HALT_LOSS_BUFFER * equity))
```

- Live WR is shrunk toward a 93% prior until enough samples
- `ev < 0` or `WR < avg entry` → cut to `RISK_FRAC_MIN`
- Bankroll up + stable positive EV → risk can rise toward MAX

### Binance early intel

- WebSocket trades on BNB/SOL/XRP (REST fallback)
- `binance INTEL` when spot leaned but Kalshi mid still stale
- Filter/cancel when Binance strongly opposes a favorite
- Coinbase confirm tagged on leans (`cb✓` / `cb×` in status)

```bash
python3 bot/binance_lead.py
python3 bot/markout_report.py bot/trades_live.jsonl
```

### Stop-loss / take-profit

- **Stop:** off — settle path was +EV; stops caused live losses
- **Take-profit:** spike at **mark ≥ 0.98**; else hold to settlement
