from fastapi import APIRouter
from models.schemas import PerfilCliente
from services.gemini import askgemini
from utils.prompt_templates import PROMPT_GUIA_ACTITUD


router = APIRouter()

@router.post("/generar-guia-actitud")
async def generar_guia_actitud(perfil_cliente: PerfilCliente):
    """
    Genera una guía de actitud para un cliente basado en su perfil.
    """
    prompt = PROMPT_GUIA_ACTITUD.format(
        zona=perfil_cliente.zona,
        # Cambiar según el modelo de PerfilCliente
        tipo_cliente=perfil_cliente.tipo_cliente,
        necesidades=perfil_cliente.necesidades,
        preferencias=perfil_cliente.preferencias
    )
    
    respuesta = await askgemini(prompt)
    
    return {"respuesta": respuesta}