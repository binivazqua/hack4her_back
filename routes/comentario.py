from fastapi import APIRouter
from models.schemas import EvaluacionCompleta
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_COMENTARIO


router = APIRouter()

@router.post("/generar-comentario")
async def generar_comentario(comentario: EvaluacionCompleta):
    """
    Genera un comentario basado en la evaluación de un cliente.
    """
    prompt = PROMPT_PLANTILLA_COMENTARIO.format(
        perfil=comentario.perfil_cliente,
        evaluacion=comentario.evaluacion,
        recomendaciones=comentario.recomendaciones
    )
    
    respuesta = ask_gemini(prompt)
    
    return {"respuesta": respuesta}

