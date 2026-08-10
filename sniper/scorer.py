"""Combine market + community signals into a go/no-go quality decision."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from community import CommunityReport, score_community
import httpx


@dataclass
class QualityDecision:
    pass_filters: bool
    score: float
    coin: dict[str, Any]
    community: CommunityReport
    reasons: list[str] = field(default_factory=list)
    fails: list[str] = field(default_factory=list)

    def summary(self) -> str:
        sym = self.coin.get("symbol") or "?"
        mint = self.coin.get("mint") or ""
        flag = "PASS" if self.pass_filters else "SKIP"
        return (
            f"{flag} {sym} score={self.score:.0f} "
            f"mcap=${float(self.coin.get('usd_market_cap') or 0):,.0f} "
            f"followers={self.community.followers} "
            f"web={'Y' if self.community.website_ok else 'N'} "
            f"replies={self.community.pump_replies} "
            f"{mint[:8]}…"
        )


@dataclass
class FilterConfig:
    min_twitter_followers: int = 50
    require_website: bool = True
    require_twitter_profile: bool = True
    reject_status_links: bool = True
    min_pump_replies: int = 5
    min_usd_mcap: float = 8_000
    max_usd_mcap: float = 250_000
    min_quality_score: float = 55
    reject_nsfw: bool = True


async def evaluate_coin(
    client: httpx.AsyncClient,
    coin: dict[str, Any],
    cfg: FilterConfig,
) -> QualityDecision:
    fails: list[str] = []
    reasons: list[str] = []

    if cfg.reject_nsfw and coin.get("nsfw"):
        fails.append("nsfw")

    mcap = float(coin.get("usd_market_cap") or 0)
    if mcap < cfg.min_usd_mcap:
        fails.append(f"mcap_low (${mcap:,.0f}<${cfg.min_usd_mcap:,.0f})")
    elif mcap > cfg.max_usd_mcap:
        fails.append(f"mcap_high (${mcap:,.0f}>${cfg.max_usd_mcap:,.0f})")
    else:
        reasons.append(f"mcap_in_band (${mcap:,.0f})")

    replies = int(coin.get("reply_count") or 0)
    if replies < cfg.min_pump_replies:
        fails.append(f"replies_low ({replies}<{cfg.min_pump_replies})")

    community = await score_community(
        client,
        twitter=coin.get("twitter"),
        website=coin.get("website"),
        telegram=coin.get("telegram"),
        reply_count=replies,
        min_followers=cfg.min_twitter_followers,
        require_website=cfg.require_website,
        require_twitter_profile=cfg.require_twitter_profile,
        reject_status_links=cfg.reject_status_links,
    )
    fails.extend(community.fails)
    reasons.extend(community.reasons)

    score = community.score
    # mild mcap-band bonus when community already decent
    if not any(f.startswith("mcap_") for f in fails) and community.score >= 40:
        score = min(100.0, score + 5)
        reasons.append("mcap_band_bonus")

    if score < cfg.min_quality_score:
        fails.append(f"quality_score_low ({score:.0f}<{cfg.min_quality_score:.0f})")

    # Hard fails that always block; soft community fails already in list
    hard = [
        f
        for f in fails
        if f.startswith("mcap_")
        or f.startswith("replies_")
        or f.startswith("nsfw")
        or f.startswith("twitter_")
        or f.startswith("no_")
        or f.startswith("website_")
        or f.startswith("quality_")
    ]
    ok = len(hard) == 0 and score >= cfg.min_quality_score

    return QualityDecision(
        pass_filters=ok,
        score=score,
        coin=coin,
        community=community,
        reasons=reasons,
        fails=fails,
    )
