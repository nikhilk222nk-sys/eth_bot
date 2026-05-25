import websocket
import json


class BinanceWebSocket:

    def __init__(self):

        self.price = None
        self.bid = None
        self.ask = None

    def on_message(self, ws, message):

        data = json.loads(message)

        self.price = float(data['c'])

        self.bid = float(data['b'])

        self.ask = float(data['a'])

    def on_error(self, ws, error):

        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):

        print("WebSocket Closed")

    def on_open(self, ws):

        print("Binance WebSocket Connected")

    def start(self):

        socket = "wss://stream.binance.com:9443/ws/ethusdt@ticker"

        ws = websocket.WebSocketApp(
            socket,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        ws.run_forever()