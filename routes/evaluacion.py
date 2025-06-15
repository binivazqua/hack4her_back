from fastapi import APIRouter, HTTPException
import datetime
from models.schemas import EvaluacionCompleta, RespuestaEntrevista
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_EVALUACION
import json
from firebase_config import db


router = APIRouter()

print("🔄 Módulo de evaluación cargado correctamente.")

# Endpoint para guardar la evaluación generada en Firestore
@router.post("/guardar-evaluacion")
async def guardar_evaluacion(evaluacion: EvaluacionCompleta):
    """
    Guarda la evaluación generada en Firestore.
    """
    try:
        fecha = datetime.datetime.now().isoformat()
        doc_data = {
            "cliente": evaluacion.cliente.dict(),
            "respuestas": [r.dict() for r in evaluacion.respuestas],
            "colaborador": evaluacion.colaborador,
            "fecha": fecha
        }

        cliente_id = f"{evaluacion.cliente.nombre_dueno.lower().replace(' ', '_')}_{evaluacion.cliente.zona.lower().replace(' ', '_')}"
        db.collection("evaluaciones").document(cliente_id).collection("entrevistas").document(fecha).set(doc_data)

        return {"mensaje": "✅ Evaluación guardada con éxito."}

    except Exception as e:
        print(f"❌ Error al guardar en Firestore: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar la evaluación.")



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
        return {"evaluacion": respuesta}
    except Exception as e:
        print(f"❌ Error al obtener respuesta de Gemini: {e}")
        print(f"Prompt enviado: {prompt}")
        raise HTTPException(status_code=500, detail="Error al generar la evaluación con Gemini.")

