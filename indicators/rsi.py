from ta.momentum import RSIIndicator


def calculate_rsi(data):
    if "Close" not in data.columns:
        return None
    rsi = RSIIndicator(data["Close"])
    return rsi.rsi()
