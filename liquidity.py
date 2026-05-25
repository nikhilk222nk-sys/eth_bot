class LiquidityDetector:

    @staticmethod
    def detect_sweep(df):

        last = df.iloc[-1]
        previous = df.iloc[-2]

        high_sweep = (
            last['high'] > previous['high']
            and last['close'] < previous['high']
        )

        low_sweep = (
            last['low'] < previous['low']
            and last['close'] > previous['low']
        )

        if high_sweep:
            return "SELL_SWEEP"

        if low_sweep:
            return "BUY_SWEEP"

        return "NO_SWEEP"