class Strategy:

    def generate_signal(
        self,
        row,
        imbalance,
        delta
    ):

        long_conditions = [

            row['ema_fast'] > row['ema_slow'],
            row['rsi'] > 55,
            imbalance > 0.15,
            delta > 0
        ]

        short_conditions = [

            row['ema_fast'] < row['ema_slow'],
            row['rsi'] < 45,
            imbalance < -0.15,
            delta < 0
        ]

        if all(long_conditions):
            return "LONG"

        if all(short_conditions):
            return "SHORT"

        return "NO TRADE"