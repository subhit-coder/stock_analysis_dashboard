def calculate_returns(data):
    returns = data["Close"].pct_change()
    return returns


def calculate_volatility(data):
    returns = calculate_returns(data)
    return returns.std()


def risk_score(returns, volatility):
    if volatility == 0 or volatility is None:
        return 0
    score = 10 - min(max(volatility * 100, 0), 10)
    return round(score)
