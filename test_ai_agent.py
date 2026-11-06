
import pandas as pd

from utils.ai_agent import chat_with_financial_agent

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

risk_metrics = {
    "Annualized Volatility": 21.83,
    "Maximum Drawdown": -19.95,
    "Historical Return": 16.18
}

#question = "Which stock has the highest return?"
#question = "Compare TSLA and GOOGL in my portfolio."
#question = "Analyze PLUG. What are its major financial risks?"
#question = "Analyze TSLA and explain its financial risks."
question = "Compare TSLA and GOOGL."



answer = chat_with_financial_agent(
    question=question,
    portfolio=portfolio,
    risk_metrics=risk_metrics
)

print("\nAI FINANCIAL AGENT RESPONSE")
print(answer)
