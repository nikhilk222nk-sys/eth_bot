class OrderFlowAnalyzer:

    @staticmethod
    def calculate_imbalance(bids, asks):

        bid_volume = sum(float(b[1]) for b in bids[:10])
        ask_volume = sum(float(a[1]) for a in asks[:10])

        total = bid_volume + ask_volume

        if total == 0:
            return 0

        imbalance = (bid_volume - ask_volume) / total

        return imbalance

    @staticmethod
    def detect_trade_pressure(trades):

        buy_volume = 0
        sell_volume = 0

        for t in trades:

            qty = float(t['amount'])

            if t['side'] == 'buy':
                buy_volume += qty
            else:
                sell_volume += qty

        delta = buy_volume - sell_volume

        return delta