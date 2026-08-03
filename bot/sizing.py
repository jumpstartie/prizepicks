"""Unit sizing for the near-expiry favorite maker strategy.

With a tiny bankroll the binding constraints are:
  - historical max drawdown at 1 contract/trade was ~$19 over 31 days
  - each losing trade costs ~$0.93 (buy ~93c, settle 0)
  - full Kelly for a 95%-win / 7c-payoff binary is ~28% of bankroll — far
    too aggressive given edge uncertainty and adverse selection
  - use quarter-Kelly (~7% of bankroll risked per trade), floored at the
    exchange minimum of 0.01 contracts and capped so concurrent exposure
    never exceeds MAX_EXPOSURE_FRAC of equity
"""
from __future__ import annotations

import math

# Strategy assumptions from the 31-day backtest
AVG_ENTRY = 0.93
AVG_WIN_PAYOFF = 1.0 - AVG_ENTRY  # ~0.07
LOSS_PER_CONTRACT = AVG_ENTRY     # lose the entry price on a loser
WIN_RATE = 0.95

# Risk controls for a $20 test account
RISK_FRACTION = 0.05              # ~quarter-Kelly; 5% of equity risked per trade
MAX_EXPOSURE_FRAC = 0.20          # max capital locked in open positions
HALT_EQUITY_FRAC = 0.50           # stop trading if equity falls to 50% of start
MIN_CONTRACTS = 0.01              # Kalshi minimum
CONTRACT_STEP = 0.01


def contracts_for_equity(equity: float, entry: float = AVG_ENTRY) -> float:
    """Contracts to buy on the next signal given current equity."""
    if equity <= 0 or entry <= 0:
        return 0.0
    risk_budget = equity * RISK_FRACTION
    raw = risk_budget / entry
    # Floor to exchange step; never below min if we can afford one min lot
    stepped = math.floor(raw / CONTRACT_STEP) * CONTRACT_STEP
    if stepped < MIN_CONTRACTS:
        return MIN_CONTRACTS if equity >= entry * MIN_CONTRACTS else 0.0
    return round(stepped, 2)


def max_concurrent(equity: float, entry: float = AVG_ENTRY) -> int:
    """Max simultaneous open positions at the current unit size."""
    unit = contracts_for_equity(equity, entry)
    if unit <= 0:
        return 0
    cap = equity * MAX_EXPOSURE_FRAC
    return max(1, int(cap // (entry * unit)))


def should_halt(equity: float, start_equity: float) -> bool:
    return equity <= start_equity * HALT_EQUITY_FRAC


def describe(start_equity: float = 20.0) -> str:
    unit = contracts_for_equity(start_equity)
    conc = max_concurrent(start_equity)
    risk = unit * LOSS_PER_CONTRACT
    locked = conc * unit * AVG_ENTRY
    return (
        f"bankroll=${start_equity:.2f}  unit={unit:.2f} contracts/trade  "
        f"risk/trade=${risk:.2f} ({100*risk/start_equity:.1f}% of bankroll)  "
        f"max concurrent={conc} (locks ~${locked:.2f})  "
        f"halt if equity <= ${start_equity*HALT_EQUITY_FRAC:.2f}"
    )


if __name__ == "__main__":
    for e in (20.0, 50.0, 100.0, 500.0):
        print(describe(e))
