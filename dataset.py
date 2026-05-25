import ccxt
import pandas as pd
import ta
import time


exchange = ccxt.binance({
    'enableRateLimit': True
})

symbol = 'ETH/USDT'

all_candles = []

print("Downloading ETH dataset...")

since = exchange.parse8601('2024-01-01T00:00:00Z')

max_batches = 100

for i in range(max_batches):

    try:

        candles = exchange.fetch_ohlcv(
            symbol,
            timeframe='5m',
            since=since,
            limit=1000
        )

        if not candles:
            break

        all_candles.extend(candles)

        since = candles[-1][0] + 1

        print(f"Batch {i+1} | Total candles: {len(all_candles)}")

        time.sleep(1)

    except Exception as e:

        print(f"ERROR: {e}")

        time.sleep(5)


df = pd.DataFrame(
    all_candles,
    columns=[
        'timestamp',
        'open',
        'high',
        'low',
        'close',
        'volume'
    ]
)

print("Generating indicators...")

df['ema_fast'] = ta.trend.ema_indicator(
    df['close'],
    window=20
)

df['ema_slow'] = ta.trend.ema_indicator(
    df['close'],
    window=50
)

df['rsi'] = ta.momentum.rsi(
    df['close'],
    window=14
)

df['atr'] = ta.volatility.average_true_range(
    df['high'],
    df['low'],
    df['close'],
    window=14
)

df['vwap'] = ta.volume.volume_weighted_average_price(
    df['high'],
    df['low'],
    df['close'],
    df['volume']
)

macd = ta.trend.MACD(df['close'])

df['macd'] = macd.macd()
df['macd_signal'] = macd.macd_signal()

stoch = ta.momentum.StochasticOscillator(
    df['high'],
    df['low'],
    df['close']
)

df['stoch'] = stoch.stoch()

bollinger = ta.volatility.BollingerBands(
    df['close']
)

df['bb_high'] = bollinger.bollinger_hband()
df['bb_low'] = bollinger.bollinger_lband()

df['returns'] = df['close'].pct_change()

df['volatility'] = (
    df['high'] - df['low']
) / df['close']

future_close = df['close'].shift(-12)

future_return = (
    future_close - df['close']
) / df['close']

df['target'] = 0

df.loc[future_return > 0.004, 'target'] = 1
df.loc[future_return < -0.004, 'target'] = -1

df.dropna(inplace=True)

print(f"Final rows: {len(df)}")

df.to_csv('eth_dataset.csv', index=False)

print("Dataset saved successfully")