from pydantic import BaseModel, Field
# Aquí definimos las clases para las estructuras de datos que vamos a utilizar en los endpoints

class PerfilCliente(BaseModel):
    """
    Modelo de datos para el perfil del cliente. @diana modificar jijiji 
    """
    caracteristicaParticular: str
    edad: str
    zona: str
    nombre: str
    sexo: str

class EvaluacionCompleta(BaseModel):
    """
    Modelo de datos para la evaluación completa del cliente.
    Incluye el perfil del cliente y las respuestas a las preguntas de la evaluación.
    """
    perfil_cliente: PerfilCliente
    respuestas: dict 

class Feedback(BaseModel):
    """
    Modelo de datos para un comentario del cliente.
    """
    text: str = Field(..., description="Texto del comentario del cliente")
