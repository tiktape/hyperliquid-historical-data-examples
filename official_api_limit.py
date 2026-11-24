"""Show the 5000-candle limit of Hyperliquid's own candleSnapshot API (no key).

    pip install requests
    python official_api_limit.py

Asks the official info endpoint for 7 days of BTC 1m candles, paging with the
last returned timestamp as the docs describe, and prints how far back it got.
"""

import time
from datetime import datetime, timezone

import requests

INFO = "https://api.hyperliquid.xyz/info"
end = int(time.time() * 1000)
start = end - 7 * 86_400_000

candles, cursor = {}, start
while cursor < end:
    batch = requests.post(INFO, timeout=30, json={
        "type": "candleSnapshot",
        "req": {"coin": "BTC", "interval": "1m", "startTime": cursor, "endTime": end},
    }).json()
    if not batch:
        cursor += 500 * 60_000  # nothing this far back: skip ahead
        continue
    for c in batch:
        candles[c["t"]] = c
    cursor = batch[-1]["t"] + 60_000


def iso(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat(timespec="minutes")


print(f"asked for 7 days ({7 * 1440} candles) from {iso(start)}")
print(f"got {len(candles)} candles, earliest {iso(min(candles))}")
