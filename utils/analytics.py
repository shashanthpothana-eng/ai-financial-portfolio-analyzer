
import pandas as pd
import numpy as np


def calculate_portfolio(portfolio, prices):

    portfolio = portfolio.copy()

    portfolio["Current Price"] = (
        portfolio["Ticker"].map(prices)
    )

    portfolio = portfolio.dropna(
        subset=["Current Price"]
    )

    portfolio["Investment Value"] = (
        portfolio["Shares"] * portfolio["Average Cost"]
    )

    portfolio["Current Value"] = (
        portfolio["Shares"] * portfolio["Current Price"]
    )

    portfolio["Profit/Loss"] = (
        portfolio["Current Value"]
        - portfolio["Investment Value"]
    )

    portfolio["Return (%)"] = (
        portfolio["Profit/Loss"]
        / portfolio["Investment Value"] * 100
    )

    return portfolio

def calculate_daily_returns(prices):
    """
    Calculate daily percentage returns.
    """
    return prices.pct_change().dropna(how="all")


def calculate_portfolio_weights(portfolio):
    """
    Calculate portfolio allocation percentages
    using current market values.
    """
    total_value = portfolio["Current Value"].sum()

    if total_value <= 0:
        raise ValueError("Portfolio value must be positive.")

    weights = (
        portfolio.set_index("Ticker")["Current Value"]
        / total_value
    )

    return weights


def calculate_portfolio_returns(prices, weights):
    """
    Calculate daily portfolio returns using
    current portfolio weights.

    This is a constant-weight approximation,
    not a daily rebalanced portfolio simulation.
    """

    available_tickers = [
        ticker for ticker in weights.index
        if ticker in prices.columns
    ]

    if not available_tickers:
        raise ValueError("No matching historical prices found.")

    aligned_prices = prices[available_tickers].dropna()

    daily_returns = calculate_daily_returns(aligned_prices)

    active_weights = weights[available_tickers]
    active_weights = active_weights / active_weights.sum()

    portfolio_returns = (
        daily_returns.mul(active_weights, axis=1).sum(axis=1)
    )

    return portfolio_returns


def calculate_cumulative_returns(daily_returns):
    """
    Convert daily returns into cumulative returns.
    """

    return (1 + daily_returns).cumprod() - 1


def calculate_volatility(daily_returns):
    """
    Calculate annualized historical volatility.
    """

    return daily_returns.std() * np.sqrt(252)


def calculate_max_drawdown(daily_returns):
    """
    Calculate maximum peak-to-trough decline.
    """

    cumulative_value = (1 + daily_returns).cumprod()

    running_max = cumulative_value.cummax()

    drawdown = (
        cumulative_value / running_max
    ) - 1

    return drawdown.min()


def calculate_risk_metrics(daily_returns):
    """
    Calculate portfolio risk statistics.
    """

    return {
        "Annualized Volatility": (
            calculate_volatility(daily_returns) * 100
        ),
        "Maximum Drawdown": (
            calculate_max_drawdown(daily_returns) * 100
        ),
        "Historical Return": (
            ((1 + daily_returns).prod() - 1) * 100
        )
    }
