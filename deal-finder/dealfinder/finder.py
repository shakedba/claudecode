"""Orchestration: fetch every retailer, extract a price, compute the Israel
landed cost, rank, and report price drops."""

from __future__ import annotations

import json
from typing import List, Optional

from .models import Offer, LandedQuote
from .fetch import fetch_html
from .extract import extract, matches_product
from .landed_cost import compute_landed
from .store import PriceStore


def load_config(path: str = "config.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def scan_retailer(retailer: dict, cfg: dict, offline_html: Optional[str] = None) -> Offer:
    """Build an Offer for one retailer. `offline_html` lets tests skip the network."""
    title = retailer.get("name")
    price = None
    currency = retailer.get("currency", "USD")
    in_stock: Optional[bool] = None
    matched_model = matched_width = False

    try:
        html = offline_html if offline_html is not None else fetch_html(retailer["url"])
        data = extract(html)
        if data.get("price") is not None:
            price = data["price"]
        if data.get("currency"):
            currency = data["currency"]
        in_stock = data.get("in_stock")
        if data.get("title"):
            title = data["title"]
        matched_model, matched_width = matches_product(data.get("title"), cfg["product"])
    except Exception as e:  # network/parse failure shouldn't kill the whole run
        retailer = {**retailer, "notes": f"{retailer.get('notes','')} (fetch error: {e})"}

    return Offer(
        retailer_id=retailer["id"],
        retailer_name=retailer["name"],
        url=retailer["url"],
        title=title or retailer["name"],
        price=price,
        currency=currency,
        in_stock=in_stock,
        ships_to_israel=bool(retailer.get("ships_to_israel", False)),
        shipping_cost=float(retailer.get("shipping_cost", 0.0)),
        notes=retailer.get("notes", ""),
        matched_size=False,  # size is variant-level; confirmed manually in cart
        matched_width=matched_width,
    )


def rank(quotes: List[LandedQuote]) -> List[LandedQuote]:
    """Reachable + in-budget first, then by total cost ascending."""
    return sorted(
        quotes,
        key=lambda q: (not q.reachable, q.total_usd),
    )


def run(cfg: dict, store: Optional[PriceStore] = None,
        offline: Optional[dict] = None) -> List[LandedQuote]:
    """Execute a full scan. `offline` maps retailer_id -> html for testing."""
    offline = offline or {}
    quotes: List[LandedQuote] = []
    for retailer in cfg["retailers"]:
        offer = scan_retailer(retailer, cfg, offline.get(retailer["id"]))
        quote = compute_landed(offer, cfg["destination"], cfg["fx_to_usd"])
        if store is not None:
            store.record(quote)
        quotes.append(quote)
    return rank(quotes)
