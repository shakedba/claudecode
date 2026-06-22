# deal-finder

A small, dependency-free engine that hunts for one specific running shoe and
tells you the **all-in cost to get it to Israel** (item + shipping + Israeli
VAT/customs), ranked cheapest-first. Built to monitor:

> **Brooks Adrenaline GTS 25 — Extra Wide (4E) — EU 43 / US 9.5 / UK 8.5**

It runs on the Python 3.11 standard library only (no `pip install`), and can run
daily in GitHub Actions to alert you on a price drop.

## Why it works the way it does

Most shoe retailers embed [schema.org](https://schema.org/Product) **JSON-LD**
(`<script type="application/ld+json">`) with price + availability. Parsing that
is far more robust across sites than hand-written CSS selectors, so the engine
tries JSON-LD first, then Open Graph `product:price:*` meta tags.

It does **not** auto-pick your size/width — variant selection differs per site
and many retailers hide stock behind a size dropdown. Instead it confirms the
**model + width** from the page title and flags "confirm size/width in cart" so
you never buy the wrong variant.

## Quick start

```bash
cd deal-finder
python -m unittest discover -s tests     # 8 offline tests, no network
python -m dealfinder                     # live scan, prints a ranked table
python -m dealfinder --json --no-db      # machine-readable, no history db
```

Example output (prices are illustrative):

```
#  Retailer                Item   Ship    Tax    TOTAL  Notes
1  Amazon US (Global)      $155    $25    $33    $213   Confirm width (4E) and size...
2  SportsShoes.com (UK)    $184    $15    $36    $235   Ships outside EU to Israel...
```

## Configure

Everything lives in [`config.json`](./config.json):

- **`product`** — model keywords, target width keywords, and your size mapping.
- **`destination`** — Israel VAT (18%), import de-minimis tiers, customs rate.
  - Israel personal-import rule modelled: **< $75** exempt · **$75–$500** VAT
    only · **> $500** VAT + customs. Tune freely — it's for *ranking*, not a
    tax ruling.
- **`fx_to_usd`** — exchange rates used to compare retailers in one currency.
  Update these periodically (or wire in a live FX feed).
- **`retailers`** — each entry: `url`, `currency`, `ships_to_israel`,
  `shipping_cost`, `notes`. Add/remove freely.
- **`alerts`** — `target_price_usd` and an optional `webhook_url`
  (Slack/Discord/etc.) that fires when the cheapest reachable total drops to/under
  target.

## Scheduled monitoring

[`.github/workflows/deal-finder.yml`](./.github/workflows/deal-finder.yml) runs
the scan daily (07:00 UTC) and on demand. Add a repo secret
`DEAL_WEBHOOK_URL` to get push alerts; results are also uploaded as an artifact.
Price history accumulates in `data/prices.db` (SQLite) for drop detection.

## Known limitation: bot protection

Some retailers (Cloudflare-fronted sites, Amazon) return **HTTP 403** to plain
`urllib` requests. The engine fails soft (shows `n/a` for that retailer) rather
than crashing. To scrape those reliably you have two clean options:

1. **Official/affiliate APIs** where available (most robust).
2. Add a headless-browser fetcher (`playwright`) behind the existing
   `fetch_html()` interface — `requirements.txt` lists it as optional.

For a one-time purchase you can also just use the ranked retailer list as your
shortlist and confirm price/stock in the browser. See
[`../FINDINGS.md`](../FINDINGS.md) for the current live shortlist of where to
buy and how to ship to Israel.

## Layout

```
deal-finder/
├── config.json                 # product, destination, retailers, alerts
├── dealfinder/
│   ├── __main__.py             # CLI: python -m dealfinder
│   ├── finder.py               # orchestrate: fetch -> extract -> landed -> rank
│   ├── extract.py              # JSON-LD + OG meta extraction
│   ├── landed_cost.py          # Israel VAT/customs landed-cost model
│   ├── fetch.py                # urllib fetch with retry/backoff
│   ├── store.py                # SQLite price history
│   ├── notify.py               # ranked table + webhook alert
│   └── models.py               # Offer, LandedQuote
├── tests/                      # offline unit tests + HTML fixture
└── .github/workflows/          # scheduled scan
```
