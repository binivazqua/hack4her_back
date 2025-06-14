from fastapi import APIRouter
from models.schemas import EvaluacionCompleta
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_EVALUACION


router = APIRouter()
@router.post("/evaluacion-completa")
async def generar_evaluacion_completa(data: EvaluacionCompleta):
    """
    Genera una evaluación completa del cliente basada en su perfil y respuestas.
    """
    prompt = PROMPT_PLANTILLA_EVALUACION.format(
        perfil=data.perfil_cliente.perfil,
        respuestas=data.respuestas
    )
    
    respuesta = await ask_gemini(prompt)
    
    return {"evaluacion": respuesta}

