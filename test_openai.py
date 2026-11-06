
from utils.llm_provider import LLMProvider

try:
    ai = LLMProvider(provider="openai")

    response = ai.generate_response(
        "Explain portfolio diversification in two sentences."
    )

    print("\nOpenAI connection successful!")
    print("\nModel:", ai.model)
    print("\nResponse:")
    print(response)

except Exception as error:
    print("\nOpenAI test failed:")
    print(type(error).__name__, str(error))
