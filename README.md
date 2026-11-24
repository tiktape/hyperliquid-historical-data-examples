# Hyperliquid historical data examples

Runnable Python for getting Hyperliquid historical candles (OHLCV), including
data older than the official API's 5000-candle window.

## The limit

Hyperliquid's `candleSnapshot` info request serves
["only the most recent 5000 candles"](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
per coin and interval: about 3.5 days of 1m bars. The official S3 archive has L2
book snapshots, asset contexts and node fills, but
["no other historical data sets ... (e.g. candles)"](https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data).

See it yourself (no key needed):

```bash
pip install requests
python official_api_limit.py
# asked for 7 days (10080 candles) from ...
# got 5000 candles, earliest ...
```

## Getting older candles

`download_ohlcv.py` pages through the [TikTape](https://tiktape.xyz/?utm_source=github&utm_medium=readme&utm_campaign=hl-data-examples)
archive, 10,000 candles per request, and writes CSV:

```bash
TIKTAPE_API_KEY=tt_... python download_ohlcv.py BTC 1m 7
# wrote 10080 candles to BTC_1m.csv
```

- 800+ markets: perps, spot (`@1`) and HIP-3 (`cash:NVDA`); intervals 1m to 1w.
- Rows are `[timestamp_ms, open, high, low, close, volume]`; prices are strings.
- Free API key (most recent 30 days, no card):
  [tiktape.xyz](https://tiktape.xyz/?utm_source=github&utm_medium=readme&utm_campaign=hl-data-examples#freeKeyCard).
  Full history back to 2025-03-23 is a paid plan.

Using CCXT? [ccxt-tiktape](https://github.com/tiktape/ccxt-tiktape) is a
drop-in `ccxt.hyperliquid` subclass with the same `fetch_ohlcv()` signature.

## More answers

- [Why the API stops at 5,000 candles](https://tiktape.xyz/learn/hyperliquid-5000-candle-limit?utm_source=github&utm_medium=readme&utm_campaign=hl-data-examples)
- [Where Hyperliquid historical data lives (API, S3, archives)](https://tiktape.xyz/learn/hyperliquid-historical-data-sources?utm_source=github&utm_medium=readme&utm_campaign=hl-data-examples)
- [Tick and trade data](https://tiktape.xyz/learn/hyperliquid-tick-data?utm_source=github&utm_medium=readme&utm_campaign=hl-data-examples)

## License

MIT for the code. Market data is subject to the
[TikTape terms](https://tiktape.xyz/terms-and-conditions) and Hyperliquid's own terms.
