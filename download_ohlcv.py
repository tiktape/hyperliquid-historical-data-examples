"""Download Hyperliquid OHLCV candles past the 5000-candle API limit.

    pip install requests
    TIKTAPE_API_KEY=tt_... python download_ohlcv.py BTC 1m 7

Arguments: coin (BTC, ETH, spot ids like @1, HIP-3 like cash:NVDA), interval
(1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w; default 1m), days back
(default 7). Writes <coin>_<interval>.csv. A free key reads the most recent
30 days; paid keys reach back to 2025-03-23.
"""

import csv
import os
import sys
import time

import requests

API = "https://tiktape.xyz/api/v1/ohlcv"
GET_KEY_URL = "https://tiktape.xyz/?utm_source=github&utm_medium=example&utm_campaign=hl-data-examples#freeKeyCard"
STEP_MS = {"1m": 60_000, "3m": 180_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
           "1h": 3_600_000, "2h": 7_200_000, "4h": 14_400_000, "6h": 21_600_000,
           "8h": 28_800_000, "12h": 43_200_000, "1d": 86_400_000, "3d": 259_200_000,
           "1w": 604_800_000}
LIMIT = 10_000  # API maximum per request


def fetch(key, coin, interval, start_ms, end_ms):
    rows, cursor = [], start_ms
    while cursor < end_ms:
        r = requests.get(API, headers={"X-API-Key": key}, timeout=60,
                         params={"coin": coin, "interval": interval, "startTime": cursor, "limit": LIMIT})
        if r.status_code == 429:  # 60 requests/min per key
            time.sleep(int(r.headers.get("Retry-After", "5")))
            continue
        if r.status_code == 403:
            sys.exit(r.json().get("error", r.text))
        r.raise_for_status()
        rows += [row for row in r.json()["data"] if row[0] < end_ms]
        cursor += LIMIT * STEP_MS[interval]
    return rows


def main():
    key = os.environ.get("TIKTAPE_API_KEY", "").strip()
    if not key:
        sys.exit(f"Set TIKTAPE_API_KEY first. Free key (last 30 days, no card): {GET_KEY_URL}")
    coin = sys.argv[1] if len(sys.argv) > 1 else "BTC"
    interval = sys.argv[2] if len(sys.argv) > 2 else "1m"
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    if interval not in STEP_MS:
        sys.exit(f"interval must be one of {' '.join(STEP_MS)}")

    end = int(time.time() * 1000)
    rows = fetch(key, coin, interval, end - days * 86_400_000, end)
    path = f"{coin.replace(':', '_').replace('@', 'spot')}_{interval}.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_ms", "open", "high", "low", "close", "volume"])
        w.writerows(rows)
    print(f"wrote {len(rows)} candles to {path}")


if __name__ == "__main__":
    main()
