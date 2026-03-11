import os
from groq import Groq


# =====================================================
# MOCK LLM (Fallback if API fails)
# =====================================================

class MockLLM:

    def generate(self, prompt: str) -> str:
        return (
            "AI service unavailable. Using fallback interpretation.\n\n"
            "Based on the financial analysis, several spending anomalies "
            "and potential inefficiencies were detected that may require "
            "further investigation by finance or procurement teams."
        )


# =====================================================
# OPENAI LLM (Not used in this project)
# =====================================================

class OpenAILLM:

    def __init__(self):
        raise NotImplementedError(
            "OpenAI integration is not enabled in this project."
        )


# =====================================================
# GROQ LLM (Primary AI Engine)
# =====================================================

class GroqLLM:

    def __init__(self, model="llama-3.1-8b-instant"):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = model


    def generate(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial risk analysis expert explaining enterprise spend analytics."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:

            return (
                "AI service unavailable. Using fallback interpretation.\n\n"
                f"Error: {str(e)}\n\n"
                + MockLLM().generate(prompt)
            )


# =====================================================
# EXPORTS
# =====================================================

__all__ = ["MockLLM", "OpenAILLM", "GroqLLM"]