import ta


def add_indicators(df):

    # EMA
    df['ema_fast'] = ta.trend.ema_indicator(
        df['close'],
        window=20
    )

    df['ema_slow'] = ta.trend.ema_indicator(
        df['close'],
        window=50
    )

    # RSI
    df['rsi'] = ta.momentum.rsi(
        df['close'],
        window=14
    )

    # ATR
    df['atr'] = ta.volatility.average_true_range(
        df['high'],
        df['low'],
        df['close'],
        window=14
    )

    # VWAP
    df['vwap'] = ta.volume.volume_weighted_average_price(
        df['high'],
        df['low'],
        df['close'],
        df['volume']
    )

    # MACD
    macd = ta.trend.MACD(
        df['close']
    )

    df['macd'] = macd.macd()

    df['macd_signal'] = macd.macd_signal()

    # STOCHASTIC
    stoch = ta.momentum.StochasticOscillator(
        df['high'],
        df['low'],
        df['close']
    )

    df['stoch'] = stoch.stoch()

    # BOLLINGER
    bollinger = ta.volatility.BollingerBands(
        df['close']
    )

    df['bb_high'] = bollinger.bollinger_hband()

    df['bb_low'] = bollinger.bollinger_lband()

    # RETURNS
    df['returns'] = df['close'].pct_change()

    # VOLATILITY
    df['volatility'] = (
        df['high'] - df['low']
    ) / df['close']

    df.dropna(inplace=True)

    return df