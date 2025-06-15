# confirmacion.py
from fastapi import APIRouter, HTTPException, Query
from firebase_config import db

router = APIRouter()

@router.post("/finalizar-visita")
async def finalizar_visita(
    punto_id: str = Query(..., description="ID del punto de venta"),
    visita_id: str = Query(..., description="ID de la visita")
):
    """
    Marca una visita como finalizada si ya contiene la información clave.
    """
    try:
        ref = db.collection("puntosDeVenta").document(punto_id).collection("visitas").document(visita_id)
        doc = ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="❌ La visita no existe.")

        data = doc.to_dict()

        if "evaluacionGenerada" not in data:
            raise HTTPException(status_code=400, detail="❌ Falta la evaluación generada en esta visita.")

        if "comentarioCualitativo" not in data:
            print("⚠️ Advertencia: La visita no tiene comentario cualitativo. Se marca como finalizada de todas formas.")

        ref.update({"visitaFinalizada": True})
        return {"mensaje": "✅ Visita marcada como finalizada exitosamente."}

    except Exception as e:
        print(f"❌ Error al finalizar visita: {e}")
        raise HTTPException(status_code=500, detail="Error al finalizar la visita.")
