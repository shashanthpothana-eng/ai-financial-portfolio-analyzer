
import json

from utils.llm_provider import LLMProvider


def generate_portfolio_analysis(
    portfolio,
    risk_metrics,
    total_investment,
    total_value,
    total_profit,
    total_return,
    provider="ollama"
):

    portfolio_data = portfolio[
        [
            "Ticker",
            "Shares",
            "Current Price",
            "Current Value",
            "Profit/Loss",
            "Return (%)"
        ]
    ].to_dict(orient="records")

    financial_context = {
        "holdings": portfolio_data,
        "total_investment": round(total_investment, 2),
        "current_value": round(total_value, 2),
        "profit_loss": round(total_profit, 2),
        "total_return_percent": round(total_return, 2),
        "risk_metrics": risk_metrics
    }

    prompt = f"""
You are a professional financial analytics assistant.

Analyze the following portfolio data:

{json.dumps(financial_context, indent=2)}

Provide your analysis using these sections:

1. Portfolio Overview
2. Individual Stock Performance
3. Risk Analysis
4. Portfolio Diversification
5. Key Observations

IMPORTANT RULES:

- Use only the supplied financial data.
- Never invent financial statistics.
- Distinguish total investment return from historical return.
- Explain annualized volatility and maximum drawdown.
- Do not classify risk as low, moderate, or high
  without an explicit benchmark.
- Identify sector concentration where supported.
- Avoid contradictory statements.
- Do not predict future stock performance.
- Do not provide personalized buy or sell advice.
- Mention missing information explicitly.

Use clear, concise language.
"""

    ai = LLMProvider(provider=provider)

    return ai.generate_response(prompt)
