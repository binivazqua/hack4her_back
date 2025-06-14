
from fastapi import FastAPI
from routes import recomendaciones, evaluacion, actitud, comentario, entrevista
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RulfoBytes Super App API",
    description="API para la Super App de RulfoBytes, que incluye funcionalidades de recomendaciones, evaluaciones, actitudes, comentarios y entrevistas.",
    version="1.0.0",

)

# Habilitar CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las origines
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir las rutas con sus prefijos
app.include_router(recomendaciones.router, tags=["Recomendaciones"])
app.include_router(evaluacion.router, tags=["Evaluaciones"])
app.include_router(actitud.router, tags=["Actitudes"])
app.include_router(comentario.router, tags=["Comentarios"])
app.include_router(entrevista.router, tags=["Entrevistas"])


@app.get("/")
def get_root():
    return {"message": "La API mas OP para la Super App de RulfoBytes esta en funcionamiento."}

