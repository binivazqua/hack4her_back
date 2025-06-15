from fastapi import APIRouter, HTTPException
from models.schemas import EvaluacionCompleta
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_RECOMENDACIONES

router = APIRouter()

@router.post("/recomendaciones-inmediatas")
def generar_recomendaciones(data: dict):
    """
    Genera recomendaciones inmediatas a partir del contenido de la evaluación completa.
    """
    try:
        prompt = PROMPT_PLANTILLA_RECOMENDACIONES.format(
            evaluacion=data["evaluacion"]
        )
        respuesta = ask_gemini(prompt)
        return {"recomendaciones": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error al generar recomendaciones: {str(e)}")

