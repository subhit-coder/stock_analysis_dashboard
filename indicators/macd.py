from ta.trend import MACD


def calculate_macd(data):
    if "Close" not in data.columns:
        return data
    macd = MACD(data["Close"])
    data = data.copy()
    data["MACD"] = macd.macd()
    data["Signal"] = macd.macd_signal()
    return data
