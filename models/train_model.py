import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from ta.momentum import RSIIndicator
from ta.trend import MACD
import joblib


def prepare_training_data(data, n_lags=3):
    data = data.copy()
    data["Return"] = data["Close"].pct_change()
    data["RSI"] = RSIIndicator(data["Close"]).rsi()
    macd = MACD(data["Close"])
    data["MACD"] = macd.macd()
    data["Signal"] = macd.macd_signal()

    for lag in range(1, n_lags + 1):
        data[f"Close_lag_{lag}"] = data["Close"].shift(lag)

    data = data.dropna()
    if data.empty:
        return None, None

    feature_columns = [f"Close_lag_{lag}" for lag in range(1, n_lags + 1)] + ["RSI", "MACD", "Signal", "Return"]
    return data[feature_columns], data["Close"]


def train_model(data, target_column="Close", model_type="linear"):
    features, target = prepare_training_data(data)
    if features is None or features.empty:
        return None, None

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    if model_type == "random_forest":
        model = RandomForestRegressor(random_state=42)
    elif model_type == "xgboost":
        model = XGBRegressor(random_state=42, verbosity=0)
    else:
        model = LinearRegression()

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    joblib.dump(model, "trained_model.pkl")
    return model, mse
