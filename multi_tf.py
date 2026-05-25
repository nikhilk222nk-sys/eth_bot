import ccxt


class MultiTF:

    def __init__(self):

        self.exchange = ccxt.binance()

    def higher_tf_trend(self):

        candles = self.exchange.fetch_ohlcv(
            'ETH/USDT',
            timeframe='15m',
            limit=100
        )

        closes = [c[4] for c in candles]

        fast = sum(closes[-20:]) / 20
        slow = sum(closes[-50:]) / 50

        if fast > slow:
            return "BULLISH"

        return "BEARISH"