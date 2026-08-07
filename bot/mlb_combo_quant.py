#!/usr/bin/env python3
"""Kalshi MLB popular-combo quant analyzer.

Scores today's moneyline legs from pitcher quality, team strength, park,
weather, and injuries; then builds 2–3 combos aimed at $25 → $100–$500
payout bands (4×–20×).

Usage:
  python3 -u bot/mlb_combo_quant.py
  python3 -u bot/mlb_combo_quant.py --stake 25 --date 2026-08-07
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PUBLIC_BASE = "https://api.elections.kalshi.com/trade-api/v2"
SLATE_PATH = Path(__file__).with_name("mlb_slate_today.json")

# Rough league-average SP anchors for z-scores
LG_ERA, LG_WHIP = 4.10, 1.28


def _load_secrets() -> None:
    env = ROOT / "secrets" / "env.sh"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or not line.startswith("export "):
            continue
        k, v = line[len("export ") :].split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))


def _http_get(url: str) -> dict:
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "mlb-combo-quant/1.0"}
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _wpct(rec: list[int]) -> float:
    w, l = rec[0], rec[1]
    n = w + l
    return (w + 1) / (n + 2) if n else 0.5  # Laplace


def _sp_quality(sp: dict) -> float:
    """Higher = better pitcher. Blend ERA/WHIP with sample-size shrink."""
    era = float(sp.get("era") or LG_ERA)
    whip = float(sp.get("whip") or LG_WHIP)
    ip = max(float(sp.get("ip") or 1.0), 1.0)
    name = str(sp.get("name") or "")
    if name.upper() == "TBD":
        return 0.0  # unknown → neutral-to-slight negative in matchup
    # z vs league; shrink toward 0 when IP light
    z_era = (LG_ERA - era) / 1.15
    z_whip = (LG_WHIP - whip) / 0.22
    shrink = min(1.0, ip / 80.0)
    return shrink * (0.65 * z_era + 0.35 * z_whip)


def _weather_offense_boost(game: dict) -> float:
    """Positive → more runs environment (helps favorites less than hit props)."""
    roof = str(game.get("roof") or "open").lower()
    if roof in ("retractable", "dome", "closed"):
        return 0.0  # roof kills weather edge
    temp = float(game.get("temp_f") or 75)
    wind = float(game.get("wind_mph") or 0)
    precip = float(game.get("precip_pct") or 0)
    park = float(game.get("park_run_factor") or 1.0)
    boost = 0.0
    if temp >= 85:
        boost += 0.08
    elif temp <= 60:
        boost -= 0.06
    if wind >= 12:
        boost += 0.04  # coarse; direction unknown
    if precip >= 40:
        boost -= 0.10
    boost += (park - 1.0) * 0.5
    return boost


@dataclass
class Leg:
    team: str
    event_key: str
    label: str
    market_price: float
    model_prob: float
    edge: float
    ticker: str
    reasons: list[str] = field(default_factory=list)
    kind: str = "ml"  # ml | prop

    @property
    def ev_per_dollar(self) -> float:
        """Expected $ profit per $1 risked at market_price if model_prob true."""
        p = self.market_price
        if p <= 0 or p >= 1:
            return -1.0
        return self.model_prob / p - 1.0


@dataclass
class Combo:
    legs: list[Leg]
    market_price: float
    model_prob: float
    stake: float
    target_band: str

    @property
    def payout_if_hit(self) -> float:
        return self.stake / self.market_price if self.market_price > 0 else 0.0

    @property
    def profit_if_hit(self) -> float:
        return self.payout_if_hit - self.stake

    @property
    def expected_profit(self) -> float:
        # EV = model_prob * payout - stake
        return self.model_prob * self.payout_if_hit - self.stake

    @property
    def edge(self) -> float:
        if self.market_price <= 0:
            return -1.0
        return self.model_prob / self.market_price - 1.0


def fetch_ml_prices(date_tag: str) -> dict[str, dict[str, Any]]:
    """Map event_key -> {team: {ticker, ask, bid, last}}."""
    _load_secrets()
    try:
        from bot.kalshi_client import KalshiClient
        client: Any = KalshiClient()
    except Exception:
        client = None

    events = _http_get(
        f"{PUBLIC_BASE}/events?status=open&limit=200&series_ticker=KXMLBGAME"
    ).get("events") or []
    out: dict[str, dict[str, Any]] = {}
    for e in events:
        et = e.get("event_ticker") or ""
        if date_tag not in et:
            continue
        # KXMLBGAME-26AUG071940MINMIL → MINMIL (strip HHMM)
        suffix = et.split(date_tag)[-1]
        key = re.sub(r"^\d{4}", "", suffix)
        mk = _http_get(
            f"{PUBLIC_BASE}/markets?event_ticker={et}&limit=20"
        ).get("markets") or []
        out[key] = {}
        for m in mk:
            ticker = m["ticker"]
            team = ticker.rsplit("-", 1)[-1]
            bid = ask = last = None
            if client is not None:
                try:
                    mm = client.market(ticker)
                    if isinstance(mm, dict) and "market" in mm:
                        mm = mm["market"]
                    bid = float(mm.get("yes_bid_dollars") or 0) or None
                    ask = float(mm.get("yes_ask_dollars") or 0) or None
                    last = float(mm.get("last_price_dollars") or 0) or None
                except Exception:
                    pass
            price = ask or last or bid
            if price is None:
                continue
            out[key][team] = {
                "ticker": ticker,
                "bid": bid,
                "ask": ask,
                "last": last,
                "price": float(price),
                "subtitle": m.get("yes_sub_title") or team,
            }
    return out


def fetch_prop_price(ticker: str) -> Optional[float]:
    _load_secrets()
    try:
        from bot.kalshi_client import KalshiClient
        mm = KalshiClient().market(ticker)
        if isinstance(mm, dict) and "market" in mm:
            mm = mm["market"]
        for k in ("yes_ask_dollars", "last_price_dollars", "yes_bid_dollars"):
            v = mm.get(k)
            if v is not None:
                return float(v)
    except Exception:
        return None
    return None


def model_home_win_prob(game: dict) -> tuple[float, list[str]]:
    reasons: list[str] = []
    home_sp_q = _sp_quality(game["home_sp"])
    away_sp_q = _sp_quality(game["away_sp"])
    sp_gap = home_sp_q - away_sp_q
    reasons.append(
        f"SP {game['home_sp']['name']}({game['home_sp']['era']:.2f}) vs "
        f"{game['away_sp']['name']}({game['away_sp']['era']:.2f}) gap={sp_gap:+.2f}"
    )

    h_wp = _wpct(game["home_record"])
    a_wp = _wpct(game["away_record"])
    team_gap = (h_wp - a_wp) * 4.0  # scale
    reasons.append(
        f"records {game['home']}:{game['home_record'][0]}-{game['home_record'][1]} "
        f"vs {game['away']}:{game['away_record'][0]}-{game['away_record'][1]}"
    )

    home_adv = 0.035  # ~53.5% baseline home
    wx = _weather_offense_boost(game)
    # weather slightly helps better offense; use team_gap sign
    wx_term = 0.15 * wx * (1.0 if team_gap >= 0 else -0.5)

    injury = str(game.get("injury_notes") or "")
    inj = 0.0
    if injury:
        # crude: if note mentions home team abbreviation pain
        if game["home"] in injury or "NYY" in injury and game["home"] == "NYY":
            inj -= 0.06
            reasons.append(f"injury drag: {injury[:80]}")
        if game["away"] in injury:
            inj += 0.04

    # TBD starter penalty on that side
    if str(game["home_sp"].get("name")).upper() == "TBD":
        inj -= 0.03
        reasons.append("home SP TBD — uncertainty penalty")
    if str(game["away_sp"].get("name")).upper() == "TBD":
        inj += 0.03
        reasons.append("away SP TBD — helps home")

    # Cap SP influence when either side is TBD / tiny sample
    if str(game["home_sp"].get("name")).upper() == "TBD" or float(
        game["home_sp"].get("ip") or 0
    ) < 30:
        sp_gap *= 0.45
        reasons.append("home SP sample/TBD — shrunk SP gap")
    if str(game["away_sp"].get("name")).upper() == "TBD" or float(
        game["away_sp"].get("ip") or 0
    ) < 30:
        sp_gap *= 0.45
        reasons.append("away SP sample/TBD — shrunk SP gap")

    logit = (
        math.log(0.54 / 0.46)  # home base
        + 0.45 * sp_gap
        + 1.15 * team_gap  # season strength weighs heavier than small SP samples
        + home_adv * 0.5
        + wx_term
        + inj * 4.0
    )
    p_home = _sigmoid(logit)
    p_home = min(0.88, max(0.12, p_home))
    return p_home, reasons


def score_legs(slate: dict, prices: dict[str, dict[str, Any]]) -> list[Leg]:
    legs: list[Leg] = []
    for game in slate["games"]:
        key = game["event_key"]
        book = prices.get(key) or {}
        if len(book) < 2:
            continue
        p_home_raw, reasons = model_home_win_prob(game)
        for side, team, p_raw in (
            ("home", game["home"], p_home_raw),
            ("away", game["away"], 1.0 - p_home_raw),
        ):
            # Kalshi team codes sometimes ATH vs A's — try aliases
            info = book.get(team)
            if info is None:
                aliases = {
                    "LAA": ["LAA", "AA"],
                    "CWS": ["CWS", "CHW"],
                    "ATH": ["ATH", "OAK"],
                    "AZ": ["AZ", "ARI"],
                }
                for alt in book:
                    if alt == team or team.startswith(alt) or alt.startswith(team):
                        info = book[alt]
                        break
                    if team in aliases and alt in aliases[team]:
                        info = book[alt]
                        break
            if info is None:
                continue
            mkt = float(info["price"])
            # Blend raw model toward market to avoid overconfident edges
            p_model = 0.55 * p_raw + 0.45 * mkt
            p_model = min(0.90, max(0.10, p_model))
            edge = p_model / mkt - 1.0 if mkt > 0 else -1.0
            legs.append(
                Leg(
                    team=team,
                    event_key=key,
                    label=f"{team} ML ({info.get('subtitle') or team})",
                    market_price=mkt,
                    model_prob=p_model,
                    edge=edge,
                    ticker=info["ticker"],
                    reasons=list(reasons)
                    + [
                        f"raw={p_raw:.1%} blend={p_model:.1%} mkt={mkt:.0%} "
                        f"edge={edge:+.1%}"
                    ],
                    kind="ml",
                )
            )

    # Optional props — blend prior with live ask; require ML lean same team
    ml_by_team = {lg.team: lg for lg in legs if lg.kind == "ml"}
    for prop in slate.get("prop_legs") or []:
        ticker = prop["ticker_hint"]
        ask = fetch_prop_price(ticker)
        if ask is None or ask <= 0:
            continue
        prior = float(prop.get("prior") or ask)
        # shrink prior toward market; bump if team ML has edge
        team = prop["team"]
        bump = 0.0
        if team in ml_by_team and ml_by_team[team].edge > 0.03:
            bump = 0.02
        model = min(0.85, max(0.05, 0.55 * prior + 0.45 * ask + bump))
        edge = model / ask - 1.0
        legs.append(
            Leg(
                team=team,
                event_key=prop["event_key"],
                label=prop["label"],
                market_price=ask,
                model_prob=model,
                edge=edge,
                ticker=ticker,
                reasons=[
                    f"prop prior={prior:.0%} live={ask:.0%} model={model:.1%} edge={edge:+.1%}"
                ],
                kind="prop",
            )
        )
    return legs


def _combo_ok(legs: list[Leg]) -> bool:
    """No two ML from same game; at most one prop; prefer multi-game structure."""
    events_ml = [lg.event_key for lg in legs if lg.kind == "ml"]
    if len(events_ml) != len(set(events_ml)):
        return False
    props = [lg for lg in legs if lg.kind == "prop"]
    if len(props) > 1:
        return False  # correlated prop stacks are lottery tickets, not quant core
    if props and props[0].event_key not in events_ml and len(events_ml) >= 1:
        # allow orphan prop only in pure longshot searches — block here
        return False
    return True


def build_combos(
    legs: list[Leg],
    stake: float,
    max_legs: int = 4,
) -> list[Combo]:
    """Search positive-edge / high-score combos in payout bands."""
    # Core pool: ML with model interest; allow props separately
    mls = [lg for lg in legs if lg.kind == "ml" and 0.20 <= lg.market_price <= 0.78]
    mls.sort(key=lambda x: (x.edge, x.model_prob), reverse=True)
    # Keep top edges + a few chalk favorites for payout construction
    chalk = sorted(
        [lg for lg in mls if lg.market_price >= 0.58],
        key=lambda x: x.model_prob,
        reverse=True,
    )[:8]
    edge_pool = mls[:14]
    pool_map = {lg.ticker: lg for lg in edge_pool + chalk}
    pool = list(pool_map.values())
    props = [lg for lg in legs if lg.kind == "prop" and lg.edge > -0.02][:4]

    bands = [
        ("$100 (4×)", 0.18, 0.32),
        ("$250 (10×)", 0.07, 0.15),
        ("$500 (20×)", 0.035, 0.075),
    ]
    scored: list[Combo] = []

    def consider(cl: list[Leg]) -> None:
        if not _combo_ok(cl):
            return
        events = [x.event_key for x in cl]
        corr = 0.88 if len(events) != len(set(events)) else 1.0
        mkt = model = 1.0
        for lg in cl:
            mkt *= lg.market_price
            model *= lg.model_prob
        model *= corr
        if mkt < 0.03 or mkt > 0.55:
            return
        band = "other"
        for name, lo, hi in bands:
            if lo <= mkt <= hi:
                band = name
                break
        c = Combo(cl, mkt, model, stake, band)
        # Require mostly non-terrible edge for "other"; bands can be moonshots
        if band == "other" and c.edge < 0:
            return
        if c.edge < -0.25:
            return
        scored.append(c)

    for n in range(2, max_legs + 1):
        for combo_legs in combinations(pool, n):
            consider(list(combo_legs))
        # ML stack + one prop for longer bands
        if props and n >= 3:
            for combo_legs in combinations(pool, n - 1):
                for pr in props:
                    consider(list(combo_legs) + [pr])

    def rank_key(c: Combo) -> tuple:
        ml_n = sum(1 for lg in c.legs if lg.kind == "ml")
        band_bonus = 0.0 if c.target_band == "other" else 2.0
        return (band_bonus, ml_n, c.expected_profit, c.edge)

    scored.sort(key=rank_key, reverse=True)

    picks: list[Combo] = []
    used_labels: set[str] = set()
    for band, _, _ in bands:
        for c in scored:
            if c.target_band != band:
                continue
            sig = "|".join(sorted(lg.label for lg in c.legs))
            if sig in used_labels:
                continue
            picks.append(c)
            used_labels.add(sig)
            break
    for c in scored:
        if len(picks) >= 3:
            break
        sig = "|".join(sorted(lg.label for lg in c.legs))
        if sig in used_labels:
            continue
        picks.append(c)
        used_labels.add(sig)
    return picks[:3]


def print_report(legs: list[Leg], combos: list[Combo], stake: float) -> None:
    print("=" * 72)
    print("MLB KALSHI COMBO QUANT — data-driven popular combo board")
    print("=" * 72)
    print(f"\nStake: ${stake:.0f}   Goal: turn into $100–$500+ on 2–3 combo tickets\n")

    print("TOP +EV / QUALITY ML LEGS")
    print("-" * 72)
    mls = sorted([lg for lg in legs if lg.kind == "ml"], key=lambda x: x.edge, reverse=True)
    for lg in mls[:10]:
        print(
            f"  {lg.team:4}  mkt={lg.market_price:.0%}  model={lg.model_prob:.0%}  "
            f"edge={lg.edge:+.0%}  [{lg.event_key}]"
        )
        print(f"         {lg.reasons[-1]}")

    props = [lg for lg in legs if lg.kind == "prop"]
    if props:
        print("\nPROP LEGS")
        print("-" * 72)
        for lg in sorted(props, key=lambda x: x.edge, reverse=True)[:6]:
            print(
                f"  {lg.label:22} mkt={lg.market_price:.0%} model={lg.model_prob:.0%} "
                f"edge={lg.edge:+.0%}"
            )

    print("\n" + "=" * 72)
    print("BEST 2–3 COMBOS FOR $25 → $100–$500 BANDS")
    print("=" * 72)
    if not combos:
        print("No combos found in target bands — widen search or refresh slate.")
        return

    for i, c in enumerate(combos, 1):
        print(f"\n#{i}  [{c.target_band}]")
        print(f"  Legs: {' + '.join(lg.label for lg in c.legs)}")
        print(
            f"  Combo ask≈{c.market_price:.1%}   model≈{c.model_prob:.1%}   "
            f"edge={c.edge:+.0%}"
        )
        print(
            f"  ${stake:.0f} → payout ${c.payout_if_hit:.0f}  "
            f"(profit ${c.profit_if_hit:.0f} if hit)   "
            f"E[profit]=${c.expected_profit:+.2f}"
        )
        for lg in c.legs:
            print(f"    • {lg.label}: {lg.reasons[-1]}")
        print(f"  Tickers: {', '.join(lg.ticker for lg in c.legs)}")

    print("\n" + "-" * 72)
    print(
        "Reality check: $25→$500 needs ~5¢ combo (long shot). Model edge ≠ lock. "
        "Confirm lineups, get combo RFQ, size only what you can lose."
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Kalshi MLB combo quant analyzer")
    ap.add_argument("--stake", type=float, default=25.0)
    ap.add_argument("--date-tag", default="26AUG07", help="Kalshi date fragment in ticker")
    ap.add_argument("--slate", type=Path, default=SLATE_PATH)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    slate = json.loads(args.slate.read_text())
    print(f"Loading Kalshi ML prices for {args.date_tag}...", flush=True)
    prices = fetch_ml_prices(args.date_tag)
    print(f"  priced events: {len(prices)}", flush=True)
    legs = score_legs(slate, prices)
    combos = build_combos(legs, stake=args.stake)
    print_report(legs, combos, args.stake)

    if args.json_out:
        payload = {
            "stake": args.stake,
            "legs": [
                {
                    "team": lg.team,
                    "event_key": lg.event_key,
                    "label": lg.label,
                    "market_price": lg.market_price,
                    "model_prob": lg.model_prob,
                    "edge": lg.edge,
                    "ticker": lg.ticker,
                    "kind": lg.kind,
                }
                for lg in legs
            ],
            "combos": [
                {
                    "band": c.target_band,
                    "market_price": c.market_price,
                    "model_prob": c.model_prob,
                    "edge": c.edge,
                    "payout_if_hit": c.payout_if_hit,
                    "profit_if_hit": c.profit_if_hit,
                    "expected_profit": c.expected_profit,
                    "legs": [lg.label for lg in c.legs],
                    "tickers": [lg.ticker for lg in c.legs],
                }
                for c in combos
            ],
        }
        args.json_out.write_text(json.dumps(payload, indent=2))
        print(f"\nWrote {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
