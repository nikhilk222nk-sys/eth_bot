import websocket
import json
import threading


class BinanceWebSocket:

    def __init__(self):

        self.price = 0
        self.bid = 0
        self.ask = 0

    def on_message(self, ws, message):

        data = json.loads(message)

        if 'data' in data:

            ticker = data['data']

            self.price = float(ticker['price'])
            self.bid = float(ticker['bestBid'])
            self.ask = float(ticker['bestAsk'])

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

        websocket_url = "wss://ws-api-spot.kucoin.com/"

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