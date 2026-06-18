import streamlit as st
from datetime import datetime

from data.stock_data import get_stock_data, get_stock_info
from charts.chart_generator import (
    create_candlestick,
    create_rsi_chart,
    create_macd_chart
)

from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd

from models.train_model import train_model
from models.predictor import (
    load_model,
    predict_next_day,
    prepare_prediction_data
)

from portfolio.portfolio_tracker import (
    load_portfolio,
    save_portfolio,
    add_stock,
    remove_stock,
    calculate_portfolio_value
)

from risk.risk_analysis import (
    calculate_returns,
    calculate_volatility,
    risk_score
)

# ============================================================
# PAGE CONFIG & THEME
# ============================================================

st.set_page_config(
    page_title="AI Stock Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': "https://github.com",
        'About': "### AI Stock Analytics Dashboard\nPowered by Streamlit, Plotly & yFinance"
    }
)

# ============================================================
# MODERNIZED CUSTOM CSS (UI/UX ENHANCEMENTS)
# ============================================================

st.markdown("""
    <style>
        /* Main container spacing */
        .main {
            padding: 1rem 2rem;
            font-family: 'Inter', sans-serif;
        }
        
        /* Sleek Animated Header Gradient */
        .header-gradient {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            padding: 40px 30px;
            border-radius: 20px;
            color: white;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .header-gradient:hover {
            transform: translateY(-2px);
        }
        .header-gradient h1 {
            margin: 0;
            font-size: 3.2em;
            font-weight: 800;
            letter-spacing: -1px;
            color: #ffffff !important;
        }
        .header-gradient p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            font-weight: 300;
            opacity: 0.9;
            color: #e0e0e0 !important;
            letter-spacing: 0.5px;
        }
        
        /* Modernized Section Headers with Underline Animation */
        .section-header {
            color: #1f77b4 !important;
            font-size: 1.8em;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 25px;
            position: relative;
            padding-bottom: 10px;
        }
        .section-header::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            height: 4px;
            width: 60px;
            background: linear-gradient(90deg, #1f77b4, #3498db);
            border-radius: 2px;
            transition: width 0.3s ease;
        }
        .section-header:hover::after {
            width: 100px;
        }
        
        /* Streamlit Native Metric Cards Upgrade */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(128, 128, 128, 0.2);
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            border-left: 4px solid #3498db;
        }
        [data-testid="stMetric"]:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            transform: translateY(-3px);
            border-left: 4px solid #1f77b4;
        }
        
        /* Enhanced Info Boxes with Hover Effects */
        .info-box, .success-box, .warning-box {
            padding: 20px !important;
            border-radius: 12px !important;
            margin: 15px 0 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
            transition: all 0.2s ease;
        }
        .info-box:hover, .success-box:hover, .warning-box:hover {
            transform: translateX(5px);
        }
        
        .info-box { 
            background: #f1f8ff !important; 
            border-left: 6px solid #0366d6 !important; 
        }
        .success-box { 
            background: #f0fff4 !important; 
            border-left: 6px solid #28a745 !important; 
        }
        .warning-box { 
            background: #fff8f2 !important; 
            border-left: 6px solid #e36209 !important; 
        }
        
        /* Strict Typography Colors for readability across dark/light mode */
        .info-box b, .info-box span, .info-box div { color: #032f62 !important; }
        .success-box b, .success-box span, .success-box div { color: #144620 !important; }
        .warning-box b, .warning-box span, .warning-box div { color: #5c2505 !important; }
        
        /* Clean Footer */
        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
            font-size: 0.9em;
            color: #888;
        }
        .footer b { color: #1f77b4 !important; }
        
        /* Subtle divider styling */
        hr {
            margin: 30px 0;
            border: none;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
        }
        
        /* Streamlit Button Hover State */
        .stButton button {
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        .stButton button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# POPULAR STOCKS DATABASE
# ============================================================

POPULAR_STOCKS = {
    "🇮🇳 INDIAN STOCKS": {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "SBI": "SBIN.NS",
        "ITC": "ITC.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Bajaj Auto": "BAJAJAUTOP.NS",
        "Wipro": "WIPRO.NS",
    },
    "🌍 GLOBAL STOCKS": {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
        "Meta": "META",
        "NVIDIA": "NVDA",
        "Netflix": "NFLX",
        "Coca Cola": "KO",
        "JPMorgan": "JPM",
    }
}

FLAT_STOCKS = {}
for category, stocks in POPULAR_STOCKS.items():
    FLAT_STOCKS.update(stocks)

# ============================================================
# SIDEBAR CONFIGURATION
# ============================================================

with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    
    # Input method selection
    input_method = st.radio(
        "📌 Stock Selection",
        ["📑 Popular Stocks", "🔍 Search Symbol"],
        horizontal=False
    )
    
    st.divider()
    
    # Stock Selection
    if input_method == "📑 Popular Stocks":
        category = st.selectbox(
            "Select Category",
            list(POPULAR_STOCKS.keys()),
            key="category_select"
        )
        
        company = st.selectbox(
            "Select Company",
            list(POPULAR_STOCKS[category].keys()),
            key="company_select"
        )
        
        symbol = POPULAR_STOCKS[category][company]
        st.info(f"**Selected:** {company} ({symbol})")
    else:
        symbol = st.text_input(
            "Enter Stock Symbol",
            value="RELIANCE.NS",
            placeholder="e.g., AAPL, GOOGL, RELIANCE.NS"
        )
    
    st.divider()
    
    # Timeframe Selection
    timeframe = st.selectbox(
        "📅 Timeframe",
        ["1mo", "3mo", "6mo", "1y", "5y"],
        index=4
    )
    
    st.divider()
    
    # Section Selection
    section = st.radio(
        "📑 Analysis Section",
        [
            "📊 Overview",
            "📈 Indicators",
            "🤖 Prediction",
            "💼 Portfolio",
            "⚠️ Risk Analysis"
        ]
    )
    
    st.divider()
    st.caption(f"⏰ Updated: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# DATA LOADING
# ============================================================

stock_data = get_stock_data(symbol, period=timeframe)
stock_info = get_stock_info(symbol)

if stock_data is None or stock_data.empty:
    st.error("❌ No stock data found for this symbol. Please try a different ticker.")
    st.stop()

# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(f"""
    <div class="header-gradient">
        <h1>📈 AI Stock Analytics Dashboard</h1>
        <p>Advanced Analytics & Intelligent Predictions | {symbol}</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# OVERVIEW SECTION
# ============================================================

if "Overview" in section:

    st.markdown('<h2 class="section-header">🏢 Company Overview</h2>', unsafe_allow_html=True)
    
    # Key Metrics - 4 Columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        current_price = stock_data['Close'].iloc[-1]
        st.metric(
            "💰 Current Price",
            f"${current_price:.2f}"
        )

    with col2:
        day_high = stock_data['High'].iloc[-1]
        st.metric(
            "📈 Day High",
            f"${day_high:.2f}"
        )

    with col3:
        day_low = stock_data['Low'].iloc[-1]
        st.metric(
            "📉 Day Low",
            f"${day_low:.2f}"
        )
    
    with col4:
        price_change = stock_data['Close'].iloc[-1] - stock_data['Open'].iloc[-1]
        change_pct = (price_change / stock_data['Open'].iloc[-1]) * 100
        st.metric(
            "📊 Change",
            f"${abs(price_change):.2f}",
            delta=f"{change_pct:.2f}%"
        )

    st.markdown("---")

    # Company Information
    company_name = stock_info.get("longName", symbol)
    sector = stock_info.get("sector", "N/A")
    industry = stock_info.get("industry", "N/A")
    country = stock_info.get("country", "N/A")
    employees = stock_info.get("fullTimeEmployees", "N/A")
    website = stock_info.get("website", "N/A")
    market_cap = stock_info.get("marketCap", "N/A")

    st.markdown(f'<h3 style="color: #1f77b4; margin-top: 20px; font-weight: 700;">{company_name}</h3>', unsafe_allow_html=True)

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.markdown(f"🏭 **Sector:** {sector}")
        st.markdown(f"🏢 **Industry:** {industry}")

    with info_col2:
        st.markdown(f"🌍 **Country:** {country}")
        employee_str = f"{employees:,}" if isinstance(employees, int) else str(employees)
        st.markdown(f"👥 **Employees:** {employee_str}")

    with info_col3:
        st.markdown(f"📊 **Market Cap:** {market_cap}")
        if website != "N/A":
            website_clean = website.replace('https://', '').replace('http://', '')
            st.markdown(f"🔗 **Website:** [{website_clean}]({website})")

    # Chairman Info
    officers = stock_info.get("companyOfficers", [])
    if len(officers) > 0:
        chairman = officers[0].get("name", "N/A")
        st.markdown(f'<div class="info-box"><b>👔 Chairman:</b> <span>{chairman}</span></div>', unsafe_allow_html=True)

    # Company Summary
    summary = stock_info.get("longBusinessSummary", "")
    if summary:
        st.markdown('<h3 style="color: #1f77b4; margin-top: 25px; font-weight: 700;">📖 Company Summary</h3>', unsafe_allow_html=True)
        summary_text = summary[:1500] + "..." if len(summary) > 1500 else summary
        st.markdown(f'<div class="info-box"><span>{summary_text}</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Candlestick Chart
    st.markdown('<h3 class="section-header">📊 Price Movement Chart</h3>', unsafe_allow_html=True)
    st.plotly_chart(
        create_candlestick(stock_data, symbol),
        use_container_width=True
    )

# ============================================================
# INDICATORS SECTION
# ============================================================

elif "Indicators" in section:

    st.markdown('<h2 class="section-header">📈 Technical Indicators</h2>', unsafe_allow_html=True)

    stock_data = calculate_macd(stock_data)
    stock_data["RSI"] = calculate_rsi(stock_data)

    # Indicator Descriptions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-box"><b>RSI</b><br/><span>Relative Strength Index<br/><small>0-100 Scale | Overbought >70 | Oversold <30</small></span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box"><b>MACD</b><br/><span>Moving Average Convergence<br/><small>Momentum & Trend Indicator</small></span></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-box"><b>Candlestick</b><br/><span>OHLC Data<br/><small>Open, High, Low, Close Prices</small></span></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Charts
    st.plotly_chart(
        create_candlestick(stock_data, symbol),
        use_container_width=True
    )

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.plotly_chart(
            create_rsi_chart(stock_data),
            use_container_width=True
        )

    with col_right:
        st.plotly_chart(
            create_macd_chart(stock_data),
            use_container_width=True
        )

# ============================================================
# PREDICTION SECTION
# ============================================================

elif "Prediction" in section:

    st.markdown('<h2 class="section-header">🤖 Stock Price Prediction</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    
    with col1:
        model_type = st.selectbox(
            "Select ML Model",
            ["linear", "random_forest", "xgboost"],
            help="Choose the machine learning model for predictions"
        )
    
    with col2:
        # Added a little vertical space so the button aligns better with the selectbox
        st.write("") 
        train_btn = st.button("🔄 Train Model", use_container_width=True)

    if train_btn:
        with st.spinner("⏳ Training model..."):
            model, mse = train_model(stock_data, model_type=model_type)

            if model is not None:
                st.markdown(
                    '<div class="success-box"><b>✅ Model trained successfully!</b></div>',
                    unsafe_allow_html=True
                )
                st.metric("Validation MSE", f"{mse:.4f}")
            else:
                st.error("❌ Insufficient data for training")

    st.markdown("---")

    try:
        model = load_model()
        prediction_input = prepare_prediction_data(stock_data)

        if prediction_input is not None:
            prediction = predict_next_day(model, prediction_input)[0]
            current = stock_data['Close'].iloc[-1]
            change = ((prediction - current) / current) * 100

            pred_col1, pred_col2, pred_col3 = st.columns(3)

            with pred_col1:
                st.metric(
                    "💰 Current Price",
                    f"${current:.2f}"
                )

            with pred_col2:
                st.metric(
                    "🔮 Predicted Close",
                    f"${prediction:.2f}"
                )

            with pred_col3:
                st.metric(
                    "📊 Expected Change",
                    f"{change:.2f}%",
                    delta=f"{'↑' if change > 0 else '↓'} {abs(change):.2f}%"
                )

            st.markdown(
                '<div class="warning-box"><b>⚠️ Disclaimer:</b> <span>Predictions are based on historical data only. Not investment advice. Always consult a financial advisor.</span></div>',
                unsafe_allow_html=True
            )

    except FileNotFoundError:
        st.markdown(
            '<div class="warning-box"><b>⚠️ No Model Found</b><br/><span>Train a model first to make predictions</span></div>',
            unsafe_allow_html=True
        )

# ============================================================
# PORTFOLIO SECTION
# ============================================================

elif "Portfolio" in section:

    st.markdown('<h2 class="section-header">💼 Portfolio Tracker</h2>', unsafe_allow_html=True)

    portfolio = load_portfolio()

    if not portfolio.empty:
        st.markdown("##### 📋 Your Holdings")
        st.dataframe(portfolio, use_container_width=True, height=300)
    else:
        st.info("📝 Your portfolio is empty. Add stocks below!")

    st.markdown("---")

    st.markdown("##### ➕ Add Stock to Portfolio")

    with st.form("portfolio_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            stock = st.text_input("Stock Symbol", placeholder="AAPL")

        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)

        with col3:
            price = st.number_input("Buy Price ($)", min_value=0.0, value=100.0)

        submitted = st.form_submit_button("➕ Add Stock", use_container_width=True)

        if submitted and stock:
            portfolio = add_stock(portfolio, stock.upper(), int(quantity), float(price))
            save_portfolio(portfolio)
            st.markdown(
                f'<div class="success-box"><b>✅ {stock.upper()}</b> <span>added to portfolio!</span></div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    if not portfolio.empty:
        try:
            value = calculate_portfolio_value(portfolio, stock_data)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💵 Total Portfolio Value", f"${value:.2f}")
        except:
            st.warning("⚠️ Could not calculate portfolio value. Check stock symbols.")

# ============================================================
# RISK ANALYSIS SECTION
# ============================================================

elif "Risk Analysis" in section:

    st.markdown('<h2 class="section-header">⚠️ Risk Analysis</h2>', unsafe_allow_html=True)

    returns = calculate_returns(stock_data)
    volatility = calculate_volatility(stock_data)
    score = risk_score(returns, volatility)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 Volatility", f"{volatility:.4f}")

    with col2:
        st.metric("⚠️ Risk Score", f"{score:.2f}/10")

    with col3:
        st.metric("📈 Latest Return", f"{returns.iloc[-1]:.4f}")

    st.markdown("---")

    # Risk Level Assessment
    st.markdown('<h3 style="color: #1f77b4; font-weight: 700;">Risk Assessment:</h3>', unsafe_allow_html=True)

    if score < 3:
        risk_level = "🟢 LOW RISK"
        risk_desc = "Conservative investment with lower volatility"
    elif score < 6:
        risk_level = "🟡 MODERATE RISK"
        risk_desc = "Balanced risk-reward profile"
    else:
        risk_level = "🔴 HIGH RISK"
        risk_desc = "Aggressive with high price volatility"

    st.markdown(f'<div class="info-box"><b>{risk_level}</b><br/><span>{risk_desc}<br/><small>Volatility: {volatility:.4f} | Risk Score: {score:.2f}/10</small></span></div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'<div class="info-box"><b>📌 What is Volatility?</b><br/><span>Measures how much price fluctuates. Higher volatility = Higher risk & higher potential returns.</span></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="info-box"><b>📊 Risk Score Levels:</b><br/><span>0-3: Low | 3-6: Moderate | 6-10: High</span></div>',
            unsafe_allow_html=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
    <div class="footer">
        <b>🚀 AI Stock Analytics Dashboard</b><br/>
        Built with ❤️ using Streamlit • Plotly • yFinance • Scikit-Learn<br/>
        <small>⚠️ For educational purposes only. Not financial advice. Always consult a financial advisor.</small>
    </div>
""", unsafe_allow_html=True)