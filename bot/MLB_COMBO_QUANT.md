# MLB Kalshi Combo Quant

Data-driven analyzer for Kalshi baseball **popular combos** — scores moneylines from pitcher quality, team strength, park, weather, and injuries, then builds **2–3 tickets** aimed at turning a small stake into **4×–20×** ($25 → $100–$500).

## Run

```bash
python3 -u bot/mlb_combo_quant.py --stake 25 --rank-by hitprob
python3 -u bot/mlb_combo_quant.py --stake 25 --rank-by ev --json-out bot/mlb_combo_picks_today.json
python3 -u bot/mlb_combo_quant.py --no-props   # moneylines only
```

## Markets scored

| Kind | Kalshi series |
|------|----------------|
| ML | `KXMLBGAME` |
| Player props | `KXMLBHIT`, `HR`, `RBI`, `TB`, `HRR`, `KS` |
| Game events | `KXMLBTOTAL`, `SPREAD`, `TEAMTOTAL`, `RFI`, `F5` |

## Inputs

| File | Role |
|------|------|
| `bot/mlb_slate_today.json` | Probable pitchers, records, park, weather (update daily) |
| Kalshi public + auth API | Live yes-ask moneylines / props / events |

## Model (v2)

1. **SP quality** — ERA/WHIP z-score vs league, shrunk by innings; TBD/tiny samples cut SP weight  
2. **Team strength** — Laplace win% gap (primary driver)  
3. **Home / park / weather** — small adjustments; roof → weather muted  
4. **Props** — prior by type/threshold, adjusted for opposing SP + park/weather + team ML lean  
5. **Events** — F5 from ML model; spreads/team totals/RFI/totals from SP+env  
6. **Calibration** — blend toward market; same-game mixes get correlation haircut  
7. **Combos** — 2–4 legs across high-prob / $100 / $250 / $500 bands 

## Honesty

Long-shot combos that pay 10–20× lose often. Positive model EV ≠ lock. Confirm lineups, take the combo RFQ only if price ≤ model, and never stake money you can’t lose.
