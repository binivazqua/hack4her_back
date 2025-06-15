from fastapi import APIRouter, HTTPException, Query
import json
from firebase_config import db
from services.gemini import ask_gemini
from utils.prompt_templates import PROMPT_PLANTILLA_COMENTARIO

router = APIRouter()

def limpiar_respuesta_json(texto: str) -> str:
    """
    Elimina etiquetas tipo ```json y otros delimitadores que Gemini puede incluir.
    """
    texto = texto.strip()
    if texto.startswith("```json"):
        texto = texto.replace("```json", "")
    if texto.startswith("```"):
        texto = texto.replace("```", "")
    if texto.endswith("```"):
        texto = texto[:-3]
    return texto.strip()

@router.post("/guardar-comentario")
async def guardar_comentario(
    comentario_colaborador: str = Query(..., description="Comentario informal del colaborador"),
    punto_id: str = Query(..., description="ID del punto de venta"),
    visita_id: str = Query(..., description="ID de la visita")
):
    """
    Procesa un comentario informal y guarda un resumen estructurado en Firestore.
    """

    try:
        prompt = PROMPT_PLANTILLA_COMENTARIO.format(
            comentario_colaborador=comentario_colaborador
        )

        respuesta_raw = ask_gemini(prompt)
        print("🔍 Respuesta cruda de Gemini:\n", respuesta_raw)

        respuesta_limpia = limpiar_respuesta_json(respuesta_raw)
        print("🧹 Respuesta limpia:\n", respuesta_limpia)

        try:
            comentario_json = json.loads(respuesta_limpia)
        except json.JSONDecodeError as e:
            print(f"❌ Error de JSON: {e}")
            raise HTTPException(status_code=400, detail="La respuesta de Gemini no es un JSON válido.")

        db.collection("puntosDeVenta")\
          .document(punto_id)\
          .collection("visitas")\
          .document(visita_id)\
          .set({"comentariosAdicionales": comentario_json}, merge=True)

        return {"mensaje": "✅ Comentario procesado y guardado correctamente."}

    except Exception as e:
        print(f"❌ Error al guardar comentario: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar el comentario.")


