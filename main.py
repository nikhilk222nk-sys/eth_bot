import time
import ccxt
import pandas as pd

from indicators import add_indicators
from orderflow import OrderFlowAnalyzer
from strategy import Strategy
from risk import RiskManager

from btc_filter import BTCFilter
from liquidity import LiquidityDetector
from multi_tf import MultiTF
from ml_model import MLModel

from telegram_alerts import TelegramAlerts


exchange = ccxt.bybit({
    'enableRateLimit': True
})

strategy = Strategy()
risk = RiskManager()

btc = BTCFilter()
multi = MultiTF()
ml = MLModel()

symbol = "ETH/USDT"

while True:

    try:

        # LIVE TICKER
        ticker = exchange.fetch_ticker(symbol)

        live_price = ticker['last']
        bid_price = ticker['bid']
        ask_price = ticker['ask']

        # FETCH CANDLES
        ohlcv = exchange.fetch_ohlcv(
            symbol,
            timeframe='1m',
            limit=200
        )

        df = pd.DataFrame(
            ohlcv,
            columns=[
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume'
            ]
        )

        # ADD INDICATORS
        df = add_indicators(df)

        # ORDER BOOK
        order_book = exchange.fetch_order_book(symbol)

        imbalance = OrderFlowAnalyzer.calculate_imbalance(
            order_book['bids'],
            order_book['asks']
        )

        # RECENT TRADES
        trades = exchange.fetch_trades(
            symbol,
            limit=50
        )

        delta = OrderFlowAnalyzer.detect_trade_pressure(
            trades
        )

        row = df.iloc[-1]

        # STRATEGY SIGNAL
        signal = strategy.generate_signal(
            row,
            imbalance,
            delta
        )

        # BTC FILTER
        btc_trend = btc.btc_trend()

        # MULTI TF FILTER
        higher_tf = multi.higher_tf_trend()

        # LIQUIDITY SWEEP
        sweep = LiquidityDetector.detect_sweep(df)

        # ML PREDICTION
        prediction, confidence = ml.predict_confidence(

            row['ema_fast'],
            row['ema_slow'],
            row['rsi'],
            row['atr'],
            row['volume'],
            row['vwap'],
            row['macd'],
            row['macd_signal'],
            row['stoch'],
            row['bb_high'],
            row['bb_low'],
            row['returns'],
            row['volatility']
        )

        # AI FILTER
        if confidence < 60:
            signal = "NO TRADE"

        # LONG FILTERS
        if signal == "LONG":

            if btc_trend != "BULLISH":
                signal = "NO TRADE"

            if higher_tf != "BULLISH":
                signal = "NO TRADE"

            if sweep == "SELL_SWEEP":
                signal = "NO TRADE"

        # SHORT FILTERS
        if signal == "SHORT":

            if btc_trend != "BEARISH":
                signal = "NO TRADE"

            if higher_tf != "BEARISH":
                signal = "NO TRADE"

            if sweep == "BUY_SWEEP":
                signal = "NO TRADE"

        # TERMINAL OUTPUT
        print("--------------------------------")

        print(f"LIVE PRICE: {live_price}")

        print(f"BID: {bid_price}")

        print(f"ASK: {ask_price}")

        print(f"CANDLE PRICE: {row['close']}")

        print(f"RSI: {row['rsi']:.2f}")

        print(f"IMBALANCE: {imbalance:.2f}")

        print(f"DELTA: {delta:.2f}")

        print(f"BTC TREND: {btc_trend}")

        print(f"HIGHER TF: {higher_tf}")

        print(f"SWEEP: {sweep}")

        print(f"AI PREDICTION: {prediction}")

        print(f"ML CONFIDENCE: {confidence:.2f}%")

        print(f"SIGNAL: {signal}")

        # TRADE LEVELS
        if signal != "NO TRADE":

            stop, take = risk.calculate_levels(
                row['close'],
                row['atr'],
                signal
            )

            print(f"STOP LOSS: {stop}")

            print(f"TAKE PROFIT: {take}")

            # TELEGRAM ALERT
            message = f'''
🚨 ETH AI SIGNAL 🚨

SIGNAL: {signal}

LIVE PRICE: {live_price}

BID: {bid_price}

ASK: {ask_price}

RSI: {row['rsi']:.2f}

IMBALANCE: {imbalance:.2f}

DELTA: {delta:.2f}

BTC TREND: {btc_trend}

HIGHER TF: {higher_tf}

SWEEP: {sweep}

AI CONFIDENCE: {confidence:.2f}%

STOP LOSS: {stop}

TAKE PROFIT: {take}
'''

            TelegramAlerts.send_message(message)

        time.sleep(10)

    except Exception as e:

        print(f"ERROR: {e}")

        time.sleep(5)