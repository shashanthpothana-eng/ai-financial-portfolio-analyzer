
import pandas as pd


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
