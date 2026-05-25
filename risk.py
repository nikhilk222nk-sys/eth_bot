class RiskManager:

    def calculate_levels(
        self,
        price,
        atr,
        signal
    ):

        if signal == "LONG":

            stop_loss = price - (1.5 * atr)
            take_profit = price + (3 * atr)

        else:

            stop_loss = price + (1.5 * atr)
            take_profit = price - (3 * atr)

        return stop_loss, take_profit