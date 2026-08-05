"""Window time-phase helpers for 15m favorite markets.

Research on live closed trades (~186 tickets) showed:

  Phase into window | WR   | Notes
  0–3m / 3–6m       | ~81–88% | Best $ — soft tipped favorites
  6–9m              | ~89% | Still strong
  12–15m (late)     | ~55% | Rich ~92¢ books, thin payoff

Prior-window settle continuation was ~53% (no edge). We log prior
direction for study but do NOT bet it unless PRIOR_DIR_BIAS is enabled,
and even then Binance must not disagree.
"""
from __future__ import annotations

import os
from typing import Optional


WINDOW_LEN_SEC = float(os.environ.get("WINDOW_LEN_SEC", "900"))

# Last N seconds of the window: cut rich late entries (data: weak WR).
LATE_WINDOW_SEC = float(os.environ.get("LATE_WINDOW_SEC", "180"))
LATE_RICH_ENTRY = float(os.environ.get("LATE_RICH_ENTRY", "0.88"))

# Early phase size boost when soft + BN agrees (first ~3m = best live pocket).
EARLY_WINDOW_SEC = float(os.environ.get("EARLY_WINDOW_SEC", "720"))  # secs_left ≥12m
EARLY_SIZE_MULT = float(os.environ.get("EARLY_SIZE_MULT", "1.25"))

# Off by default — prior settle continuation ≈ coin flip in our sample.
PRIOR_DIR_BIAS = os.environ.get("PRIOR_DIR_BIAS", "0").lower() in (
    "1", "true", "yes", "on",
)
PRIOR_DIR_AGREE_MULT = float(os.environ.get("PRIOR_DIR_AGREE_MULT", "1.10"))
PRIOR_DIR_DISAGREE_MULT = float(os.environ.get("PRIOR_DIR_DISAGREE_MULT", "0.50"))


def secs_into_window(secs_left: float, window_len: float = WINDOW_LEN_SEC) -> float:
    return max(0.0, float(window_len) - float(secs_left))


def phase_label(secs_left: float, window_len: float = WINDOW_LEN_SEC) -> str:
    """Coarse 3-minute phase labels for logs / research."""
    into = secs_into_window(secs_left, window_len)
    if into < 180:
        return "0-3m"
    if into < 360:
        return "3-6m"
    if into < 540:
        return "6-9m"
    if into < 720:
        return "9-12m"
    return "12-15m"


def is_late_window(secs_left: float) -> bool:
    return 0 < float(secs_left) <= LATE_WINDOW_SEC


def is_early_window(secs_left: float) -> bool:
    return float(secs_left) >= EARLY_WINDOW_SEC


def late_rich_blocked(entry: float, secs_left: float) -> tuple[bool, str]:
    """True = block. Late + rich favorites were the weak pocket live."""
    if not is_late_window(secs_left):
        return False, ""
    if float(entry) >= LATE_RICH_ENTRY:
        return True, (
            f"late_rich:{phase_label(secs_left)} entry={entry:.2f}"
            f">={LATE_RICH_ENTRY:g} with {secs_left:.0f}s left"
        )
    return False, ""


def phase_size_mult(
    entry: float,
    secs_left: float,
    side: str,
    prior_dir: Optional[str],
    bn_agreed: bool,
) -> tuple[float, str]:
    """Extra size multipliers from time-phase / optional prior-dir bias.

    prior_dir is 'up'|'down' from last settled window of the same series.
    """
    mult = 1.0
    tags: list[str] = []
    soft = float(entry) < 0.85

    if soft and bn_agreed and is_early_window(secs_left) and EARLY_SIZE_MULT > 1:
        mult *= EARLY_SIZE_MULT
        tags.append(f"early×{EARLY_SIZE_MULT:g}")

    if PRIOR_DIR_BIAS and prior_dir in ("up", "down"):
        want = "up" if side == "yes" else "down"
        if prior_dir == want:
            # Only boost when Binance isn't fighting us
            if bn_agreed and PRIOR_DIR_AGREE_MULT != 1.0:
                mult *= PRIOR_DIR_AGREE_MULT
                tags.append(f"prior✓×{PRIOR_DIR_AGREE_MULT:g}")
        else:
            if PRIOR_DIR_DISAGREE_MULT < 1.0:
                mult *= PRIOR_DIR_DISAGREE_MULT
                tags.append(f"prior×{PRIOR_DIR_DISAGREE_MULT:g}")

    return mult, ("+".join(tags) if tags else "")


def settle_direction(side: str, won: bool) -> str:
    """Map our side + outcome to market direction up/down."""
    if side == "yes":
        return "up" if won else "down"
    return "down" if won else "up"
