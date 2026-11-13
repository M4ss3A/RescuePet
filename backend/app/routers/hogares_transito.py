from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import GestorAnimales, ResponsableHogar, UsuarioActual, require_role
from app.core.uow import UnitOfWork
from app.models.enums import RolNombre
from app.schemas.hogar_transito import (
    AsignacionCreate,
    AsignacionEgreso,
    AsignacionRead,
    HogarTransitoCreate,
    HogarTransitoRead,
    HogarTransitoUpdate,
)
from app.schemas.usuario import UsuarioPublic
from app.services.hogar_transito_service import HogarTransitoService

router = APIRouter(prefix="/api/v1", tags=["Hogares de tránsito"])


UsuarioHogares = Annotated[
    UsuarioPublic,
    Depends(require_role([RolNombre.RESCATISTA, RolNombre.HOGAR_TRANSITO, RolNombre.ADMINISTRADOR])),
]


def get_hogar_transito_service() -> HogarTransitoService:
    return HogarTransitoService(UnitOfWork())


Servicio = Annotated[HogarTransitoService, Depends(get_hogar_transito_service)]


@router.get("/hogares-transito", response_model=list[HogarTransitoRead])
def listar_hogares(_usuario: UsuarioHogares, service: Servicio, disponible: bool | None = None):
    """Lista los hogares. Con ?disponible=true devuelve solo los disponibles."""
    return service.listar(disponible)


@router.get("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def obtener_hogar(hogar_id: int, _usuario: UsuarioHogares, service: Servicio):
    return service.obtener(hogar_id)


@router.post("/hogares-transito", response_model=HogarTransitoRead, status_code=status.HTTP_201_CREATED)
def crear_hogar(datos: HogarTransitoCreate, responsable: ResponsableHogar, service: Servicio):
    """El responsable del hogar es el usuario logueado (rol HOGAR_TRANSITO)."""
    return service.crear(datos, responsable)


@router.patch("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def actualizar_hogar(hogar_id: int, datos: HogarTransitoUpdate, usuario: UsuarioActual, service: Servicio):
    """Solo el responsable del hogar o un administrador."""
    return service.actualizar(hogar_id, datos, usuario)


@router.get("/hogares-transito/{hogar_id}/asignaciones", response_model=list[AsignacionRead])
def listar_asignaciones(hogar_id: int, usuario: UsuarioActual, service: Servicio, activas: bool = False):
    """Rescatistas, administradores y el responsable del hogar. Con ?activas=true, solo las actuales."""
    return service.listar_asignaciones(hogar_id, usuario, activas)


@router.post(
    "/hogares-transito/{hogar_id}/asignaciones",
    response_model=AsignacionRead,
    status_code=status.HTTP_201_CREATED,
)
def asignar_animal(hogar_id: int, datos: AsignacionCreate, _usuario: GestorAnimales, service: Servicio):
    """Un rescatista o administrador ubica a un animal en el hogar."""
    return service.asignar_animal(hogar_id, datos)


@router.patch("/asignaciones-transito/{asignacion_id}/egreso", response_model=AsignacionRead)
def registrar_egreso(asignacion_id: int, datos: AsignacionEgreso, usuario: UsuarioActual, service: Servicio):
    """Rescatistas, administradores y el responsable del hogar."""
    return service.registrar_egreso(asignacion_id, datos, usuario)