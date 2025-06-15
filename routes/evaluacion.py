from fastapi import APIRouter, HTTPException
import datetime
from models.schemas import EvaluacionCompleta, RespuestaEntrevista
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_EVALUACION
import json
from firebase_config import db
from fastapi import Query


router = APIRouter()

print("🔄 Módulo de evaluación cargado correctamente.")

# Endpoint para guardar la evaluación generada en Firestore
@router.post("/guardar-evaluacion")
async def guardar_evaluacion(evaluacion: EvaluacionCompleta, punto_id: str = Query(..., description="ID del punto de venta"),
    visita_id: str = Query(..., description="ID de la visita")):
    """
    Guarda la evaluación generada dentro de una visita existente en Firestore,
    bajo la ruta /puntosDeVenta/{punto_id}/visitas/{visita_id}.
    """
    try:
        evaluacion_dict = {
            
            "respuestas": [r.dict() for r in evaluacion.respuestas],
            "colaborador": evaluacion.colaborador
        }

        ref = db.collection("puntosDeVenta").document(punto_id).collection("visitas").document(visita_id)

        if ref.get().exists:
            ref.update({"evaluacionGenerada": evaluacion_dict})
        else:
            ref.set({"evaluacionGenerada": evaluacion_dict})

        return {"mensaje": "✅ Evaluación guardada correctamente en la visita."}

    except Exception as e:
        print(f"❌ Error al guardar evaluación en visita: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar la evaluación en la visita.")






@router.post("/evaluacion-completa")
async def generar_evaluacion_completa(data: EvaluacionCompleta):
    """
    Genera una evaluación completa del cliente basada en su perfil y respuestas.
    """
    prompt = PROMPT_PLANTILLA_EVALUACION.format(
        perfil=data.cliente.tipo_negocio,
        respuestas=", ".join(
            f"{respuesta.id_pregunta}: {respuesta.respuesta}" for respuesta in data.respuestas
        )
    )
    
    try:
        respuesta = ask_gemini(prompt)
        if not respuesta.strip().endswith(".") or respuesta.strip().endswith(":") or respuesta.strip().endswith("*"):
            print("⚠️ Evaluación truncada detectada, añadiendo cierre automático...")
            respuesta += "\n\n**Cierre del reporte:** Esta auditoría ha concluido. Se recomienda implementar las acciones sugeridas para mejorar el punto de venta."

        return {"evaluacion": respuesta}
    except Exception as e:
        print(f"❌ Error al obtener respuesta de Gemini: {e}")
        print(f"Prompt enviado: {prompt}")
        raise HTTPException(status_code=500, detail="Error al generar la evaluación con Gemini.")

