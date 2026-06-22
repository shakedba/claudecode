"""Tiny HTTP fetcher built on urllib (no third-party deps).

Retries with exponential backoff on transient network errors.
"""

from __future__ import annotations

import time
import urllib.request
import urllib.error

_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 dealfinder/0.1"
)


def fetch_html(url: str, timeout: int = 20, retries: int = 3) -> str:
    """Return decoded HTML for `url`, or raise the last error after retries."""
    last_err: Exception | None = None
    delay = 2.0
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": _UA,
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")
