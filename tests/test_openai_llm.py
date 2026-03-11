from src.llm.backends import OpenAILLM

llm = OpenAILLM()

response = llm.generate(
    "Explain in one sentence why duplicate invoices are risky for SMBs."
)

print("LLM RESPONSE:")
print(response)
