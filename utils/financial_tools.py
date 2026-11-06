
import pandas as pd

from utils.analytics import (
    calculate_portfolio_weights,
)

from utils.stock_research import research_stock



def get_portfolio_summary(portfolio):
    """Return overall portfolio performance."""

    total_investment = portfolio["Investment Value"].sum()
    total_value = portfolio["Current Value"].sum()
    total_profit = portfolio["Profit/Loss"].sum()

    total_return = (
        total_profit / total_investment * 100
        if total_investment > 0 else 0
    )

    return {
        "total_holdings": len(portfolio),
        "total_investment": round(float(total_investment), 2),
        "current_value": round(float(total_value), 2),
        "unrealized_profit_loss": round(float(total_profit), 2),
        "total_return_percent": round(float(total_return), 2),
    }


def get_stock_performance(portfolio, ticker):
    """Return performance for a particular stock."""

    ticker = ticker.upper()

    stock = portfolio[
        portfolio["Ticker"].str.upper() == ticker
    ]

    if stock.empty:
        return {"error": f"{ticker} is not in your portfolio."}

    row = stock.iloc[0]

    return {
        "ticker": ticker,
        "shares": float(row["Shares"]),
        "average_cost": round(float(row["Average Cost"]), 2),
        "current_price": round(float(row["Current Price"]), 2),
        "investment_value": round(float(row["Investment Value"]), 2),
        "current_value": round(float(row["Current Value"]), 2),
        "profit_loss": round(float(row["Profit/Loss"]), 2),
        "return_percent": round(float(row["Return (%)"]), 2),
    }


def get_portfolio_allocation(portfolio):
    """Calculate allocation percentage for each holding."""

    weights = calculate_portfolio_weights(portfolio)

    return {
        ticker: round(float(weight * 100), 2)
        for ticker, weight in weights.items()
    }


def get_risk_metrics(risk_metrics):
    """Return existing calculated portfolio risk metrics."""

    return {
        key: round(float(value), 2)
        for key, value in risk_metrics.items()
    }


def compare_stocks(portfolio, ticker1, ticker2):
    """Compare two stocks in the portfolio."""

    first = get_stock_performance(portfolio, ticker1)
    second = get_stock_performance(portfolio, ticker2)

    if "error" in first:
        return first

    if "error" in second:
        return second

    return {
        "stock_1": first,
        "stock_2": second,
        "higher_return": (
            ticker1.upper()
            if first["return_percent"] > second["return_percent"]
            else ticker2.upper()
            if second["return_percent"] > first["return_percent"]
            else "Equal"
        )
    }

def compare_external_stocks(ticker1, ticker2):
    """
    Compare two stocks using external financial research.
    """

    ticker1 = ticker1.upper().strip()
    ticker2 = ticker2.upper().strip()

    if ticker1 == ticker2:
        return {"error": "Please provide two different stock tickers."}

    first = research_stock(ticker1)
    second = research_stock(ticker2)

    if "error" in first:
        return first

    if "error" in second:
        return second

    return {
        "stock_1": first,
        "stock_2": second,

        "higher_one_year_return": (
            ticker1
            if first["one_year_return"] > second["one_year_return"]
            else ticker2
            if second["one_year_return"] > first["one_year_return"]
            else "Equal"
        ),

        "lower_volatility": (
            ticker1
            if first["annualized_volatility"] < second["annualized_volatility"]
            else ticker2
            if second["annualized_volatility"] < first["annualized_volatility"]
            else "Equal"
        )
    }
