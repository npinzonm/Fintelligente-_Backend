import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def categorize_transaction(description: str, amount: float):
    prompt = f"""
    You are a financial transaction classifier for a personal finance app.
    Classify the following transaction into a single category:

    Description: "{description}"
    Amount: {amount}

    Possible Categories:
    - GROCERIES
    - RENT
    - UTILITIES
    - TRANSPORTATION
    - ENTERTAINMENT
    - HEALTH
    - INCOME
    - TRANSFER
    - EDUCATION
    - BUSINESS
    - OTHER

    Respond only with the category name.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    category = response.text.strip().upper()

    # Validación
    valid = {
        "GROCERIES",
        "RENT",
        "UTILITIES",
        "TRANSPORTATION",
        "ENTERTAINMENT",
        "HEALTH",
        "INCOME",
        "TRANSFER",
        "EDUCATION",
        "BUSINESS",
        "OTHER"
    }

    if category not in valid:
        return "OTHER"

    return category