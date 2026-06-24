"""SQLite-backed price history so we can detect drops over time."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from .models import LandedQuote


class PriceStore:
    def __init__(self, path: str = "data/prices.db") -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS observations (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                retailer_id  TEXT NOT NULL,
                observed_at  TEXT NOT NULL,
                price        REAL,
                currency     TEXT,
                total_usd    REAL,
                in_stock     INTEGER,
                url          TEXT
            )
            """
        )
        self.conn.commit()

    def record(self, quote: LandedQuote) -> None:
        o = quote.offer
        self.conn.execute(
            "INSERT INTO observations "
            "(retailer_id, observed_at, price, currency, total_usd, in_stock, url) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                o.retailer_id, o.observed_at, o.price, o.currency,
                quote.total_usd if quote.total_usd != float("inf") else None,
                None if o.in_stock is None else int(o.in_stock),
                o.url,
            ),
        )
        self.conn.commit()

    def previous_best_total(self, retailer_id: str) -> Optional[float]:
        """Most recent prior total_usd for a retailer (before the row we just wrote)."""
        cur = self.conn.execute(
            "SELECT total_usd FROM observations "
            "WHERE retailer_id = ? AND total_usd IS NOT NULL "
            "ORDER BY id DESC LIMIT 1 OFFSET 1",
            (retailer_id,),
        )
        row = cur.fetchone()
        return row[0] if row else None

    def close(self) -> None:
        self.conn.close()
