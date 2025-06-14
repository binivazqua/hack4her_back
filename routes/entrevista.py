from fastapi import APIRouter
from models.schemas import PerfilCliente
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_ENTREVISTA



router = APIRouter()

@router.post("/generar-guia-entrevista")
async def generar_guia_entrevista(perfil_cliente: PerfilCliente):
    """
    Genera una guía de entrevista para un cliente basado en su perfil.
    """
    prompt = PROMPT_PLANTILLA_ENTREVISTA.format(
        zona=perfil_cliente.zona,
        tipo_cliente=perfil_cliente.tipo_cliente,
        necesidades=perfil_cliente.necesidades,
        preferencias=perfil_cliente.preferencias
    )
    
    respuesta = await ask_gemini(prompt)
    
    return {"respuesta": respuesta}
    