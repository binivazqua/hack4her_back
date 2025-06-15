from fastapi import APIRouter
from models.schemas import EvaluacionCompleta, ComentarioInput
from firebase_config import db
from fastapi import HTTPException, Query
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_COMENTARIO


router = APIRouter()

@router.post("/guardar-comentario")
async def guardar_comentario(
    data: ComentarioInput,
    punto_id: str = Query(..., description="ID del punto de venta"),
    visita_id: str = Query(..., description="ID de la visita")
):
    """
    Guarda el comentario cualitativo generado a partir del feedback del colaborador.
    """
    try:
        ref = db.collection("puntosDeVenta").document(punto_id).collection("visitas").document(visita_id)

        if not ref.get().exists:
            raise HTTPException(status_code=404, detail="❌ La visita no existe.")

        ref.update({
            "comentarioCualitativo": {
                "texto": data.comentario,
                "clasificacion": data.clasificacion
            }
        })

        return {"mensaje": "✅ Comentario cualitativo guardado correctamente."}

    except Exception as e:
        print(f"❌ Error al guardar comentario: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar el comentario cualitativo.")

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

