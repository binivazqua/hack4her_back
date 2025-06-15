import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# create api_key variable
api_key = os.getenv("GEMINI_API_KEY")
# Initialize the Gemini API client

genai.configure(api_key=api_key)

# crear variable para el modelo
model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=genai.GenerationConfig(
    temperature=0.5,
    max_output_tokens=256,
    top_p=0.95,
    top_k=40
))

"""
    - top_p (float): Controla la "nucleus sampling" o muestreo de núcleo. 
    Este parámetro especifica el umbral de probabilidad acumulada para considerar 
    las siguientes palabras candidatas en la generación de texto. Por ejemplo,
    si top_p=0.95, el modelo seleccionará palabras de entre el conjunto más pequeño posible
    cuyo total de probabilidades sume al menos el 95%. Esto ayuda a mantener la diversidad 
    en las respuestas, evitando que el modelo elija siempre las palabras más probables.

    - top_k (int): Limita el número de palabras candidatas consideradas en cada paso de generación. 
    Si top_k=40, el modelo solo considerará las 40 palabras más probables para seleccionar la
    siguiente palabra en la secuencia. Un valor más bajo hace que las respuestas sean más predecibles, 
    mientras que un valor más alto permite mayor diversidad.

"""


def ask_gemini(prompt:str) -> str:
    """
    Funcion base para interactuar con gemini """
    response = model.generate_content(prompt)
    print("🧠 Prompt generado:\n", prompt)
    return response.text.strip() if response.text else "Gemini no pudo generar una respuesta."