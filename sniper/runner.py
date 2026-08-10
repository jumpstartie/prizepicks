#!/usr/bin/env python3
"""Pump.fun quality sniper — community-gated entries, paper by default."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Set

import httpx

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))

from axiom_client import AxiomBridge
from community import normalize_twitter
from pumpfun_client import PumpFunClient
from scorer import FilterConfig, evaluate_coin
from trader import Trader
from wallet import WalletError, get_sol_balance, load_keypair, resolve_public_key


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_env_file(path: Path, *, override: bool = True) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if not k:
            continue
        if override or k not in os.environ:
            os.environ[k] = v


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return float(raw)


def env_int(name: str, default: int) -> int:
    return int(env_float(name, float(default)))


def build_filters() -> FilterConfig:
    return FilterConfig(
        min_twitter_followers=env_int("MIN_TWITTER_FOLLOWERS", 50),
        require_website=env_bool("REQUIRE_WEBSITE", True),
        require_twitter_profile=env_bool("REQUIRE_TWITTER_PROFILE", True),
        reject_status_links=env_bool("REJECT_STATUS_LINKS", True),
        min_pump_replies=env_int("MIN_PUMP_REPLIES", 5),
        min_usd_mcap=env_float("MIN_USD_MCAP", 8_000),
        max_usd_mcap=env_float("MAX_USD_MCAP", 250_000),
        min_quality_score=env_float("MIN_QUALITY_SCORE", 55),
    )


def quick_prefilter(coin: dict[str, Any], cfg: FilterConfig) -> Optional[str]:
    """Cheap rejects before Twitter/website HTTP calls."""
    if cfg.reject_nsfw and coin.get("nsfw"):
        return "nsfw"
    # Default allows migrated/hot coins for more movement; set REQUIRE_ON_CURVE=1 to restrict
    if env_bool("REQUIRE_ON_CURVE", False) and coin.get("complete") is True:
        return "already_migrated"
    mcap = float(coin.get("usd_market_cap") or 0)
    if mcap < cfg.min_usd_mcap or mcap > cfg.max_usd_mcap:
        return "mcap_band"
    replies = int(coin.get("reply_count") or 0)
    if replies < cfg.min_pump_replies:
        return "replies"
    tw = coin.get("twitter") or ""
    _, _, is_profile, is_status = normalize_twitter(tw)
    if cfg.reject_status_links and is_status:
        return "status_link"
    if cfg.require_twitter_profile and not is_profile:
        return "no_tw_profile"
    web = str(coin.get("website") or "").strip()
    if cfg.require_website and not web:
        return "no_website"
    return None


async def manage_exits(
    client: httpx.AsyncClient,
    pump: PumpFunClient,
    trader: Trader,
    *,
    take_profit_x: float,
    stop_loss_x: float,
) -> None:
    for mint, pos in list(trader.positions.items()):
        coin = await pump.get_coin(mint)
        if not coin:
            continue
        mcap = float(coin.get("usd_market_cap") or 0)
        if pos.entry_mcap_usd <= 0 or mcap <= 0:
            continue
        x = mcap / pos.entry_mcap_usd
        if x >= take_profit_x:
            log(f"TP {pos.symbol} {x:.2f}x mcap ${mcap:,.0f} — selling")
            await trader.sell(client, mint, reason="take_profit", mark_mcap_usd=mcap)
        elif x <= stop_loss_x:
            log(f"SL {pos.symbol} {x:.2f}x mcap ${mcap:,.0f} — selling")
            await trader.sell(client, mint, reason="stop_loss", mark_mcap_usd=mcap)


async def run_loop(args: argparse.Namespace) -> None:
    load_env_file(REPO / "secrets" / "sniper.env")
    load_env_file(REPO / "secrets" / "env.sh")

    mode = (args.mode or os.getenv("SNIPER_MODE") or "paper").lower()
    cfg = build_filters()
    poll = env_float("POLL_SECS", 8.0)
    max_open = env_int("MAX_OPEN", 3)
    buy_sol = env_float("BUY_SOL", 0.05)
    tp = env_float("TAKE_PROFIT_X", 2.0)
    sl = env_float("STOP_LOSS_X", 0.55)
    rpc = os.getenv("SOLANA_RPC_URL") or "https://api.mainnet-beta.solana.com"

    keypair = None
    pubkey = ""
    try:
        keypair = load_keypair()
    except WalletError as e:
        if mode == "live":
            raise SystemExit(str(e))
        if args.connect_wallet:
            log(f"no signing key yet (watch-only ok): {e}")

    try:
        pubkey = resolve_public_key(keypair)
        bal = await get_sol_balance(rpc, pubkey)
        log(
            f"wallet {pubkey} balance={bal:.4f} SOL "
            f"({'signing' if keypair else 'watch-only'})"
        )
        reserve = env_float("MIN_SOL_RESERVE", 0.0025)
        priority = env_float("PRIORITY_FEE_SOL", 0.00005)
        need = buy_sol + reserve + priority
        if mode == "live" and bal < need:
            raise SystemExit(
                f"insufficient SOL for live buys (have {bal:.4f}, need ~{need:.4f} "
                f"= buy {buy_sol} + reserve {reserve} + priority {priority})"
            )
    except WalletError as e:
        log(f"wallet address not set: {e}")

    axiom = AxiomBridge()
    if axiom.enabled and pubkey:
        try:
            ab = axiom.get_balance(pubkey)
            log(f"axiom balance check: {ab}")
        except Exception as e:
            log(f"axiom optional check skipped: {e}")

    trader = Trader(
        mode=mode,
        keypair=keypair,
        rpc_url=rpc,
        buy_sol=buy_sol,
        slippage_pct=env_float("SLIPPAGE_PCT", 5.0),
        priority_fee_sol=env_float("PRIORITY_FEE_SOL", 0.00005),
        pool=os.getenv("TRADE_POOL") or "auto",
        state_path=ROOT / "state.json",
        trades_path=ROOT / "trades.jsonl",
    )

    seen: Set[str] = set()
    seen_path = ROOT / "seen_mints.json"
    if seen_path.exists():
        try:
            seen = set(json.loads(seen_path.read_text()))
        except Exception:
            seen = set()

    log(
        f"starting sniper mode={trader.mode} buy={buy_sol} SOL "
        f"filters followers>={cfg.min_twitter_followers} "
        f"mcap=${cfg.min_usd_mcap:,.0f}-${cfg.max_usd_mcap:,.0f} "
        f"min_score={cfg.min_quality_score} replies>={cfg.min_pump_replies}"
    )
    if trader.mode == "paper":
        log("PAPER mode — no real trades. Set SNIPER_MODE=live after funding wallet to go live.")

    headers = {"User-Agent": "prizepicks-pump-sniper/0.1", "Accept": "application/json"}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        pump = PumpFunClient(client)
        while True:
            try:
                await manage_exits(client, pump, trader, take_profit_x=tp, stop_loss_x=sl)

                # blend newest + actively traded
                newest = await pump.newest(limit=40)
                hot = await pump.hottest(limit=40)
                by_mint: dict[str, dict[str, Any]] = {}
                for c in newest + hot:
                    m = c.get("mint")
                    if m:
                        by_mint[str(m)] = c

                candidates = 0
                for mint, coin in by_mint.items():
                    if mint in trader.positions or mint in seen:
                        continue
                    reason = quick_prefilter(coin, cfg)
                    if reason:
                        continue
                    candidates += 1
                    decision = await evaluate_coin(client, coin, cfg)
                    if not decision.pass_filters:
                        seen.add(mint)
                        if args.verbose:
                            log(f"{decision.summary()} fails={decision.fails[:4]}")
                        continue

                    log(decision.summary())
                    log(
                        f"  twitter=@{decision.community.twitter_handle} "
                        f"followers={decision.community.followers} "
                        f"web={decision.community.website_url} "
                        f"reasons={decision.reasons[:5]}"
                    )

                    if len(trader.positions) >= max_open:
                        log(f"max open positions ({max_open}) — signal only")
                        seen.add(mint)
                        continue

                    if args.dry_run:
                        log("dry-run: not buying")
                        seen.add(mint)
                        continue

                    try:
                        pos = await trader.buy(client, coin, quality_score=decision.score)
                        log(
                            f"BUY {pos.symbol} {pos.entry_sol} SOL "
                            f"mcap=${pos.entry_mcap_usd:,.0f} "
                            f"{'paper' if pos.paper else 'LIVE tx='+pos.tx}"
                        )
                    except Exception as e:
                        log(f"buy failed {coin.get('symbol')}: {e}")
                    seen.add(mint)

                # persist seen (cap size)
                if len(seen) > 5000:
                    seen = set(list(seen)[-3000:])
                seen_path.write_text(json.dumps(sorted(seen)[-3000:]))

                open_n = len(trader.positions)
                cash = trader.paper_cash_sol if not trader.live else None
                log(
                    f"loop ok candidates_checked~{candidates} open={open_n} "
                    + (f"paper_cash={cash:.3f}SOL" if cash is not None else f"wallet={pubkey[:8]}…")
                )
            except Exception as e:
                log(f"loop error: {e}")
            await asyncio.sleep(poll)


def main() -> None:
    p = argparse.ArgumentParser(description="Pump.fun community-quality sniper")
    p.add_argument("--mode", choices=["paper", "live"], default=None)
    p.add_argument("--connect-wallet", action="store_true", help="Load Phantom key and show balance")
    p.add_argument("--dry-run", action="store_true", help="Score only, never buy")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--once", action="store_true", help="Single scan then exit")
    args = p.parse_args()

    if args.once:
        async def once() -> None:
            load_env_file(REPO / "secrets" / "sniper.env")
            cfg = build_filters()
            headers = {"User-Agent": "prizepicks-pump-sniper/0.1", "Accept": "application/json"}
            async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
                pump = PumpFunClient(client)
                coins = await pump.hottest(limit=60)
                hits = 0
                for coin in coins:
                    if quick_prefilter(coin, cfg):
                        continue
                    d = await evaluate_coin(client, coin, cfg)
                    if d.pass_filters or args.verbose:
                        log(d.summary() + ("" if d.pass_filters else f" fails={d.fails[:3]}"))
                        if d.pass_filters:
                            hits += 1
                log(f"scan done passes={hits}")

        asyncio.run(once())
        return

    asyncio.run(run_loop(args))


if __name__ == "__main__":
    main()
