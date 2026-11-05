
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
