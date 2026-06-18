# AI Stock Dashboard

A Streamlit-based dashboard for stock analysis, technical indicators, basic portfolio tracking, and risk overview.

## Project Structure

- `app.py` - Main Streamlit dashboard.
- `data/stock_data.py` - Fetches stock data using `yfinance`.
- `indicators/rsi.py` - Calculates RSI.
- `indicators/macd.py` - Calculates MACD.
- `charts/chart_generator.py` - Builds Plotly charts.
- `models/train_model.py` - Training helpers for ML models.
- `models/predictor.py` - Model loading and prediction utilities.
- `portfolio/portfolio_tracker.py` - Basic portfolio tracking.
- `risk/risk_analysis.py` - Risk and volatility calculations.
- `assets/style.css` - Custom Streamlit styling.
- `requirements.txt` - Python dependencies.

## Run the app

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start Streamlit:

```bash
streamlit run app.py
```

## Notes

- `portfolio.csv` will be created automatically when using the portfolio tracker.
- Prediction and model training are scaffolded and can be extended with feature engineering.
