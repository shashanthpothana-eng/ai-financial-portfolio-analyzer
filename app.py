
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.stock_data import get_portfolio_prices
from utils.analytics import calculate_portfolio


st.set_page_config(
    page_title="AI Financial Portfolio Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Financial Portfolio Analyzer")

st.write(
    "Analyze your stock portfolio and monitor "
    "your investment performance."
)

st.info(
    "Demo application. Enter sample holdings or "
    "your own data. Prices are latest available "
    "market closes, not necessarily real-time."
)

# Sample portfolio
sample_data = pd.DataFrame({
    "Ticker": ["AAPL", "NVDA", "MSFT"],
    "Shares": [5, 3, 4],
    "Average Cost": [180.0, 120.0, 400.0]
})

st.subheader("Your Portfolio")

portfolio = st.data_editor(
    sample_data,
    num_rows="dynamic",
    use_container_width=True
)

# Clean user input
portfolio["Ticker"] = (
    portfolio["Ticker"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

portfolio["Shares"] = pd.to_numeric(
    portfolio["Shares"],
    errors="coerce"
)

portfolio["Average Cost"] = pd.to_numeric(
    portfolio["Average Cost"],
    errors="coerce"
)

portfolio = portfolio[
    (portfolio["Ticker"] != "")
    & (portfolio["Shares"] > 0)
    & (portfolio["Average Cost"] > 0)
]

if portfolio.empty:
    st.warning("Please enter at least one valid holding.")
    st.stop()

if portfolio["Ticker"].duplicated().any():
    st.error("Please enter each stock ticker only once.")
    st.stop()

# Fetch stock prices
tickers = portfolio["Ticker"].tolist()

with st.spinner("Fetching market data..."):
    prices, errors = get_portfolio_prices(tickers)

if errors:
    st.warning("Some stock prices could not be retrieved.")
    for ticker, error in errors.items():
        st.write(f"{ticker}: {error}")

# Calculate portfolio
results = calculate_portfolio(portfolio, prices)

if results.empty:
    st.error("No valid stock prices were retrieved.")
    st.stop()

# Portfolio metrics
total_investment = results["Investment Value"].sum()
total_value = results["Current Value"].sum()
total_profit = results["Profit/Loss"].sum()

total_return = (
    total_profit / total_investment * 100
    if total_investment > 0 else 0
)

st.subheader("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Investment",
    f"${total_investment:,.2f}"
)

col2.metric(
    "Current Value",
    f"${total_value:,.2f}"
)

col3.metric(
    "Profit / Loss",
    f"${total_profit:,.2f}"
)

col4.metric(
    "Total Return",
    f"{total_return:.2f}%"
)

# Portfolio table
st.subheader("Stock Performance")

st.dataframe(
    results.style.format({
        "Shares": "{:.2f}",
        "Average Cost": "${:.2f}",
        "Current Price": "${:.2f}",
        "Investment Value": "${:,.2f}",
        "Current Value": "${:,.2f}",
        "Profit/Loss": "${:,.2f}",
        "Return (%)": "{:.2f}%"
    }),
    use_container_width=True
)

# Portfolio allocation
st.subheader("Portfolio Allocation")

fig = px.pie(
    results,
    names="Ticker",
    values="Current Value",
    title="Portfolio Distribution",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# Individual stock performance
st.subheader("Individual Stock Performance")

bar_chart = px.bar(
    results,
    x="Ticker",
    y="Profit/Loss",
    color="Profit/Loss",
    title="Profit and Loss by Stock"
)

st.plotly_chart(bar_chart, use_container_width=True)

st.caption(
    "Educational project only. Not financial or investment advice."
)
