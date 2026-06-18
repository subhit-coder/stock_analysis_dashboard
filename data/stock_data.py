import yfinance as yf


def get_stock_data(symbol: str, period: str = "1y"):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        return history
    except Exception:
        return None


def get_stock_info(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except Exception:
        return {}
