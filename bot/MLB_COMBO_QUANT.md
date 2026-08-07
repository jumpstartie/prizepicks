# MLB Kalshi Combo Quant

Data-driven analyzer for Kalshi baseball **popular combos** — scores moneylines from pitcher quality, team strength, park, weather, and injuries, then builds **2–3 tickets** aimed at turning a small stake into **4×–20×** ($25 → $100–$500).

## Run

```bash
python3 -u bot/mlb_combo_quant.py --stake 25
python3 -u bot/mlb_combo_quant.py --stake 25 --json-out bot/mlb_combo_picks_today.json
```

## Inputs

| File | Role |
|------|------|
| `bot/mlb_slate_today.json` | Probable pitchers, records, park, weather (update daily) |
| Kalshi public + auth API | Live yes-ask moneylines / props |

## Model (v1)

1. **SP quality** — ERA/WHIP z-score vs league, shrunk by innings; TBD/tiny samples cut SP weight  
2. **Team strength** — Laplace win% gap (primary driver)  
3. **Home / park / weather** — small adjustments; roof → weather muted  
4. **Injuries** — manual notes in slate JSON  
5. **Calibration** — `blend = 0.55*raw + 0.45*market` so edges stay honest  
6. **Combos** — search 2–4 legs into payout bands ≈25¢ / 10¢ / 5¢ for $25→$100/$250/$500  

## Honesty

Long-shot combos that pay 10–20× lose often. Positive model EV ≠ lock. Confirm lineups, take the combo RFQ only if price ≤ model, and never stake money you can’t lose.
