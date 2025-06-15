from fastapi import APIRouter
from models.schemas import PerfilCliente
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_ENTREVISTA
import json
from fastapi import HTTPException
from models.schemas import Pregunta


router = APIRouter()

def limpiar_respuesta_json(texto: str) -> str:
    """
    Elimina bordes tipo ```json o ``` de las respuestas de Gemini.
    """
    if texto.startswith("```json"):
        texto = texto.replace("```json", "")
    if texto.endswith("```"):
        texto = texto.replace("```", "")
    return texto.strip()

@router.post("/generar-guia-entrevista")
async def generar_guia_entrevista(perfil_cliente: PerfilCliente):
    """
    Genera una guía de entrevista para un cliente basado en su perfil.
    """
    prompt = PROMPT_PLANTILLA_ENTREVISTA.format(
        zona=perfil_cliente.zona,
        tipo_negocio=perfil_cliente.tipo_negocio,
        antiguedad_cliente=perfil_cliente.antiguedad_cliente,
        nombre_dueno=perfil_cliente.nombre_dueno
    )

    respuesta_cruda = ask_gemini(prompt)
    print("🔍 Respuesta de Gemini:\n", respuesta_cruda)

    respuesta_limpia = limpiar_respuesta_json(respuesta_cruda)

    try:
        datos_json = json.loads(respuesta_limpia)
    except json.JSONDecodeError as e:
        print("⚠️ JSON inválido o incompleto:", e)
        raise HTTPException(status_code=400, detail=f"❌ Gemini devolvió JSON inválido o truncado: {str(e)}")

    entrevista = []
    for item in datos_json:
        if not isinstance(item, dict) or "rubro" not in item or "pregunta" not in item:
            print(f"⚠️ Pregunta malformada: {item}")
            continue
        try:
            entrevista.append(Pregunta(**item))
        except Exception as e:
            print(f"❌ Error convirtiendo item a Pregunta: {e}")
            continue

    if not entrevista:
        raise HTTPException(status_code=500, detail="Gemini no devolvió ninguna pregunta válida.")

    return {"entrevista": entrevista}
    