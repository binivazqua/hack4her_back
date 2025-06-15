from fastapi import APIRouter
from models.schemas import PerfilCliente
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_GUIA_ACTITUD


router = APIRouter()

@router.post("/generar-guia-actitud")
async def generar_guia_actitud(perfil_cliente: PerfilCliente):
    """
    Genera una guía de actitud para un cliente basado en su perfil.
    """
    prompt = PROMPT_GUIA_ACTITUD.format(
        zona=perfil_cliente.zona,
        antiguedad=perfil_cliente.antiguedad_cliente,
        edad=perfil_cliente.edad,
        nombre=perfil_cliente.nombre_dueno,
        sexo=perfil_cliente.sexo
    )
    try:
        respuesta = ask_gemini(prompt)
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": str(e)}
