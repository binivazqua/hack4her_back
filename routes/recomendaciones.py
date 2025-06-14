from fastapi import APIRouter
from models.schemas import EvaluacionCompleta
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_RECOMENDACIONES

router = APIRouter()

@router.post("/recomendaciones-inmediatas")
def generar_recomendaciones(data: EvaluacionCompleta):
    prompt = PROMPT_PLANTILLA_RECOMENDACIONES.format(
        perfil=data.perfil_cliente.caracteristicaParticular,
        contexto=data.respuestas
    )
    respuesta = ask_gemini(prompt)
    return {"recomendaciones": respuesta}
