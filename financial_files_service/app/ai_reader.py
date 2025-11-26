# app/ai_reader.py
import json
from google import genai
from google.genai import types
from .schemas import ReporteFinanciero


def analyze_financial_text(text_content: str) -> ReporteFinanciero:
    # 1. Obtener el cliente de la API
    try:
        # Esto asume que genai.configure() ya se ejecutó en app/core/gemini.py
        client = genai.Client()
    except Exception as e:
        # Si la configuración falló, es mejor levantar una excepción clara
        raise RuntimeError("El cliente de Gemini no pudo ser inicializado. Revise su API_KEY.")

    # 2. Definición del Modelo y Configuración

    # Configuramos el modelo para que devuelva JSON y usamos la instrucción del sistema
    config = types.GenerateContentConfig(
        # Usar response_mime_type="application/json" fuerza la salida JSON (si el modelo lo soporta)
        response_mime_type="application/json",

        system_instruction="Eres un experto analista financiero y API de backend. Tu tarea es analizar el texto extraído de un extracto bancario y convertirlo en un JSON estructurado."
    )

    # Definimos el esquema de la respuesta JSON para que el modelo lo use
    # La nueva API permite pasar el schema directamente. Aquí simplificamos con la descripción en el prompt.

    prompt = f"""
    Instrucciones:
    1. Identifica cada transacción.
    2. Clasifica si es "ingreso" o "gasto".
    3. Asigna una categoría lógica (Ej: Comida, Transporte, Servicios, Nómina).
    4. El formato de fecha debe ser YYYY-MM-DD.
    5. Calcula los totales de ingresos y gastos.
    6. A partir de la clasificación decir la categoría en la que más se gasta 
    7. Dar un consejo financiero para el mes
    6. Tu respuesta debe ser *estrictamente* un objeto JSON válido, siguiendo este esquema:

    {{
        "resumen": "Un breve texto resumiendo la salud financiera del extracto",
        "transacciones": [
            {{
                "fecha": "2023-10-25",
                "descripcion": "Compra Supermercado",
                "monto": 150.50,
                "tipo": "gasto",
                "categoria": "Alimentación"
            }}
        ],
        "total_ingresos": 0.0,
        "total_gastos": 0.0
    }}

    TEXTO DEL DOCUMENTO:
    {text_content}
    """

    try:
        # 3. Llamada a la API
        # Usamos client.models.generate_content y pasamos los argumentos como clave=valor
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],  # Contents debe ser una lista de partes
            config=config
        )

        # 4. Procesamiento de la Respuesta

        # Con JSON Mode, la respuesta.text ya debe ser JSON puro.
        clean_response = response.text.strip()

        data = json.loads(clean_response)

        # Validamos con Pydantic
        return ReporteFinanciero(**data)

    except json.JSONDecodeError as e:
        print(f"Error decodificando el JSON de Gemini. Respuesta AI: {response.text[:200]}...")
        raise ValueError(f"La IA no devolvió un JSON válido. Error: {e}")

    except Exception as e:
        print(f"Error inesperado procesando con AI: {e}")
        raise e