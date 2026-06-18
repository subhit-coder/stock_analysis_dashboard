import plotly.graph_objects as go


def create_candlestick(data, symbol):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=symbol,
            )
        ]
    )
    fig.update_layout(title_text=f"{symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
    return fig


def create_rsi_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], name="RSI", line_color="orange"))
    fig.update_layout(title_text="RSI", xaxis_title="Date", yaxis_title="RSI")
    return fig


def create_macd_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["MACD"], name="MACD", line_color="cyan"))
    fig.add_trace(go.Scatter(x=data.index, y=data["Signal"], name="Signal", line_color="magenta"))
    fig.update_layout(title_text="MACD", xaxis_title="Date", yaxis_title="Value")
    return fig
