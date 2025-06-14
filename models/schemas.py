from pydantic import BaseModel, Field
# Aquí definimos las clases para las estructuras de datos que vamos a utilizar en los endpoints

class PerfilCliente(BaseModel):
    """
    Modelo de datos para el perfil del cliente. @diana modificar jijiji 
    """
    zona: str
    tipo_cliente: str
    necesidades: str
    preferencias: str


