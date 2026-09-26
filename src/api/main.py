from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import build_crud_router
from src.database import init_db
from src.models import (
    AsistenciaModel,
    ClaseModel,
    ClienteModel,
    EntrenadorModel,
    EquipoModel,
    MembresiaModel,
    PagoModel,
    RutinaModel,
    SedeModel,
    UsuarioModel,
)

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="API REST - Proyecto Gym",
    description="API para administrar las entidades del gimnasio.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESOURCES = (
    ("usuarios", UsuarioModel, "id_usuario"),
    ("membresias", MembresiaModel, "id_membresia"),
    ("sedes", SedeModel, "id_sede"),
    ("clientes", ClienteModel, "id_cliente"),
    ("entrenadores", EntrenadorModel, "id_entrenador"),
    ("clases", ClaseModel, "id_clase"),
    ("rutinas", RutinaModel, "id_rutina"),
    ("equipos", EquipoModel, "id_equipo"),
    ("asistencias", AsistenciaModel, "id_asistencia"),
    ("pagos", PagoModel, "id_pago"),
)

for resource, model, id_field in RESOURCES:
    app.include_router(
        build_crud_router(model, resource, id_field),
        prefix=API_PREFIX,
    )


@app.get("/", status_code=status.HTTP_200_OK, tags=["Inicio"])
def root():
    return {"mensaje": "API REST del Proyecto Gym", "documentacion": "/docs"}
