
import yfinance as yf
import pandas as pd
import numpy as np


def research_stock(ticker):

    ticker = ticker.strip().upper()

    stock = yf.Ticker(ticker)

    history = stock.history(period="1y")

    if history.empty:
        return {
            "error": f"No market data found for {ticker}."
        }

    prices = history["Close"].dropna()

    daily_returns = prices.pct_change().dropna()

    current_price = float(prices.iloc[-1])

    annualized_volatility = (
        daily_returns.std() * np.sqrt(252) * 100
    )

    cumulative_returns = (
        (1 + daily_returns).cumprod()
    )

    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns / running_max
    ) - 1

    info = stock.info

    return {
        "ticker": ticker,
        "company_name": info.get("longName", ticker),
        "current_price": round(current_price, 2),
        "annualized_volatility": round(
            float(annualized_volatility), 2
        ),
        "maximum_drawdown": round(
            float(drawdown.min() * 100), 2
        ),
        "one_year_return": round(
            float((prices.iloc[-1] / prices.iloc[0] - 1) * 100),
            2
        ),
        "market_cap": info.get("marketCap"),
        "revenue": info.get("totalRevenue"),
        "profit_margin": info.get("profitMargins"),
        "sector": info.get("sector"),
        "industry": info.get("industry")
    }
