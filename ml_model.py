import joblib
import numpy as np


class MLModel:

    def __init__(self):

        self.model = joblib.load(
            'models/xgb_model.pkl'
        )

    def predict_confidence(

        self,

        ema_fast,
        ema_slow,
        rsi,
        atr,
        volume,
        vwap,
        macd,
        macd_signal,
        stoch,
        bb_high,
        bb_low,
        returns,
        volatility
    ):

        features = np.array([[
            ema_fast,
            ema_slow,
            rsi,
            atr,
            volume,
            vwap,
            macd,
            macd_signal,
            stoch,
            bb_high,
            bb_low,
            returns,
            volatility
        ]])

        prediction = self.model.predict(
            features
        )[0]

        probability = self.model.predict_proba(
            features
        )[0]

        confidence = max(probability) * 100

        if prediction == 1:
            signal = "LONG"
        else:
            signal = "SHORT"

        return signal, confidence