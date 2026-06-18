import pandas as pd
import os

PORTFOLIO_PATH = "portfolio.csv"


def load_portfolio():
    if os.path.exists(PORTFOLIO_PATH):
        return pd.read_csv(PORTFOLIO_PATH)
    return pd.DataFrame(columns=["Stock", "Quantity", "BuyPrice"])


def save_portfolio(portfolio):
    portfolio.to_csv(PORTFOLIO_PATH, index=False)


def add_stock(portfolio, stock, quantity, buy_price):
    row = {"Stock": stock, "Quantity": quantity, "BuyPrice": buy_price}
    return pd.concat([portfolio, pd.DataFrame([row])], ignore_index=True)


def remove_stock(portfolio, stock):
    return portfolio[portfolio["Stock"] != stock]


def calculate_portfolio_value(portfolio, stock_data):
    if portfolio.empty or stock_data is None:
        return 0.0
    latest_price = stock_data["Close"].iloc[-1]
    total = 0.0
    for _, row in portfolio.iterrows():
        total += row["Quantity"] * latest_price
    return total
