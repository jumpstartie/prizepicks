"""Community quality checks: Twitter/X profile + website + Pump.fun engagement."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlparse

import httpx

_TW_PROFILE_RE = re.compile(
    r"^(?:https?://)?(?:www\.)?(?:x\.com|twitter\.com)/([A-Za-z0-9_]{1,15})/?$",
    re.I,
)
_TW_STATUS_RE = re.compile(r"/(?:status|i/communities)/", re.I)
_BAD_HOST_FRAGMENTS = (
    "pump.fun",
    "axiom.trade",
    "dexscreener.com",
    "birdeye.so",
    "t.me",
    "telegram.me",
    "linktr.ee",
)


@dataclass
class CommunityReport:
    twitter_url: str = ""
    twitter_handle: str = ""
    twitter_ok: bool = False
    twitter_is_profile: bool = False
    twitter_is_status: bool = False
    followers: int = 0
    following: int = 0
    tweets: int = 0
    twitter_name: str = ""
    twitter_bio: str = ""
    website_url: str = ""
    website_ok: bool = False
    website_status: int = 0
    website_is_real: bool = False
    telegram_url: str = ""
    pump_replies: int = 0
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    fails: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "twitter_url": self.twitter_url,
            "twitter_handle": self.twitter_handle,
            "twitter_ok": self.twitter_ok,
            "followers": self.followers,
            "website_url": self.website_url,
            "website_ok": self.website_ok,
            "telegram_url": self.telegram_url,
            "pump_replies": self.pump_replies,
            "score": round(self.score, 1),
            "reasons": self.reasons,
            "fails": self.fails,
        }


def normalize_twitter(raw: Optional[str]) -> tuple[str, str, bool, bool]:
    """Return (url, handle, is_profile, is_status)."""
    if not raw:
        return "", "", False, False
    s = str(raw).strip()
    if s.startswith("@"):
        handle = s[1:]
        return f"https://x.com/{handle}", handle, True, False
    if _TW_STATUS_RE.search(s):
        return s if s.startswith("http") else f"https://{s}", "", False, True
    m = _TW_PROFILE_RE.match(s.rstrip("/"))
    if m:
        handle = m.group(1)
        if handle.lower() in {"home", "share", "intent", "i", "search", "explore"}:
            return s, "", False, False
        return f"https://x.com/{handle}", handle, True, False
    # bare handle
    if re.fullmatch(r"[A-Za-z0-9_]{1,15}", s):
        return f"https://x.com/{s}", s, True, False
    return s, "", False, False


def website_looks_real(url: str) -> bool:
    if not url or not url.startswith("http"):
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return False
    if not host or "." not in host:
        return False
    return not any(b in host for b in _BAD_HOST_FRAGMENTS)


async def fetch_twitter_profile(client: httpx.AsyncClient, handle: str) -> dict[str, Any]:
    if not handle:
        return {}
    url = f"https://api.fxtwitter.com/{handle}"
    try:
        r = await client.get(url, timeout=12.0)
        if r.status_code != 200:
            return {"error": f"http_{r.status_code}"}
        data = r.json()
        user = data.get("user") or {}
        return {
            "followers": int(user.get("followers") or 0),
            "following": int(user.get("following") or 0),
            "tweets": int(user.get("tweets") or 0),
            "name": str(user.get("name") or ""),
            "bio": str(user.get("description") or ""),
            "ok": True,
        }
    except Exception as e:
        return {"error": str(e)}


async def check_website(client: httpx.AsyncClient, url: str) -> tuple[bool, int]:
    if not url:
        return False, 0
    try:
        r = await client.head(url, follow_redirects=True, timeout=10.0)
        code = r.status_code
        if code >= 400 or code == 405:
            r = await client.get(url, follow_redirects=True, timeout=12.0)
            code = r.status_code
        return 200 <= code < 400, code
    except Exception:
        return False, 0


async def score_community(
    client: httpx.AsyncClient,
    *,
    twitter: Optional[str],
    website: Optional[str],
    telegram: Optional[str],
    reply_count: int = 0,
    min_followers: int = 50,
    require_website: bool = True,
    require_twitter_profile: bool = True,
    reject_status_links: bool = True,
) -> CommunityReport:
    report = CommunityReport(
        twitter_url=str(twitter or ""),
        website_url=str(website or ""),
        telegram_url=str(telegram or ""),
        pump_replies=int(reply_count or 0),
    )
    url, handle, is_profile, is_status = normalize_twitter(twitter)
    report.twitter_url = url or report.twitter_url
    report.twitter_handle = handle
    report.twitter_is_profile = is_profile
    report.twitter_is_status = is_status

    score = 0.0

    if is_status and reject_status_links:
        report.fails.append("twitter_is_status_link")
    elif require_twitter_profile and not is_profile:
        report.fails.append("twitter_not_profile")
    elif is_profile:
        tw = await fetch_twitter_profile(client, handle)
        if tw.get("ok"):
            report.twitter_ok = True
            report.followers = int(tw.get("followers") or 0)
            report.following = int(tw.get("following") or 0)
            report.tweets = int(tw.get("tweets") or 0)
            report.twitter_name = str(tw.get("name") or "")
            report.twitter_bio = str(tw.get("bio") or "")
            if report.followers >= min_followers:
                score += 35
                report.reasons.append(f"twitter_followers>={min_followers} ({report.followers})")
            elif report.followers >= max(10, min_followers // 3):
                score += 15
                report.reasons.append(f"twitter_followers_weak ({report.followers})")
            else:
                report.fails.append(f"twitter_followers_low ({report.followers}<{min_followers})")
            if report.tweets >= 3:
                score += 8
                report.reasons.append("twitter_has_posts")
            if report.twitter_bio:
                score += 5
                report.reasons.append("twitter_has_bio")
        else:
            report.fails.append(f"twitter_lookup_failed:{tw.get('error')}")
    else:
        report.fails.append("no_twitter")

    web = str(website or "").strip()
    report.website_is_real = website_looks_real(web)
    if require_website and not web:
        report.fails.append("no_website")
    elif web and not report.website_is_real:
        report.fails.append("website_not_real_project_site")
    elif report.website_is_real:
        ok, code = await check_website(client, web)
        report.website_ok = ok
        report.website_status = code
        if ok:
            score += 25
            report.reasons.append(f"website_live ({code})")
        else:
            report.fails.append(f"website_dead ({code})")

    if telegram and str(telegram).startswith("http"):
        score += 8
        report.reasons.append("has_telegram")

    if report.pump_replies >= 50:
        score += 15
        report.reasons.append(f"pump_replies>={report.pump_replies}")
    elif report.pump_replies >= 5:
        score += 8
        report.reasons.append(f"pump_replies={report.pump_replies}")

    # Cap / floor
    report.score = max(0.0, min(100.0, score))
    return report
