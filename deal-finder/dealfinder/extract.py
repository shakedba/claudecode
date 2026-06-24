"""Extract price / availability / title from a product page.

Strategy (most robust first):
  1. schema.org JSON-LD  (<script type="application/ld+json"> Product/Offer)
  2. Open Graph / meta price tags  (og:price:amount, product:price:amount)
As a portability win these cover the large majority of shoe retailers without
needing a hand-written CSS selector per site.
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from typing import Any, Optional


# ----------------------------- JSON-LD ------------------------------------ #

class _LdParser(HTMLParser):
    """Collect the text inside every <script type="application/ld+json">."""

    def __init__(self) -> None:
        super().__init__()
        self._in_ld = False
        self.blocks: list[str] = []
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._in_ld = True
            self._buf = []

    def handle_data(self, data):
        if self._in_ld:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self._in_ld = False
            self.blocks.append("".join(self._buf))


def _iter_products(node: Any):
    """Yield every dict in the JSON-LD graph that looks like a Product."""
    if isinstance(node, list):
        for item in node:
            yield from _iter_products(item)
    elif isinstance(node, dict):
        if "@graph" in node:
            yield from _iter_products(node["@graph"])
        t = node.get("@type", "")
        types = t if isinstance(t, list) else [t]
        if any("Product" in str(x) for x in types):
            yield node


def _first_offer(product: dict) -> dict:
    offers = product.get("offers")
    if isinstance(offers, list):
        return offers[0] if offers else {}
    if isinstance(offers, dict):
        return offers
    return {}


def _from_jsonld(html: str) -> Optional[dict]:
    p = _LdParser()
    try:
        p.feed(html)
    except Exception:
        return None
    for block in p.blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for product in _iter_products(data):
            offer = _first_offer(product)
            price = offer.get("price") or offer.get("lowPrice")
            avail = str(offer.get("availability", "")).lower()
            in_stock = None
            if avail:
                in_stock = "instock" in avail or "limited" in avail
            return {
                "title": product.get("name"),
                "price": _to_float(price),
                "currency": offer.get("priceCurrency"),
                "in_stock": in_stock,
            }
    return None


# ------------------------------- meta -------------------------------------- #

_META_PRICE = re.compile(
    r'<meta[^>]+(?:property|name)=["\'](?:og:price:amount|product:price:amount)["\']'
    r'[^>]+content=["\']([\d.,]+)["\']',
    re.I,
)
_META_CUR = re.compile(
    r'<meta[^>]+(?:property|name)=["\'](?:og:price:currency|product:price:currency)["\']'
    r'[^>]+content=["\']([A-Z]{3})["\']',
    re.I,
)
_META_TITLE = re.compile(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', re.I
)


def _from_meta(html: str) -> Optional[dict]:
    m = _META_PRICE.search(html)
    if not m:
        return None
    cur = _META_CUR.search(html)
    title = _META_TITLE.search(html)
    return {
        "title": title.group(1) if title else None,
        "price": _to_float(m.group(1)),
        "currency": cur.group(1) if cur else None,
        "in_stock": None,
    }


# ------------------------------ helpers ------------------------------------ #

def _to_float(value) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r"[^\d.]", "", str(value).replace(",", ""))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def extract(html: str) -> dict:
    """Return {title, price, currency, in_stock}; missing fields are None."""
    result = _from_jsonld(html) or _from_meta(html) or {}
    return {
        "title": result.get("title"),
        "price": result.get("price"),
        "currency": result.get("currency"),
        "in_stock": result.get("in_stock"),
    }


def matches_product(title: Optional[str], cfg_product: dict) -> tuple[bool, bool]:
    """Return (matched_model, matched_width) based on title keywords."""
    if not title:
        return (False, False)
    low = title.lower()
    model = all(k.lower() in low for k in cfg_product.get("match_keywords", []))
    width = any(
        k.lower() in low for k in cfg_product.get("match_width_keywords", [])
    )
    return (model, width)
