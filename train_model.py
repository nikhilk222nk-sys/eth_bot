import pandas as pd
import joblib

from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier


print("Loading professional dataset...")

df = pd.read_csv('eth_dataset.csv')

features = [

    'ema_fast',
    'ema_slow',
    'rsi',
    'atr',
    'volume',
    'vwap',
    'macd',
    'macd_signal',
    'stoch',
    'bb_high',
    'bb_low',
    'returns',
    'volatility'
]

# REMOVE NO-TRADE ROWS
df = df[df['target'] != 0]

# CONVERT TARGETS
# -1 -> 0
# 1 -> 1

df['target'] = df['target'].replace({
    -1: 0,
     1: 1
})

X = df[features]

y = df['target']

print(f"Dataset size: {len(df)}")

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training professional AI model...")

model = XGBClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"REAL Accuracy: {accuracy * 100:.2f}%")

joblib.dump(
    model,
    'models/xgb_model.pkl'
)

print("Professional AI model saved")