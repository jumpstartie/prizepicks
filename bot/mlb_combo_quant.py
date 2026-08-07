#!/usr/bin/env python3
"""Kalshi MLB popular-combo quant analyzer (ML + player props + game events).

Scores moneylines, hits/HR/RBI/HRR/K props, totals, spreads, F5, and RFI
from pitcher quality, team strength, park, and weather. Builds 2–3 combos
for $25 → $100–$500 bands and can rank by hit probability.

Usage:
  python3 -u bot/mlb_combo_quant.py --stake 25
  python3 -u bot/mlb_combo_quant.py --stake 25 --rank-by hitprob --props
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PUBLIC_BASE = "https://api.elections.kalshi.com/trade-api/v2"
SLATE_PATH = Path(__file__).with_name("mlb_slate_today.json")

LG_ERA, LG_WHIP = 4.10, 1.28

# Series we pull for props / game events
PROP_SERIES = (
    "KXMLBHIT",
    "KXMLBHR",
    "KXMLBRBI",
    "KXMLBTB",
    "KXMLBHRR",
    "KXMLBKS",
)
EVENT_SERIES = (
    "KXMLBTOTAL",
    "KXMLBSPREAD",
    "KXMLBTEAMTOTAL",
    "KXMLBRFI",
    "KXMLBF5",
)

# Baseline priors by market family / threshold (before park/SP adjust)
PROP_PRIORS = {
    ("HIT", 1): 0.68,
    ("HIT", 2): 0.28,
    ("HR", 1): 0.18,
    ("RBI", 1): 0.36,
    ("TB", 2): 0.42,
    ("HRR", 1): 0.72,
    ("HRR", 2): 0.50,
    ("KS", 3): 0.78,
    ("KS", 4): 0.62,
    ("KS", 5): 0.48,
    ("KS", 6): 0.35,
}


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
        url, headers={"Accept": "application/json", "User-Agent": "mlb-combo-quant/2.0"}
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _wpct(rec: list[int]) -> float:
    w, l = rec[0], rec[1]
    n = w + l
    return (w + 1) / (n + 2) if n else 0.5


def _sp_quality(sp: dict) -> float:
    era = float(sp.get("era") or LG_ERA)
    whip = float(sp.get("whip") or LG_WHIP)
    ip = max(float(sp.get("ip") or 1.0), 1.0)
    if str(sp.get("name") or "").upper() == "TBD":
        return 0.0
    z_era = (LG_ERA - era) / 1.15
    z_whip = (LG_WHIP - whip) / 0.22
    shrink = min(1.0, ip / 80.0)
    return shrink * (0.65 * z_era + 0.35 * z_whip)


def _weather_offense_boost(game: dict) -> float:
    roof = str(game.get("roof") or "open").lower()
    if roof in ("retractable", "dome", "closed"):
        return 0.0
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
        boost += 0.04
    if precip >= 40:
        boost -= 0.10
    boost += (park - 1.0) * 0.5
    return boost


class PriceCache:
    def __init__(self) -> None:
        _load_secrets()
        self._client: Any = None
        try:
            from bot.kalshi_client import KalshiClient
            self._client = KalshiClient()
        except Exception:
            self._client = None
        self._cache: dict[str, Optional[float]] = {}

    def price(self, ticker: str) -> Optional[float]:
        if ticker in self._cache:
            return self._cache[ticker]
        p: Optional[float] = None
        if self._client is not None:
            try:
                mm = self._client.market(ticker)
                if isinstance(mm, dict) and "market" in mm:
                    mm = mm["market"]
                for k in ("yes_ask_dollars", "last_price_dollars", "yes_bid_dollars"):
                    if mm.get(k) is not None:
                        p = float(mm[k])
                        break
            except Exception:
                p = None
        self._cache[ticker] = p
        return p


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
    kind: str = "ml"  # ml | prop | event
    family: str = "ML"
    threshold: int = 0
    player: str = ""

    @property
    def ev_per_dollar(self) -> float:
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
        return self.model_prob * self.payout_if_hit - self.stake

    @property
    def edge(self) -> float:
        if self.market_price <= 0:
            return -1.0
        return self.model_prob / self.market_price - 1.0


def _event_key_from_ticker(ticker: str, date_tag: str) -> str:
    """KXMLBHIT-26AUG071940MINMIL-... → MINMIL"""
    if date_tag not in ticker:
        return ""
    rest = ticker.split(date_tag, 1)[1]
    # rest like 1940MINMIL-SDMMACHADO13-1 or just for RFI: (empty after strip?)
    m = re.match(r"(\d{4})([A-Z]+)", rest)
    if not m:
        # RFI: KXMLBRFI-26AUG071940MINMIL
        m2 = re.match(r"(\d{4})([A-Z]+)$", rest)
        if m2:
            return m2.group(2)
        return re.sub(r"^\d{4}", "", rest.split("-")[0])
    return m.group(2)


def fetch_ml_prices(date_tag: str, cache: PriceCache) -> dict[str, dict[str, Any]]:
    events = _http_get(
        f"{PUBLIC_BASE}/events?status=open&limit=200&series_ticker=KXMLBGAME"
    ).get("events") or []
    out: dict[str, dict[str, Any]] = {}
    for e in events:
        et = e.get("event_ticker") or ""
        if date_tag not in et:
            continue
        key = re.sub(r"^\d{4}", "", et.split(date_tag)[-1])
        mk = _http_get(
            f"{PUBLIC_BASE}/markets?event_ticker={et}&limit=20"
        ).get("markets") or []
        out[key] = {}
        for m in mk:
            ticker = m["ticker"]
            team = ticker.rsplit("-", 1)[-1]
            p = cache.price(ticker)
            if p is None:
                continue
            out[key][team] = {
                "ticker": ticker,
                "price": float(p),
                "subtitle": m.get("yes_sub_title") or team,
            }
    return out


def fetch_series_markets(
    series: str,
    date_tag: str,
    event_keys: set[str],
    max_pages: int = 10,
) -> list[dict]:
    found: list[dict] = []
    cursor = None
    for _ in range(max_pages):
        url = f"{PUBLIC_BASE}/markets?status=open&limit=200&series_ticker={series}"
        if cursor:
            url += f"&cursor={urllib.parse.quote(cursor)}"
        d = _http_get(url)
        for m in d.get("markets") or []:
            t = m.get("ticker") or ""
            if date_tag not in t:
                continue
            ek = _event_key_from_ticker(t, date_tag)
            if event_keys and ek not in event_keys:
                continue
            m["_event_key"] = ek
            found.append(m)
        cursor = d.get("cursor")
        if not cursor:
            break
    return found


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
    team_gap = (h_wp - a_wp) * 4.0
    reasons.append(
        f"records {game['home']}:{game['home_record'][0]}-{game['home_record'][1]} "
        f"vs {game['away']}:{game['away_record'][0]}-{game['away_record'][1]}"
    )
    wx = _weather_offense_boost(game)
    wx_term = 0.15 * wx * (1.0 if team_gap >= 0 else -0.5)
    injury = str(game.get("injury_notes") or "")
    inj = 0.0
    if injury and (game["home"] in injury or ("NYY" in injury and game["home"] == "NYY")):
        inj -= 0.06
        reasons.append(f"injury drag: {injury[:80]}")
    if str(game["home_sp"].get("name")).upper() == "TBD" or float(
        game["home_sp"].get("ip") or 0
    ) < 30:
        sp_gap *= 0.45
    if str(game["away_sp"].get("name")).upper() == "TBD" or float(
        game["away_sp"].get("ip") or 0
    ) < 30:
        sp_gap *= 0.45
    logit = (
        math.log(0.54 / 0.46)
        + 0.45 * sp_gap
        + 1.15 * team_gap
        + 0.017
        + wx_term
        + inj * 4.0
    )
    return min(0.88, max(0.12, _sigmoid(logit))), reasons


def _parse_prop_meta(series: str, ticker: str, title: str) -> tuple[str, int, str, str]:
    """Return family, threshold, team, player_label."""
    fam = series.replace("KXMLB", "")
    thr = 0
    m = re.search(r"-(\d+)$", ticker)
    if m:
        thr = int(m.group(1))
    # team is embedded before player code: ...-MINMIL-SDMMACHADO13-1 → need team from player prefix
    # player segment like SDMMACHADO13 or PHIBHARPER3
    player = ""
    team = ""
    parts = ticker.split("-")
    if len(parts) >= 3:
        seg = parts[-2] if fam != "RFI" else ""
        # map known 2/3-letter prefixes
        for pref in (
            "NYY", "NYM", "CHC", "CWS", "LAD", "LAA", "ATH", "SDP", "SD",
            "SF", "TB", "KC", "AZ", "WSH", "BOS", "MIL", "STL", "PHI",
            "CLE", "DET", "HOU", "TEX", "TOR", "MIN", "MIA", "CIN", "COL",
            "BAL", "SEA", "ATL", "PIT",
        ):
            if seg.startswith(pref):
                team = "SD" if pref == "SDP" else pref
                player = title.split(":")[0].strip() if ":" in title else seg[len(pref):]
                break
    if not player and ":" in title:
        player = title.split(":")[0].strip()
    return fam, thr, team, player


def _game_by_key(slate: dict) -> dict[str, dict]:
    return {g["event_key"]: g for g in slate["games"]}


def _opp_sp_quality_for_team(game: dict, team: str) -> float:
    if team == game["home"]:
        return _sp_quality(game["away_sp"])
    if team == game["away"]:
        return _sp_quality(game["home_sp"])
    return 0.0


def _own_sp_quality_for_team(game: dict, team: str) -> float:
    if team == game["home"]:
        return _sp_quality(game["home_sp"])
    if team == game["away"]:
        return _sp_quality(game["away_sp"])
    return 0.0


def score_prop_market(
    series: str,
    m: dict,
    game: dict,
    cache: PriceCache,
    ml_edge_by_team: dict[str, float],
) -> Optional[Leg]:
    ticker = m["ticker"]
    title = m.get("title") or m.get("yes_sub_title") or ticker
    fam, thr, team, player = _parse_prop_meta(series, ticker, title)
    # Keep liquid / useful thresholds only
    keep = {
        "HIT": {1},
        "HR": {1},
        "RBI": {1},
        "TB": {2},
        "HRR": {1, 2},
        "KS": {4, 5, 6},
    }
    if fam in keep and thr not in keep[fam]:
        return None
    ask = cache.price(ticker)
    if ask is None or ask < 0.08 or ask > 0.85:
        return None

    prior = PROP_PRIORS.get((fam, thr), ask)
    wx = _weather_offense_boost(game)
    park = float(game.get("park_run_factor") or 1.0)
    adj = 0.0
    reasons = []

    if fam in ("HIT", "HR", "RBI", "TB", "HRR"):
        # Hitting props: better vs weak opposing SP, hot parks
        opp = _opp_sp_quality_for_team(game, team) if team else 0.0
        adj += -0.04 * opp  # tough SP lowers hit/HR
        adj += 0.06 * wx
        adj += 0.04 * (park - 1.0)
        if fam == "HR" and park < 0.95:
            adj -= 0.03
            reasons.append("pitcher park HR haircut")
        if team and ml_edge_by_team.get(team, 0) > 0.05:
            adj += 0.015  # team win lean → more counting stats
        reasons.append(f"vsSP_q={opp:+.2f} wx={wx:+.2f} park={park:.2f}")
    elif fam == "KS":
        own = _own_sp_quality_for_team(game, team) if team else 0.0
        adj += 0.05 * own
        # K props for bad SPs should be faded at high lines
        if thr >= 6 and own < 0.2:
            adj -= 0.04
        reasons.append(f"ownSP_q={own:+.2f}")

    raw = min(0.90, max(0.05, prior + adj))
    model = 0.50 * raw + 0.50 * ask  # stronger market blend for props
    edge = model / ask - 1.0
    label = title.replace("?", "")
    return Leg(
        team=team or game.get("home", ""),
        event_key=game["event_key"],
        label=label,
        market_price=ask,
        model_prob=model,
        edge=edge,
        ticker=ticker,
        reasons=reasons + [f"prior={prior:.0%} raw={raw:.0%} blend={model:.0%} mkt={ask:.0%} edge={edge:+.0%}"],
        kind="prop",
        family=fam,
        threshold=thr,
        player=player,
    )


def score_event_market(
    series: str,
    m: dict,
    game: dict,
    cache: PriceCache,
    p_home: float,
    ml_by_team: dict[str, Leg],
) -> Optional[Leg]:
    ticker = m["ticker"]
    title = m.get("title") or ticker
    ask = cache.price(ticker)
    if ask is None or ask < 0.10 or ask > 0.80:
        return None
    ek = game["event_key"]
    fam = series.replace("KXMLB", "")
    reasons: list[str] = []
    raw = ask
    team = ""
    thr = 0
    label = title.replace("?", "")

    if fam == "RFI":
        # First-inning run — bump in hitter parks / weak SP mismatches
        wx = _weather_offense_boost(game)
        sp_soft = -min(_sp_quality(game["home_sp"]), _sp_quality(game["away_sp"]))
        raw = 0.42 + 0.08 * wx + 0.03 * sp_soft
        reasons.append(f"RFI env wx={wx:+.2f}")
        label = f"RFI yes ({game['away']}@{game['home']})"
    elif fam == "F5":
        side = ticker.rsplit("-", 1)[-1]
        if side == "TIE":
            return None
        team = side
        # F5 ≈ slightly less than full-game ML for favorites
        if team == game["home"]:
            raw = min(0.85, p_home * 0.92 + 0.04)
        elif team == game["away"]:
            raw = min(0.85, (1 - p_home) * 0.92 + 0.04)
        else:
            return None
        label = f"{team} F5 win"
        reasons.append(f"from ML model home={p_home:.0%}")
    elif fam == "SPREAD":
        # e.g. ...-MIL2 → wins by over 1.5
        m_sp = re.search(r"-([A-Z]+)(\d+)$", ticker)
        if not m_sp:
            return None
        team, n = m_sp.group(1), int(m_sp.group(2))
        thr = n
        if n != 2:  # only -1.5 style (n=2 means over 1.5)
            return None
        ml = ml_by_team.get(team)
        if not ml:
            return None
        # Rough: P(cover -1.5) ≈ 0.55 * P(win) for solid faves
        raw = max(0.15, min(0.70, ml.model_prob * 0.58 + 0.05 * max(0, ml.edge)))
        label = f"{team} -1.5"
        reasons.append(f"from {team} ML model={ml.model_prob:.0%}")
    elif fam == "TEAMTOTAL":
        m_tt = re.search(r"-([A-Z]+)(\d+)$", ticker)
        if not m_tt:
            return None
        team, line = m_tt.group(1), int(m_tt.group(2))
        thr = line
        # Keep over 2.5 / 3.5 (line codes 3 / 4 in samples)
        if line not in (3, 4):
            return None
        ml = ml_by_team.get(team)
        wx = _weather_offense_boost(game)
        base = 0.70 if line == 3 else 0.55
        if ml:
            base += 0.08 * max(-0.1, min(0.15, ml.edge))
        base += 0.05 * wx
        # fade team totals vs elite SP
        opp = _opp_sp_quality_for_team(game, team)
        base -= 0.04 * max(0, opp)
        raw = base
        label = f"{team} team o{line - 0.5:.1f}"
        reasons.append(f"wx={wx:+.2f} vsSP={opp:+.2f}")
    elif fam == "TOTAL":
        m_to = re.search(r"-(\d+)$", ticker)
        if not m_to:
            return None
        line = int(m_to.group(1))
        thr = line
        # YES ≈ over line (over 7 / 8 / 9 common)
        if line not in (7, 8, 9):
            return None
        wx = _weather_offense_boost(game)
        # better pitching → under; use average SP quality
        avg_sp = (_sp_quality(game["home_sp"]) + _sp_quality(game["away_sp"])) / 2
        # model over-prob
        base = {7: 0.62, 8: 0.50, 9: 0.38}[line]
        base += 0.10 * wx - 0.06 * avg_sp
        raw = base
        label = f"Total o{line - 0.5:.1f} ({game['away']}@{game['home']})"
        reasons.append(f"wx={wx:+.2f} avgSP={avg_sp:+.2f}")
    else:
        return None

    raw = min(0.88, max(0.08, raw))
    model = 0.50 * raw + 0.50 * ask
    edge = model / ask - 1.0
    return Leg(
        team=team or game.get("home", ""),
        event_key=ek,
        label=label,
        market_price=ask,
        model_prob=model,
        edge=edge,
        ticker=ticker,
        reasons=reasons
        + [f"raw={raw:.0%} blend={model:.0%} mkt={ask:.0%} edge={edge:+.0%}"],
        kind="event",
        family=fam,
        threshold=thr,
    )


def score_ml_legs(slate: dict, prices: dict[str, dict[str, Any]]) -> list[Leg]:
    legs: list[Leg] = []
    for game in slate["games"]:
        key = game["event_key"]
        book = prices.get(key) or {}
        if len(book) < 2:
            continue
        p_home_raw, reasons = model_home_win_prob(game)
        for team, p_raw in (
            (game["home"], p_home_raw),
            (game["away"], 1.0 - p_home_raw),
        ):
            info = book.get(team)
            if info is None:
                for alt in book:
                    if alt == team or team.startswith(alt) or alt.startswith(team):
                        info = book[alt]
                        break
            if info is None:
                continue
            mkt = float(info["price"])
            p_model = min(0.90, max(0.10, 0.55 * p_raw + 0.45 * mkt))
            edge = p_model / mkt - 1.0
            legs.append(
                Leg(
                    team=team,
                    event_key=key,
                    label=f"{team} ML",
                    market_price=mkt,
                    model_prob=p_model,
                    edge=edge,
                    ticker=info["ticker"],
                    reasons=list(reasons)
                    + [f"raw={p_raw:.1%} blend={p_model:.1%} mkt={mkt:.0%} edge={edge:+.1%}"],
                    kind="ml",
                    family="ML",
                )
            )
    return legs


def score_all_props_events(
    slate: dict,
    date_tag: str,
    cache: PriceCache,
    ml_legs: list[Leg],
    focus_keys: Optional[set[str]] = None,
) -> list[Leg]:
    games = _game_by_key(slate)
    keys = focus_keys or set(games)
    ml_by_team = {lg.team: lg for lg in ml_legs}
    ml_edge = {lg.team: lg.edge for lg in ml_legs}
    p_home = {}
    for g in slate["games"]:
        p_home[g["event_key"]], _ = model_home_win_prob(g)

    out: list[Leg] = []
    print(f"  fetching props/events for {len(keys)} games...", flush=True)
    for series in PROP_SERIES:
        markets = fetch_series_markets(series, date_tag, keys)
        n = 0
        for m in markets:
            ek = m.get("_event_key") or ""
            g = games.get(ek)
            if not g:
                continue
            leg = score_prop_market(series, m, g, cache, ml_edge)
            if leg is None:
                continue
            out.append(leg)
            n += 1
        print(f"    {series}: kept {n}/{len(markets)}", flush=True)

    for series in EVENT_SERIES:
        markets = fetch_series_markets(series, date_tag, keys)
        n = 0
        for m in markets:
            ek = m.get("_event_key") or ""
            g = games.get(ek)
            if not g:
                continue
            leg = score_event_market(
                series, m, g, cache, p_home.get(ek, 0.5), ml_by_team
            )
            if leg is None:
                continue
            out.append(leg)
            n += 1
        print(f"    {series}: kept {n}/{len(markets)}", flush=True)
    return out


def _combo_ok(legs: list[Leg]) -> bool:
    """Correlation rules for ML + props + events."""
    mls = [lg for lg in legs if lg.kind == "ml"]
    events_ml = [lg.event_key for lg in mls]
    if len(events_ml) != len(set(events_ml)):
        return False
    # At most one ML per game already; max 2 non-ML legs
    non = [lg for lg in legs if lg.kind != "ml"]
    if len(non) > 2:
        return False
    # Same player can't appear twice
    players = [lg.player for lg in legs if lg.player]
    if len(players) != len(set(players)):
        return False
    # Same family+team duplicate (e.g. two HIT props same team) blocked if same event
    fam_team = [(lg.family, lg.team, lg.event_key) for lg in non]
    if len(fam_team) != len(set(fam_team)):
        return False
    # Don't stack TOTAL + TEAMTOTAL same game
    for ek in {lg.event_key for lg in legs}:
        fams = {lg.family for lg in legs if lg.event_key == ek}
        if "TOTAL" in fams and "TEAMTOTAL" in fams:
            return False
        if "ML" in {lg.family for lg in legs if lg.event_key == ek and lg.kind == "ml"}:
            if "F5" in fams:
                # ML + F5 same team only ok; block ML + F5 different implications loosely
                pass
    return True


def _corr_haircut(legs: list[Leg]) -> float:
    events = [lg.event_key for lg in legs]
    if len(events) == len(set(events)):
        return 1.0
    # same-game mix
    kinds = {lg.kind for lg in legs}
    if "prop" in kinds and "ml" in kinds:
        return 0.82
    if "event" in kinds and "ml" in kinds:
        return 0.86
    if "prop" in kinds and "event" in kinds:
        return 0.80
    return 0.85


def build_combos(
    legs: list[Leg],
    stake: float,
    max_legs: int = 4,
    rank_by: str = "ev",
) -> list[Combo]:
    mls = [lg for lg in legs if lg.kind == "ml" and 0.22 <= lg.market_price <= 0.78]
    mls.sort(key=lambda x: (x.edge, x.model_prob), reverse=True)
    chalk = sorted(
        [lg for lg in mls if lg.market_price >= 0.58],
        key=lambda x: x.model_prob,
        reverse=True,
    )[:8]
    ml_pool = list({lg.ticker: lg for lg in mls[:12] + chalk}.values())

    props = sorted(
        [lg for lg in legs if lg.kind == "prop" and lg.edge >= -0.03 and lg.model_prob >= 0.35],
        key=lambda x: (x.edge, x.model_prob),
        reverse=True,
    )[:16]
    events = sorted(
        [lg for lg in legs if lg.kind == "event" and lg.edge >= -0.03 and lg.model_prob >= 0.35],
        key=lambda x: (x.edge, x.model_prob),
        reverse=True,
    )[:12]
    extras = props + events

    bands = [
        ("$100 (4×)", 0.18, 0.32),
        ("$250 (10×)", 0.07, 0.15),
        ("$500 (20×)", 0.035, 0.075),
        ("high-prob", 0.32, 0.55),
    ]
    scored: list[Combo] = []

    def consider(cl: list[Leg]) -> None:
        if not _combo_ok(cl):
            return
        # Prefer at least one ML in moonshot/value tickets
        if not any(lg.kind == "ml" for lg in cl) and len(cl) > 2:
            return
        corr = _corr_haircut(cl)
        mkt = model = 1.0
        for lg in cl:
            mkt *= lg.market_price
            model *= lg.model_prob
        model *= corr
        if mkt < 0.03 or mkt > 0.60:
            return
        band = "other"
        for name, lo, hi in bands:
            if lo <= mkt <= hi:
                band = name
                break
        c = Combo(cl, mkt, model, stake, band)
        if c.edge < -0.20:
            return
        if band == "other" and c.edge < 0:
            return
        scored.append(c)

    for n in range(2, max_legs + 1):
        for cl in combinations(ml_pool, n):
            consider(list(cl))
        # ML + props/events
        for n_ml in range(1, max_legs):
            n_ex = max_legs - n_ml
            if n_ex < 1:
                continue
            for ml_set in combinations(ml_pool, n_ml):
                for ex_set in combinations(extras[:14], min(n_ex, 2)):
                    if len(ml_set) + len(ex_set) < 2:
                        continue
                    consider(list(ml_set) + list(ex_set))

    if rank_by == "hitprob":
        scored.sort(key=lambda c: (c.model_prob, c.expected_profit), reverse=True)
    elif rank_by == "payout":
        scored.sort(key=lambda c: (c.payout_if_hit, c.expected_profit), reverse=True)
    else:
        scored.sort(
            key=lambda c: (
                0 if c.target_band == "other" else 1,
                c.expected_profit,
                c.edge,
            ),
            reverse=True,
        )

    picks: list[Combo] = []
    used: set[str] = set()

    # Always surface best high-prob mix first when ranking by hitprob
    order_bands = (
        ["high-prob", "$100 (4×)", "$250 (10×)", "$500 (20×)"]
        if rank_by == "hitprob"
        else ["$100 (4×)", "$250 (10×)", "$500 (20×)", "high-prob"]
    )
    for band in order_bands:
        for c in scored:
            if c.target_band != band:
                continue
            sig = "|".join(sorted(lg.ticker for lg in c.legs))
            if sig in used:
                continue
            picks.append(c)
            used.add(sig)
            break
    for c in scored:
        if len(picks) >= 3:
            break
        sig = "|".join(sorted(lg.ticker for lg in c.legs))
        if sig in used:
            continue
        picks.append(c)
        used.add(sig)
    return picks[:3]


def print_report(
    legs: list[Leg],
    combos: list[Combo],
    stake: float,
    rank_by: str,
) -> None:
    print("=" * 72)
    print("MLB KALSHI COMBO QUANT — ML + props + game events")
    print("=" * 72)
    print(f"\nStake: ${stake:.0f}   Rank: {rank_by}\n")

    print("TOP ML LEGS")
    print("-" * 72)
    for lg in sorted([x for x in legs if x.kind == "ml"], key=lambda z: z.edge, reverse=True)[:8]:
        print(
            f"  {lg.team:4} mkt={lg.market_price:.0%} model={lg.model_prob:.0%} "
            f"edge={lg.edge:+.0%} [{lg.event_key}]"
        )

    props = [x for x in legs if x.kind == "prop"]
    events = [x for x in legs if x.kind == "event"]
    if props:
        print(f"\nTOP PLAYER PROPS ({len(props)} scored)")
        print("-" * 72)
        for lg in sorted(props, key=lambda z: z.edge, reverse=True)[:10]:
            print(
                f"  {lg.label[:42]:42} mkt={lg.market_price:.0%} "
                f"model={lg.model_prob:.0%} edge={lg.edge:+.0%}"
            )
    if events:
        print(f"\nTOP GAME EVENTS ({len(events)} scored)")
        print("-" * 72)
        for lg in sorted(events, key=lambda z: z.edge, reverse=True)[:10]:
            print(
                f"  {lg.label[:42]:42} mkt={lg.market_price:.0%} "
                f"model={lg.model_prob:.0%} edge={lg.edge:+.0%}"
            )

    print("\n" + "=" * 72)
    print("BEST 2–3 COMBOS (includes props/events when +EV)")
    print("=" * 72)
    if not combos:
        print("No combos found.")
        return
    for i, c in enumerate(combos, 1):
        print(f"\n#{i}  [{c.target_band}]  P(hit)={c.model_prob:.1%}")
        print(f"  Legs: {' + '.join(lg.label for lg in c.legs)}")
        print(
            f"  ask≈{c.market_price:.1%}  edge={c.edge:+.0%}  "
            f"${stake:.0f}→${c.payout_if_hit:.0f} (profit ${c.profit_if_hit:.0f})  "
            f"E[profit]=${c.expected_profit:+.2f}"
        )
        for lg in c.legs:
            print(f"    • [{lg.kind}/{lg.family}] {lg.label}: {lg.reasons[-1]}")
        print(f"  Tickers: {', '.join(lg.ticker for lg in c.legs)}")
    print("\n" + "-" * 72)
    print("Confirm lineups & combo RFQ. Same-game props get a correlation haircut.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Kalshi MLB combo quant (ML+props+events)")
    ap.add_argument("--stake", type=float, default=25.0)
    ap.add_argument("--date-tag", default="26AUG07")
    ap.add_argument("--slate", type=Path, default=SLATE_PATH)
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--props", action="store_true", default=True)
    ap.add_argument("--no-props", action="store_true")
    ap.add_argument(
        "--rank-by",
        choices=("ev", "hitprob", "payout"),
        default="hitprob",
    )
    ap.add_argument(
        "--focus",
        default="ATHBOS,MINMIL,TORPHI,COLSTL,CLECWS,HOUSD,LAAMIA,TBSEA",
        help="Comma event_keys to pull props for (speed)",
    )
    args = ap.parse_args()
    use_props = not args.no_props

    slate = json.loads(args.slate.read_text())
    cache = PriceCache()
    print(f"Loading Kalshi ML prices for {args.date_tag}...", flush=True)
    prices = fetch_ml_prices(args.date_tag, cache)
    print(f"  priced ML events: {len(prices)}", flush=True)
    legs = score_ml_legs(slate, prices)

    if use_props:
        focus = {x.strip() for x in args.focus.split(",") if x.strip()}
        # Always include top ML event keys
        top_ek = {
            lg.event_key
            for lg in sorted(legs, key=lambda z: z.edge, reverse=True)[:10]
        }
        focus |= top_ek
        legs.extend(score_all_props_events(slate, args.date_tag, cache, legs, focus))

    combos = build_combos(legs, stake=args.stake, rank_by=args.rank_by)
    print_report(legs, combos, args.stake, args.rank_by)

    if args.json_out:
        payload = {
            "stake": args.stake,
            "rank_by": args.rank_by,
            "n_legs": len(legs),
            "n_props": sum(1 for lg in legs if lg.kind == "prop"),
            "n_events": sum(1 for lg in legs if lg.kind == "event"),
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
                    "family": lg.family,
                    "player": lg.player,
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
                    "kinds": [lg.kind for lg in c.legs],
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
