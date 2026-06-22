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

## ⚠️ Reality check on the 4E width in Europe

**"Extra Wide / 4E" is a US & UK width designation.** Mainland-EU stock
(including **Amazon.de** and German/French running stores) is almost always only
**Medium (D)** or at most **Wide (2E)** — the **4E is rarely carried in the EU**.
So for the *exact* 4E width your most reliable European sources are **UK**
retailers, and Amazon Europe is a long shot for 4E (great for 2E). Always confirm
the **4E + EU43** variant is actually in the cart before paying.

## Ranked EU/UK routes to Israel (you reported US shipping problems)

### 1. Run and Become (UK) — best for the *exact* 4E, ships to Israel
- Has an explicit **4E Extra Wide** product page for the GTS 25, and offers
  **international express shipping**. Confirm **Israel + UK 8.5 / EU 43** at
  checkout; duties/VAT (18%) payable on arrival.
- https://www.runandbecome.com/item/Brooks/Adrenaline-GTS-25-4E-Extra-Wide/84V4

### 2. SportsShoes.com (UK) — reliably ships to Israel
- Delivers to Israel (outside-EU orders supported); import duty + Israeli VAT
  payable on arrival. Carries the Adrenaline GTS line — confirm 4E (EU stock
  often only 2E).
- Store: https://www.sportsshoes.com/store/brooks-adrenaline
- Tax policy: https://support.sportsshoes.com/hc/en-gb/articles/5026410046098-International-Delivery-Taxes

### 3. Amazon — only Amazon.co.uk is worth trying for 4E
**4E only — 2E is not acceptable.** Checked across marketplaces:
- **Amazon.co.uk** — the *only* Amazon likely to list **4E** (the UK uses the 4E
  label). Ships to Israel via **AmazonGlobal** (~£5.79/kg + £4.39, customs
  prepaid). But Brooks 4E on Amazon is usually **third-party / sporadic** — verify
  the **4E + UK 8.5 / EU 43** variant is actually listed before relying on it.
  https://www.amazon.co.uk/s?k=Brooks+Adrenaline+GTS+25+4E+extra+wide
- **Amazon.de / mainland-EU Amazon** — does **not** carry 4E (Medium/2E only). Skip.
- **Amazon.com (US)** — 4E appears only via 3rd-party sellers; plus you had US
  shipping issues. Fallback only.

> Verdict: no Amazon marketplace *reliably* stocks the exact 4E/EU43. Amazon.co.uk
> is the one to check; otherwise use the UK specialists (options 1, 2, and below).

### 3b. Other reliable UK 4E specialists (£145)
- **Profeet.co.uk** — dedicated "Adrenaline GTS 25 4E Wide" page (confirm Israel
  shipping; may need a forwarder): https://shop.profeet.co.uk/footwear/wide-fit-running-shoes/brooks-adrenaline-gts-25-4e-wide-mens-running-shoes--black__866
- **Brooks UK official** — lists 4E, UK 6–13: https://www.brooksrunning.com/en_gb/mens/road-running-shoes/adrenaline-gts-25/110454.html

### 4. EU mainland stores (i-Run.fr, Keller Sports) — need a forwarder
These big EU running stores **don't ship directly to Israel**, so route via a
parcel forwarder with an EU address:
- **i-Run.fr** (France) → forward with **Easy-Delivery** (FR address): https://www.easy-delivery.com/en/delivery/i-run-shoes-clothes-for-running-trail-fitness/israel
- **Keller Sports** (Germany) → **ColisExpat** or **ShipGerman**: https://www.colisexpat.com/en/delivery-shipping/keller-sports/
- Add the forwarder's quoted leg into that retailer's `shipping_cost` in
  `deal-finder/config.json` and the engine folds it into the landed total.

## What does *not* work
- **Zalando** — does **not** deliver to Israel.
- **i-Run / Keller Sports** — no *direct* Israel delivery (forwarder only).
- (US fallback) **Road Runner Sports** US-only; **Zappos** no reliable direct IL.

## Rough landed-cost math (illustrative)
For a ~$155 shoe + ~$20 shipping into Israel, the **$75–$500 tier** applies:
**VAT only (18%), no customs duty** → roughly **$175 × 1.18 ≈ $207 landed**.
The engine computes this per-retailer with live prices and your FX rates.

## Sources
- [Run and Become (UK) — Adrenaline GTS 25 4E Extra Wide](https://www.runandbecome.com/item/Brooks/Adrenaline-GTS-25-4E-Extra-Wide/84V4)
- [SportsShoes.com — Brooks Adrenaline](https://www.sportsshoes.com/store/brooks-adrenaline)
- [SportsShoes International Delivery & Taxes](https://support.sportsshoes.com/hc/en-gb/articles/5026410046098-International-Delivery-Taxes)
- [Amazon.de — International Delivery Rates & Times](https://www.amazon.de/-/en/gp/help/customer/display.html?nodeId=GA6MMBQJBJ5QYUDW)
- [AmazonGlobal Export Countries (incl. Israel)](https://www.amazon.com/gp/help/customer/display.html?nodeId=GCBBSZMUXA6U2P8R)
- [Amazon reinstates free shipping to Israel (Ynet)](https://www.ynetnews.com/business/article/r1myupqea)
- [i-Run.fr → Israel via Easy-Delivery](https://www.easy-delivery.com/en/delivery/i-run-shoes-clothes-for-running-trail-fitness/israel)
- [Keller Sports → worldwide via ColisExpat](https://www.colisexpat.com/en/delivery-shipping/keller-sports/)
- [Brooks Adrenaline GTS 25 (official)](https://www.brooksrunning.com/en_us/mens/shoes/road-running-shoes/adrenaline-gts-25/110454.html)
- [Amazon US — Brooks Adrenaline GTS 25 (fallback)](https://www.amazon.com/Brooks-Adrenaline-Supportive-Running-Walking/dp/B0DZ425CX2)
