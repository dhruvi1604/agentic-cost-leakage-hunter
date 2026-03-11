from src.llm.backends import GeminiLLM

llm = GeminiLLM()

print(
    llm.generate(
        "Explain in simple words why duplicate invoices are a problem for small businesses."
    )
)
