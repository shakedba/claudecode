"""Core data structures shared across the engine."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional
import datetime as _dt


@dataclass
class Offer:
    """A single price observation for the target product at one retailer."""

    retailer_id: str
    retailer_name: str
    url: str
    title: str
    price: Optional[float]          # in the retailer's local currency
    currency: str
    in_stock: Optional[bool]
    ships_to_israel: bool
    shipping_cost: float            # local currency
    notes: str = ""
    matched_size: bool = False      # did we confirm the EU43 / US9.5 variant?
    matched_width: bool = False     # did we confirm the Extra Wide (4E) variant?
    observed_at: str = field(
        default_factory=lambda: _dt.datetime.now(_dt.timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LandedQuote:
    """An Offer enriched with the all-in cost to get it to Israel, in USD."""

    offer: Offer
    item_usd: float
    shipping_usd: float
    vat_usd: float
    customs_usd: float
    fees_usd: float
    total_usd: float
    reachable: bool                 # can this realistically be delivered to IL?
    reason: str = ""                # why not reachable / caveats

    def to_dict(self) -> dict:
        d = {k: v for k, v in asdict(self).items() if k != "offer"}
        d["offer"] = self.offer.to_dict()
        return d
