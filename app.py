
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.stock_data import (
    get_portfolio_prices,
    get_historical_prices
)

from utils.analytics import (
    calculate_portfolio,
    calculate_portfolio_weights,
    calculate_portfolio_returns,
    calculate_cumulative_returns,
    calculate_risk_metrics
)
from utils.ai_analyst import generate_portfolio_analysis
from utils.chat_manager import (
    initialize_chat,
    clear_chat
)

from utils.ai_agent import chat_with_financial_agent


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
# Default risk metrics in case historical data is unavailable
risk_metrics = {
    "Historical Return": 0.0,
    "Annualized Volatility": 0.0,
    "Maximum Drawdown": 0.0
}
# ==========================================
# ADVANCED FINANCIAL ANALYTICS
# ==========================================

st.divider()

st.header("Advanced Financial Analytics")

# Retrieve historical prices for portfolio stocks
# and S&P 500 benchmark

with st.spinner("Analyzing historical performance..."):

    historical_prices = get_historical_prices(
        tickers + ["^GSPC"],
        period="1y"
    )

if historical_prices.empty:
    st.warning("Historical data is currently unavailable.")

else:
    available_stocks = [
        ticker for ticker in tickers
        if ticker in historical_prices.columns
    ]

    if not available_stocks:
        st.warning("No matching historical stock data found.")

    else:
        # Calculate current portfolio allocation

        weights = calculate_portfolio_weights(results)

        allocation = weights * 100

        st.subheader("Portfolio Diversification")

        allocation_df = pd.DataFrame({
            "Stock": allocation.index,
            "Allocation (%)": allocation.values
        })

        allocation_chart = px.bar(
            allocation_df,
            x="Stock",
            y="Allocation (%)",
            color="Stock",
            title="Current Portfolio Allocation"
        )

        st.plotly_chart(
            allocation_chart,
            use_container_width=True
        )

        # Calculate historical portfolio returns

        portfolio_returns = calculate_portfolio_returns(
            historical_prices[available_stocks],
            weights
        )

        cumulative_returns = calculate_cumulative_returns(
            portfolio_returns
        )

        # Calculate risk metrics

        risk_metrics = calculate_risk_metrics(
            portfolio_returns
        )

        st.subheader("Portfolio Risk Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Historical Return",
            f"{risk_metrics['Historical Return']:.2f}%"
        )

        col2.metric(
            "Annualized Volatility",
            f"{risk_metrics['Annualized Volatility']:.2f}%"
        )

        col3.metric(
            "Maximum Drawdown",
            f"{risk_metrics['Maximum Drawdown']:.2f}%"
        )

        # Historical performance chart

        st.subheader("Historical Portfolio Performance")

        performance_df = pd.DataFrame({
            "Portfolio": cumulative_returns * 100
        })

        # Compare against S&P 500

        if "^GSPC" in historical_prices.columns:

            benchmark_prices = historical_prices["^GSPC"].dropna()

            benchmark_returns = (
                benchmark_prices.pct_change().dropna()
            )

            benchmark_returns = benchmark_returns.reindex(
                portfolio_returns.index
            )

            benchmark_returns = benchmark_returns.dropna()

            if not benchmark_returns.empty:

                aligned_portfolio_returns = (
                    portfolio_returns.reindex(
                        benchmark_returns.index
                    )
                )

                performance_df = pd.DataFrame({
                    "Portfolio": (
                        (1 + aligned_portfolio_returns).cumprod() - 1
                    ) * 100,

                    "S&P 500": (
                        (1 + benchmark_returns).cumprod() - 1
                    ) * 100
                })

        performance_chart = px.line(
            performance_df,
            title="Portfolio vs S&P 500",
            labels={
                "value": "Cumulative Return (%)",
                "index": "Date"
            }
        )

        st.plotly_chart(
            performance_chart,
            use_container_width=True
        )

        st.caption(
            "Historical analysis is illustrative. "
            "It does not guarantee future performance."
        )


# ==========================================
# DUAL MODEL AI FINANCIAL ANALYST
# ==========================================

st.divider()

st.header("🤖 AI Financial Analyst")

st.write(
    "Choose between a locally hosted Llama model "
    "and the OpenAI cloud model."
)

selected_provider = st.selectbox(
    "Select AI Model",
    options=["ollama", "openai"],
    format_func=lambda x: (
        "Llama 3.2 3B (Local)" if x == "ollama"
        else "OpenAI GPT-6 Luna (Cloud)"
    )
)

if selected_provider == "ollama":

    st.success(
        "Local AI selected. Your portfolio prompt "
        "will be processed through Ollama."
    )

else:

    st.info(
        "Cloud AI selected. Portfolio metrics included "
        "in your prompt will be sent to OpenAI."
    )

if st.button("Generate AI Portfolio Analysis"):

    try:

        with st.spinner(
            f"Analyzing with {selected_provider}..."
        ):

            analysis = generate_portfolio_analysis(
                portfolio=results,
                risk_metrics=risk_metrics,
                total_investment=total_investment,
                total_value=total_value,
                total_profit=total_profit,
                total_return=total_return,
                provider=selected_provider
            )

        st.subheader("AI-Generated Financial Insights")

        st.markdown(analysis)

        st.caption(
            f"Generated using: {selected_provider}"
        )



    except Exception as error:

        st.error(
            f"AI analysis failed: {error}"
        )

        st.info(
            "Check your API key, internet connection, "
            "model availability, and Ollama status."
        )



# ==========================================
# AI FINANCIAL CHATBOT
# ==========================================

st.divider()

st.header("💬 AI Financial Assistant")

st.caption(
    "Ask questions about your portfolio, "
    "stock performance and risk."
)

initialize_chat()

# Clear conversation
if st.button("🗑️ Clear Chat", key="clear_financial_chat"):
    clear_chat()
    st.rerun()

# Display conversation history
for message in st.session_state.financial_chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask something about your portfolio..."
)

if question:

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your portfolio..."):

            try:

                answer = chat_with_financial_agent(
                    question=question,
                    portfolio=results,
                    risk_metrics=risk_metrics,
                    conversation_history=(
                        st.session_state.financial_chat_history
                    )
                )

                st.markdown(answer)

            except Exception as e:

                st.error(f"Chatbot error: {e}")

st.caption(
    "Educational financial analysis only. "
    "Not investment advice."
)
