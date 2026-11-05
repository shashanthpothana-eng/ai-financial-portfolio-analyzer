
import yfinance as yf
import pandas as pd
import streamlit as st


@st.cache_data(ttl=300)
def get_stock_price(ticker):
    """
    Retrieve the latest available closing price
    for a stock ticker.
    """

    stock = yf.Ticker(ticker)
    history = stock.history(
        period="5d",
        auto_adjust=True
    )

    if history.empty:
        raise ValueError(f"No stock data found for {ticker}")

    latest_price = history["Close"].dropna().iloc[-1]

    return float(latest_price)


def get_portfolio_prices(tickers):
    """
    Retrieve prices for multiple stocks.
    """

    prices = {}
    errors = {}

    for ticker in tickers:
        try:
            prices[ticker] = get_stock_price(ticker)
        except Exception as error:
            errors[ticker] = str(error)

    return prices, errors


@st.cache_data(ttl=3600)
def get_historical_prices(tickers, period="1y"):
    """
    Download historical adjusted closing prices
    for multiple stocks.
    """

    historical_data = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)

            history = stock.history(
                period=period,
                auto_adjust=True
            )

            if not history.empty:
                historical_data[ticker] = history["Close"]

        except Exception as error:
            print(f"Error retrieving {ticker}: {error}")

    if not historical_data:
        return pd.DataFrame()

    prices = pd.DataFrame(historical_data)

    return prices.dropna(how="all").sort_index()

