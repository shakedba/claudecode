# Where to buy — Brooks Adrenaline GTS 25, Extra Wide (4E), EU 43

**Your size:** EU 43 = **US 9.5 (men)** = **UK 8.5 (men)**. Brooks lists this
width as **"Extra Wide (4E)"** for men (the medium is "D", wide is "2E", extra
wide is "4E"). MSRP is **~$155 USD / £145 GBP**.

> Snapshot researched 2026-06-22. Stock and prices on shoes move fast — the
> [`deal-finder`](./deal-finder) engine in this repo re-checks these on a
> schedule. Always confirm the **4E width + EU43** in the cart before paying.

## Use these existing tools first (don't reinvent discovery)

Before relying on the custom engine, these off-the-shelf services already do
price discovery/alerting well. Use them for finding the price; use the
[`deal-finder`](./deal-finder) engine for the part they *don't* do — the **Israel
landed cost** (VAT + customs).

- **ShoesTrace AI** — https://shoestrace.com — price tracker + AI search across
  17,000+ shoes. Search "Brooks Adrenaline GTS 25" for a live price ranking. Free.
- **Running Shoe Score** — https://runningshoescore.com — running-shoe price
  comparison + drop alerts, updated daily. Free.
- **CamelCamelCamel** — https://camelcamelcamel.com — free Amazon price history +
  alerts; pair with **Amazon Global** (ships the GTS 25 to Israel, customs prepaid).
- **Keepa** — https://keepa.com — Amazon tracker across 11 marketplaces (good for
  catching the 4E width on Amazon UK/DE). ~$20/mo for premium.
- **changedetection.io** — https://changedetection.io — 30k★ open-source,
  self-hosted page-change monitor with Playwright + JSON price extraction. Point it
  at the bot-protected 4E retailer pages below if you want private monitoring.

> Note: none of these compute the all-in delivered-to-Israel price including 18%
> VAT and customs tiers — that's exactly what `deal-finder` adds on top.

## Ranked routes to Israel

### 1. SportsShoes.com (UK) — best "ships directly to Israel" option
- **Ships to Israel:** yes (outside-EU orders supported). Import duty + Israeli
  VAT (18%) are payable on arrival; SportsShoes doesn't prepay them.
- **Why first:** UK retailer that actually delivers to IL and carries the Brooks
  Adrenaline GTS line. Confirm the **4E / EU43** variant is in stock at checkout
  — some brands restrict non-EU shipping, and you'd be told at the cart.
- Store: https://www.sportsshoes.com/store/brooks-adrenaline
- Shipping/tax policy: https://support.sportsshoes.com/hc/en-gb/articles/5026410046098-International-Delivery-Taxes

### 2. Amazon US (Global) — taxes handled for you
- **Ships to Israel:** many Brooks listings ship via **Amazon Global** with an
  **Import Fees Deposit** collected at checkout, so customs/VAT are prepaid (no
  surprise bill at the door).
- Verify the listing's "Deliver to Israel" box shows the **Extra Wide 4E, 9.5**
  variant as eligible — width/size eligibility varies by third-party seller.
- Listing: https://www.amazon.com/Brooks-Adrenaline-Supportive-Running-Walking/dp/B0DZ425CX2

### 3. US specialist + freight forwarder — most reliable for the exact 4E
These US stores reliably stock the **exact Extra Wide (4E)** colorways but ship
**US-only**, so pair them with a forwarder (Shippn, USendHome, etc.) that
re-ships to Israel:
- **=PR= Run & Walk** (exact 4E page): https://prrunandwalk.com/products/mens-brooks-adrenaline-gts-25-extra-wide-4e
- **We Run Wild** (4E colorways): https://www.werunwild.com/product/5695645/brooks/mens-adrenaline-gts-25-extra-wide-4e
- **Brooks USA official** (4E, often sold out): https://www.brooksrunning.com/en_us/mens/shoes/road-running-shoes/adrenaline-gts-25/110454.html
- Forwarder route US→IL: https://www.shippn.com/en/route/shop-from-us-to-il

> Add the forwarder's quoted leg into the retailer's `shipping_cost` in
> `deal-finder/config.json` and the engine will fold it into the landed total.

## What does *not* work
- **Road Runner Sports** — US/territories only, **no international shipping**.
- **Zappos** — primarily US; there's a marketing "Israel" page but no reliable
  direct IL delivery for this variant.

## Rough landed-cost math (illustrative)
For a ~$155 shoe + ~$20 shipping into Israel, the **$75–$500 tier** applies:
**VAT only (18%), no customs duty** → roughly **$175 × 1.18 ≈ $207 landed**.
The engine computes this per-retailer with live prices and your FX rates.

## Sources
- [Brooks Adrenaline GTS 25 (men's, official)](https://www.brooksrunning.com/en_us/mens/shoes/road-running-shoes/adrenaline-gts-25/110454.html)
- [=PR= Run & Walk — Men's 4E Extra Wide](https://prrunandwalk.com/products/mens-brooks-adrenaline-gts-25-extra-wide-4e)
- [We Run Wild — Men's 4E Extra Wide](https://www.werunwild.com/product/5695645/brooks/mens-adrenaline-gts-25-extra-wide-4e)
- [SportsShoes.com — Brooks Adrenaline](https://www.sportsshoes.com/store/brooks-adrenaline)
- [SportsShoes International Delivery & Taxes](https://support.sportsshoes.com/hc/en-gb/articles/5026410046098-International-Delivery-Taxes)
- [Amazon — Brooks Adrenaline GTS 25 (men's)](https://www.amazon.com/Brooks-Adrenaline-Supportive-Running-Walking/dp/B0DZ425CX2)
- [Road Runner Sports — shipping info (US-only)](https://www.roadrunnersports.com/content/shipping-info)
- [Shippn — US→Israel forwarding](https://www.shippn.com/en/route/shop-from-us-to-il)
