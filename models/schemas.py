from pydantic import BaseModel
from typing import Optional

# ---------------------------
# NUEVAS CLASES BASE
# ---------------------------

class Negocio(BaseModel):
    tipo: str
    zona: str
    antiguedad_cliente: str


class Dueno(BaseModel):
    nombre: str
    edad: Optional[int] = None
    sexo: Optional[str] = None
    caracteristica_particular: Optional[str] = None
    contacto: Optional[str] = None


class PuntoDeVenta(BaseModel):
    negocio: Negocio
    dueno: Dueno

# ---------------------------
# COMPATIBILIDAD CON ENDPOINTS ACTUALES
# ---------------------------

class PerfilCliente(BaseModel):
    tipo_negocio: str
    zona: str
    antiguedad_cliente: str
    nombre_dueno: str

    @classmethod
    def from_pdv(cls, pdv: PuntoDeVenta):
        return cls(
            tipo_negocio=pdv.negocio.tipo,
            zona=pdv.negocio.zona,
            antiguedad_cliente=pdv.negocio.antiguedad_cliente,
            nombre_dueno=pdv.dueno.nombre
        )

# ---------------------------
# NUEVO PERFIL PARA GUÍA DE ACTITUD
# ---------------------------

class PerfilActitud(BaseModel):
    edad: int
    sexo: str
    zona: str
    nombre: str
    caracteristica_particular: Optional[str] = None

    @classmethod
    def from_pdv(cls, pdv: PuntoDeVenta):
        return cls(
            edad=pdv.dueno.edad,
            sexo=pdv.dueno.sexo,
            zona=pdv.negocio.zona,
            nombre=pdv.dueno.nombre,
            caracteristica_particular=pdv.dueno.caracteristica_particular
        )


# ---------------------------
# MODELOS PARA ENTREVISTA
# ---------------------------

class Pregunta(BaseModel):
    rubro: str
    pregunta: str


class GenerarEntrevistaRequest(BaseModel):
    cliente: PerfilCliente  # se mantiene como está


class GenerarEntrevistaResponse(BaseModel):
    entrevista: list[Pregunta]


# ---------------------------
# MODELOS PARA EVALUACIÓN COMPLETA
# ---------------------------

class RespuestaEntrevista(BaseModel):
    pregunta: str
    respuesta: str


class EvaluacionCompleta(BaseModel):
    cliente: PerfilCliente
    respuestas: list[RespuestaEntrevista]

