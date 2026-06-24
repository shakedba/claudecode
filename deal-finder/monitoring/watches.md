# Watch list — Brooks Adrenaline GTS 25, 4E Extra Wide, EU 43 → Israel

Because the blocker right now is **shipping into Israel (post-conflict carrier
disruption)**, these watches track two things: (1) is the **4E/EU43 in stock**,
and (2) has the **ship-to-Israel route reopened**. Add each in the
changedetection.io UI (`http://localhost:5000` after `docker compose up -d`).

For each watch: paste the URL, set **Fetch method = Playwright/Chrome**
(via the sockpuppetbrowser), set recheck to a few hours, and add the filter /
trigger text shown. Configure one notification URL globally in
**Settings → Notifications** (Telegram/Slack/Discord/email via Apprise).

---

## A. "Has shipping to Israel reopened?" (the real gate)

1. **eBay International Shipping status** — eBay paused IL shipping (Mar 2026).
   Watch for it resuming.
   - URL: `https://www.ebay.com/help/selling/shipping-items/setting-shipping-options/ebay-international-shipping-program?id=5348`
   - Trigger: **"Remove text" / "Ignore" everything except** mentions of Israel;
     or use *"Trigger on text change"* and eyeball when Israel returns to the
     covered list.

2. **Amazon Israel shipping eligibility** — watch a known 4E listing's delivery
   block for an Israel address (set your IL address in the browser profile, or
   watch the listing for the "Deliver to Israel" availability line).
   - URL: your saved Amazon 4E ASIN page (see B2/B3).
   - Trigger text to alert on: `Deliver to Israel` **and not** `does not ship`.

---

## B. "Is the 4E/EU43 in stock?" (so you can buy the instant a route opens)

3. **eBay — saved 4E search** (US sellers list 4E regularly):
   - URL: `https://www.ebay.com/sch/i.html?_nkw=brooks+adrenaline+gts+25+4e+9.5`
   - Watch the results count / first listing; alert on new listings.

4. **Amazon.com — 4E search**:
   - URL: `https://www.amazon.com/s?k=Brooks+Adrenaline+GTS+25+4E+extra+wide+9.5`
   - CSS price filter: `.a-price .a-offscreen`  (alert on price drop / new stock).

5. **Amazon.co.uk — 4E search** (UK uses the 4E label):
   - URL: `https://www.amazon.co.uk/s?k=Brooks+Adrenaline+GTS+25+4E+extra+wide`

6. **=PR= Run & Walk — exact 4E product** (size dropdown shows EU43/US9.5 stock):
   - URL: `https://prrunandwalk.com/products/mens-brooks-adrenaline-gts-25-extra-wide-4e`
   - Visual-selector the size button for **9.5** and trigger when it leaves the
     "sold out / unavailable" state.

7. **We Run Wild — exact 4E product**:
   - URL: `https://www.werunwild.com/product/5695645/brooks/mens-adrenaline-gts-25-extra-wide-4e`

8. **Run and Become — exact 4E product** (buy here only if you later add a
   forwarder; it does NOT ship to IL directly):
   - URL: `https://www.runandbecome.com/item/Brooks/Adrenaline-GTS-25-4E-Extra-Wide/84V4`

---

## Notifications (set once, globally)

Settings → Notifications → add an Apprise URL, e.g.:
- Telegram: `tgram://<bot-token>/<chat-id>`
- Slack:    `slack://<tokenA>/<tokenB>/<tokenC>`
- Email:    `mailto://user:pass@smtp.host?to=you@example.com`

Notification body suggestion:
```
{{watch_url}} changed — {{diff}}
4E GTS25 stock / Israel-shipping update.
```

## Tip
When a route reopens, move fast: the 4E is third-party/low-stock and (per the
research) ship-to-Israel eligibility is currently rationed by flight capacity.
The landed cost of whatever you find is computed by the `dealfinder` engine
(`python -m dealfinder`) — drop the live price into `config.json` first.
