import websocket
import json
import threading


class BinanceWebSocket:

    def __init__(self):

        self.price = None
        self.bid = None
        self.ask = None

    def on_message(self, ws, message):

        try:

            data = json.loads(message)

            if 'data' in data:

                ticker = data['data']

                self.price = float(
                    ticker.get('lastPrice', 0)
                )

                bid = ticker.get('bid1Price')
                ask = ticker.get('ask1Price')

                self.bid = float(bid) if bid else 0
                self.ask = float(ask) if ask else 0

        except Exception as e:

            print(f"WebSocket Error: {e}")

    def on_error(self, ws, error):

        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):

        print("WebSocket Closed")

    def on_open(self, ws):

        print("Bybit WebSocket Connected")

        subscribe_message = {
            "op": "subscribe",
            "args": ["tickers.ETHUSDT"]
        }

        ws.send(json.dumps(subscribe_message))

    def start(self):

        websocket_url = "wss://stream.bybit.com/v5/public/spot"

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