# app/core/gemini.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def get_gemini_client():
    """Retorna la instancia del cliente de Gemini configurada."""
    return client
