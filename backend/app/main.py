from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.errors import registrar_manejadores
from app.core.seed import cargar_admin, cargar_roles
from app.routers import (
    adopciones,
    animales,
    auth,
    health,
    hogares_transito,
    publicaciones,
    registros_sanitarios,
    rescates,
    solicitudes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    cargar_roles()
    cargar_admin()
    yield


app = FastAPI(
    title=settings.app_name,
    description="API REST de RescuePet: gestión de rescate, tránsito y adopción responsable de animales.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

registrar_manejadores(app)

app.include_router(health.router)
app.include_router(animales.router)
app.include_router(rescates.router)
app.include_router(registros_sanitarios.router)
app.include_router(hogares_transito.router)
app.include_router(auth.router)
app.include_router(publicaciones.router)
app.include_router(solicitudes.router)
app.include_router(adopciones.router)