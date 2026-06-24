"""Compute the landed cost (item + shipping + Israeli VAT/customs) of an Offer.

Israel import rules modelled here (configurable in config.json):
  * Standard VAT: 18% (since 2025).
  * De-minimis tiers on the (item + shipping) value in USD:
      - under $75            -> no VAT, no customs
      - $75 to $500          -> VAT only, no customs duty
      - over $500            -> VAT + customs/purchase tax
These are simplifications of Israel Customs personal-import rules and are meant
for ranking offers, not as a tax ruling. Tune the numbers in config.json.
"""

from __future__ import annotations

from typing import Dict
from .models import Offer, LandedQuote


def _to_usd(amount: float, currency: str, fx_to_usd: Dict[str, float]) -> float:
    rate = fx_to_usd.get(currency.upper())
    if rate is None:
        raise KeyError(
            f"No FX rate for currency {currency!r}; add it to config 'fx_to_usd'."
        )
    return amount * rate


def _tier_for(value_usd: float, tiers: list) -> dict:
    for tier in tiers:
        cap = tier.get("max")
        if cap is None or value_usd <= cap:
            return tier
    return tiers[-1]


def compute_landed(offer: Offer, dest: dict, fx_to_usd: Dict[str, float]) -> LandedQuote:
    """Turn an Offer into a LandedQuote priced in USD."""

    if offer.price is None:
        return LandedQuote(
            offer=offer,
            item_usd=0.0, shipping_usd=0.0, vat_usd=0.0,
            customs_usd=0.0, fees_usd=0.0, total_usd=float("inf"),
            reachable=False,
            reason="No price found (out of stock or selector needs calibration).",
        )

    item_usd = _to_usd(offer.price, offer.currency, fx_to_usd)
    shipping_usd = _to_usd(offer.shipping_cost, offer.currency, fx_to_usd)
    dutiable = item_usd + shipping_usd

    tier = _tier_for(dutiable, dest["import_tiers_usd"])

    customs_usd = 0.0
    if tier.get("apply_customs"):
        customs_usd = item_usd * float(dest.get("customs_duty_rate", 0.0))

    vat_usd = 0.0
    if tier.get("apply_vat"):
        # VAT is charged on item + shipping + customs (CIF + duty).
        vat_usd = (dutiable + customs_usd) * float(dest.get("vat_rate", 0.0))

    fees_usd = float(dest.get("clearance_fee_usd", 0.0))
    total_usd = item_usd + shipping_usd + customs_usd + vat_usd + fees_usd

    reachable = bool(offer.ships_to_israel)
    reason = "" if reachable else (
        "Retailer does not ship to Israel directly — route via a freight "
        "forwarder (add the forwarder leg to shipping_cost)."
    )
    if reachable and not (offer.matched_width and offer.matched_size):
        unconfirmed = []
        if not offer.matched_width:
            unconfirmed.append("width (4E)")
        if not offer.matched_size:
            unconfirmed.append("size (EU43/US9.5)")
        reason = "Confirm " + " and ".join(unconfirmed) + " in cart before buying."

    return LandedQuote(
        offer=offer,
        item_usd=round(item_usd, 2),
        shipping_usd=round(shipping_usd, 2),
        vat_usd=round(vat_usd, 2),
        customs_usd=round(customs_usd, 2),
        fees_usd=round(fees_usd, 2),
        total_usd=round(total_usd, 2),
        reachable=reachable,
        reason=reason,
    )
