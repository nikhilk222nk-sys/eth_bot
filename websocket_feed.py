import websocket
import json
import threading


class BinanceWebSocket:

    def __init__(self):

        self.price = 0
        self.bid = 0
        self.ask = 0

    def on_message(self, ws, message):

        try:

            data = json.loads(message)

            # Ignore non-dict messages
            if not isinstance(data, dict):
                return

            # Ignore messages without market data
            if 'data' not in data:
                return

            ticker = data['data']

            # Ignore if ticker is not dict
            if not isinstance(ticker, dict):
                return

            self.price = float(
                ticker.get('price', 0)
            )

            self.bid = float(
                ticker.get('bestBid', 0)
            )

            self.ask = float(
                ticker.get('bestAsk', 0)
            )

        except Exception as e:

            print(f"WebSocket Error: {e}")

    def on_error(self, ws, error):

        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):

        print("WebSocket Closed")

    def on_open(self, ws):

        print("KuCoin WebSocket Connected")

        subscribe_message = {
            "id": "1",
            "type": "subscribe",
            "topic": "/market/ticker:ETH-USDT",
            "privateChannel": False,
            "response": True
        }

        ws.send(json.dumps(subscribe_message))

    def start(self):

        websocket_url = "wss://ws-api-spot.kucoin.com"

        ws = websocket.WebSocketApp(
            websocket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        thread = threading.Thread(
            target=ws.run_forever
        )

        thread.daemon = True

        thread.start()