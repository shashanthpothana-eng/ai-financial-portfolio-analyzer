
import pandas as pd

from utils.financial_tools import (
    get_portfolio_summary,
    get_stock_performance,
    get_portfolio_allocation,
    compare_stocks,
)

# Sample portfolio for testing
portfolio = pd.DataFrame([
    {
        "Ticker": "AAPL",
        "Shares": 5,
        "Average Cost": 180,
        "Current Price": 346.33,
        "Investment Value": 900,
        "Current Value": 1731.65,
        "Profit/Loss": 831.65,
        "Return (%)": 92.41,
    },
    {
        "Ticker": "NVDA",
        "Shares": 3,
        "Average Cost": 120,
        "Current Price": 184.40,
        "Investment Value": 360,
        "Current Value": 553.20,
        "Profit/Loss": 193.20,
        "Return (%)": 53.67,
    },
    {
        "Ticker": "MSFT",
        "Shares": 4,
        "Average Cost": 400,
        "Current Price": 539.63,
        "Investment Value": 1600,
        "Current Value": 2158.52,
        "Profit/Loss": 558.52,
        "Return (%)": 34.91,
    },
])

print("\nPORTFOLIO SUMMARY")
print(get_portfolio_summary(portfolio))

print("\nAPPLE PERFORMANCE")
print(get_stock_performance(portfolio, "AAPL"))

print("\nPORTFOLIO ALLOCATION")
print(get_portfolio_allocation(portfolio))

print("\nAPPLE VS NVIDIA")
print(compare_stocks(portfolio, "AAPL", "NVDA"))
