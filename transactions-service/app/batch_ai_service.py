import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CATEGORIES = [
    "GROCERIES", "RENT", "UTILITIES", "TRANSPORTATION",
    "ENTERTAINMENT", "HEALTH", "INCOME", "TRANSFER",
    "EDUCATION", "BUSINESS", "OTHER"
]


def batch_categorize(transactions: list):
    """
    transactions = [
        {"description": "...", "amount": ...},
        {...}
    ]
    """
    prompt = f"""
    You are a financial transaction classifier.
    Classify each transaction with one of the following categories:

    {", ".join(CATEGORIES)}

    Respond ONLY in this JSON list format:
    [
      {{"category": "GROCERIES"}},
      {{"category": "RENT"}}
    ]

    Transactions:
    {transactions}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        categories = eval(response.text)   # puede usarse json.loads si el modelo responde limpio
        return [c["category"] for c in categories]
    except:
        # fallback si el modelo no responde perfecto
        return ["OTHER"] * len(transactions)