
import json

from utils.financial_tools import (
    get_portfolio_summary,
    get_stock_performance,
    get_portfolio_allocation,
    get_risk_metrics,
    compare_stocks,
)

from utils.stock_research import research_stock

from utils.financial_tools import (
    get_portfolio_summary,
    get_stock_performance,
    get_portfolio_allocation,
    get_risk_metrics,
    compare_stocks,
    compare_external_stocks,
)

TOOLS = [
    {
        "type": "function",
        "name": "get_portfolio_summary",
        "description": "Get total investment, current value, profit and return.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_stock_performance",
        "description": "Get performance details for a stock in the portfolio.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker, such as AAPL or NVDA."
                }
            },
            "required": ["ticker"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_portfolio_allocation",
        "description": "Get portfolio allocation percentages for all holdings.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_risk_metrics",
        "description": "Get calculated portfolio risk metrics.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "compare_stocks",
        "description": "Compare performance of two portfolio holdings.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker1": {
                    "type": "string"
                },
                "ticker2": {
                    "type": "string"
                }
            },
            "required": ["ticker1", "ticker2"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "research_stock",
        "description": (
            "Research any publicly traded stock, "
            "including stocks not currently in the user's portfolio. "
            "Returns market price, historical returns, volatility, "
            "drawdown, revenue, profit margin and sector."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker, such as PLUG or TSLA."
                }
            },
            "required": ["ticker"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "compare_external_stocks",
        "description": (
            "Compare two stocks using external financial research, "
            "including stocks outside the user's portfolio."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticker1": {"type": "string"},
                "ticker2": {"type": "string"}
            },
            "required": ["ticker1", "ticker2"],
            "additionalProperties": False
        },
        "strict": True
    }
    
]


def execute_tool(
    tool_name,
    arguments,
    portfolio,
    risk_metrics
):
    """Execute an approved financial tool."""

    if tool_name == "get_portfolio_summary":
        return get_portfolio_summary(portfolio)

    elif tool_name == "get_stock_performance":

        ticker = arguments["ticker"].upper()
        portfolio_tickers = (
            portfolio["Ticker"].str.upper().tolist()
        )
        if ticker not in portfolio_tickers:
            return research_stock(ticker)

        return get_stock_performance(
            portfolio,
            ticker
        )

    elif tool_name == "get_portfolio_allocation":
        return get_portfolio_allocation(portfolio)

    elif tool_name == "get_risk_metrics":
        return get_risk_metrics(risk_metrics)

    elif tool_name == "compare_stocks":
        return compare_stocks(
            portfolio,
            arguments["ticker1"],
            arguments["ticker2"]
        )
    elif tool_name == "research_stock":

        return research_stock(
            arguments["ticker"]
    )
    elif tool_name == "compare_external_stocks":

        return compare_external_stocks(
            arguments["ticker1"],
            arguments["ticker2"]
    )

    raise ValueError(f"Unknown tool requested: {tool_name}")


def chat_with_financial_agent(
    question,
    portfolio,
    risk_metrics,
    conversation_history=None
):
    """Run an OpenAI financial agent with controlled tool calling."""

    from utils.llm_provider import LLMProvider

    ai = LLMProvider(provider="openai")

    if conversation_history is None:
        conversation_history = []

    instructions = """
    You are an educational AI financial portfolio assistant.

    Your job is to analyze portfolio performance, research external
    stocks, compare companies, and explain financial risks.

    AVAILABLE CAPABILITIES:

    1. Portfolio analysis
    2. Individual stock performance
    3. External stock research
    4. Portfolio risk analysis
    5. External stock comparison

    RULES:

    1. Use financial tools whenever a question requires actual
    portfolio or market data.

    2. Never invent financial values or company information.

    3. Use portfolio data only when analyzing the user's holdings.

    4. Use research_stock for researching individual stocks
    outside the user's portfolio.

    5. Use compare_stocks for comparing two stocks specifically
    within the user's portfolio.

    6. Use compare_external_stocks whenever the user asks to
    compare two stocks using external financial research.
    This works whether or not the stocks belong to the portfolio.

    7. Do not call get_stock_performance repeatedly to compare
    external stocks. Use compare_external_stocks instead.

    8. Never confuse external stock research with existing
    portfolio holdings.

    9. Clearly distinguish unrealized gains from realized gains.

    10. Explain financial calculations when relevant.

    11. When users ask whether they should buy a stock,
        provide balanced educational analysis, not personalized
        buy or sell instructions.

    12. Explain financial risks using retrieved data.

    13. Never invent missing financial information.

    14. If a financial tool returns an error, explain the issue
        rather than making up an answer.

    15. When comparing companies, consider:
        - One-year historical return
        - Annualized volatility
        - Maximum drawdown
        - Profit margin
        - Revenue
        - Market capitalization

    16. Explain which company has stronger metrics based on
        the available data, without treating any single metric
        as proof of a better investment.

    17. Never describe lower historical volatility as guaranteed
        lower future investment risk.

    18. Clearly identify missing data and differences in
        reporting periods when relevant.

    19. Never guarantee future stock performance.

    20. Include an educational financial disclaimer when
        providing investment-related analysis.

    Always provide clear, structured, and understandable answers.
    """

    # Preserve the previous conversation and add the new question.
    conversation_history.append({
        "role": "user",
        "content": question
    })

    response = ai.client.responses.create(
        model=ai.model,
        instructions=instructions,
        input=conversation_history,
        tools=TOOLS
    )

    # Process tool calls, if requested.
    for _ in range(5):

        function_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            answer = response.output_text

            conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        tool_outputs = []

        for call in function_calls:

            arguments = json.loads(call.arguments)
            print(f"\n[AI AGENT] Tool requested: {call.name}")
            print(f"[AI AGENT] Arguments: {arguments}")

            result = execute_tool(
                tool_name=call.name,
                arguments=arguments,
                portfolio=portfolio,
                risk_metrics=risk_metrics
            )
            print(f"[AI AGENT] Tool result: {result}")


            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result)
            })

        response = ai.client.responses.create(
            model=ai.model,
            instructions=instructions,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=TOOLS
        )

    raise RuntimeError(
        "Maximum tool-calling iterations reached."
    )
