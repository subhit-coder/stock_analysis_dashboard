import joblib
from ta.momentum import RSIIndicator
from ta.trend import MACD


def load_model(model_path="trained_model.pkl"):
    return joblib.load(model_path)


def prepare_prediction_data(data, n_lags=3):
    if data.shape[0] < n_lags + 1:
        return None

    recent = data.copy()
    recent["Return"] = recent["Close"].pct_change()
    recent["RSI"] = RSIIndicator(recent["Close"]).rsi()
    macd = MACD(recent["Close"])
    recent["MACD"] = macd.macd()
    recent["Signal"] = macd.macd_signal()

    recent = recent.dropna()
    if recent.empty:
        return None

    last_row = recent.iloc[-1]
    features = [last_row[f"Close_lag_{lag}"] if f"Close_lag_{lag}" in recent.columns else recent["Close"].shift(lag).iloc[-1] for lag in range(1, n_lags + 1)]
    return [features + [last_row["RSI"], last_row["MACD"], last_row["Signal"], last_row["Return"]]]


def predict_next_day(model, data):
    return model.predict(data)
