
import os
import ollama

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMProvider:

    def __init__(self, provider="ollama"):

        self.provider = provider

        

        if provider == "ollama":
            self.model = "llama3.2:3b"

        elif provider == "openai":

            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY is missing. Check your .env file."
                )

            self.model = os.getenv(
                "OPENAI_MODEL",
                "gpt-5-mini"
            )

            self.client = OpenAI(api_key=api_key)

        else:
            raise ValueError(
                f"Unsupported provider: {provider}"
            )

    def generate_response(self, prompt):

        system_instruction = """
        You are an educational financial analytics assistant.

        Rules:
        - Use only the financial data provided.
        - Never invent financial statistics.
        - Explain financial concepts clearly.
        - Identify concentration risks when supported by data.
        - Do not provide personalized buy or sell recommendations.
        """

        if self.provider == "ollama":

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response["message"]["content"]

        elif self.provider == "openai":

            response = self.client.responses.create(
                model=self.model,
                instructions=system_instruction,
                input=prompt
            )
            print("OPENAI API CALLED")
            print("Model:", response.model)
            print("Response ID:", response.id)

            return response.output_text
