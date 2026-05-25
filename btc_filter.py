import ccxt


class BTCFilter:

    def __init__(self):

        self.exchange = ccxt.binance()

    def btc_trend(self):

        candles = self.exchange.fetch_ohlcv(
            'BTC/USDT',
            timeframe='5m',
            limit=50
        )

        closes = [c[4] for c in candles]

        ema_fast = sum(closes[-10:]) / 10
        ema_slow = sum(closes[-30:]) / 30

        if ema_fast > ema_slow:
            return "BULLISH"

        return "BEARISH"