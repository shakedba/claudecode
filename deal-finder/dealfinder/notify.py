"""Alerting: always prints a ranked table; optionally POSTs to a webhook."""

from __future__ import annotations

import json
import urllib.request
from typing import List

from .models import LandedQuote


def render_table(quotes: List[LandedQuote]) -> str:
    lines = []
    header = f"{'#':<2} {'Retailer':<28} {'Item':>8} {'Ship':>7} {'Tax':>8} {'TOTAL':>9}  Notes"
    lines.append(header)
    lines.append("-" * len(header))
    for i, q in enumerate(quotes, 1):
        o = q.offer
        total = "n/a" if q.total_usd == float("inf") else f"${q.total_usd:,.0f}"
        item = "—" if q.total_usd == float("inf") else f"${q.item_usd:,.0f}"
        ship = f"${q.shipping_usd:,.0f}"
        tax = f"${q.vat_usd + q.customs_usd + q.fees_usd:,.0f}"
        flag = "" if o.ships_to_israel else " [no direct IL ship]"
        note = (q.reason or o.notes)[:48]
        lines.append(
            f"{i:<2} {o.retailer_name[:28]:<28} {item:>8} {ship:>7} {tax:>8} "
            f"{total:>9}  {note}{flag}"
        )
    return "\n".join(lines)


def maybe_webhook(quotes: List[LandedQuote], webhook_url: str, target_usd: float) -> bool:
    """POST a JSON alert if the cheapest reachable total is at/under target."""
    if not webhook_url:
        return False
    reachable = [q for q in quotes if q.reachable and q.total_usd != float("inf")]
    if not reachable:
        return False
    best = min(reachable, key=lambda q: q.total_usd)
    if best.total_usd > target_usd:
        return False
    payload = {
        "text": (
            f"Deal alert: {best.offer.retailer_name} landed total "
            f"${best.total_usd:,.0f} (<= target ${target_usd:,.0f})\n{best.offer.url}"
        ),
        "best": best.to_dict(),
    }
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception:
        return False
