"""CLI entry point:  python -m dealfinder [--config config.json] [--no-db] [--json]"""

from __future__ import annotations

import argparse
import json
import sys

from .finder import load_config, run
from .store import PriceStore
from .notify import render_table, maybe_webhook


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Find & monitor a shoe deal shippable to Israel.")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--db", default="data/prices.db", help="SQLite price-history path")
    ap.add_argument("--no-db", action="store_true", help="skip recording price history")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    store = None if args.no_db else PriceStore(args.db)

    quotes = run(cfg, store=store)

    if args.json:
        print(json.dumps([q.to_dict() for q in quotes], indent=2))
    else:
        p = cfg["product"]
        print(f"\nTarget: {p['name']} — {p['width']} — EU{p['size']['eu']} "
              f"(US {p['size']['us_men']} / UK {p['size']['uk_men']})")
        print(f"Destination: {cfg['destination']['country']} "
              f"(VAT {cfg['destination']['vat_rate']*100:.0f}%)\n")
        print(render_table(quotes))
        print("\nAll totals are estimated landed cost in USD (item + shipping + IL VAT/customs).")

    alerts = cfg.get("alerts", {})
    if maybe_webhook(quotes, alerts.get("webhook_url", ""),
                     float(alerts.get("target_price_usd", 0))):
        print("\n🔔 Webhook alert sent (cheapest reachable total is at/under target).")

    if store:
        store.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
