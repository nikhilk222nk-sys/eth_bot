from binance.client import Client
from config import API_KEY, API_SECRET


client = Client(API_KEY, API_SECRET)


class Executor:

    def place_market_order(
        self,
        symbol,
        side,
        quantity
    ):

        order = client.futures_create_order(
            symbol=symbol.replace("/", ""),
            side=side,
            type='MARKET',
            quantity=quantity
        )

        return order