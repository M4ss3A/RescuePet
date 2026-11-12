from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork
from app.schemas.hogar_transito import (
    AsignacionCreate,
    AsignacionEgreso,
    AsignacionRead,
    HogarTransitoCreate,
    HogarTransitoRead,
    HogarTransitoUpdate,
)
from app.services.hogar_transito_service import HogarTransitoService

router = APIRouter(prefix="/api/v1", tags=["Hogares de tránsito"])


def get_hogar_transito_service() -> HogarTransitoService:
    return HogarTransitoService(UnitOfWork())


@router.get("/hogares-transito", response_model=list[HogarTransitoRead])
def listar_hogares(disponible: bool | None = None, service: HogarTransitoService = Depends(get_hogar_transito_service)):
    """Lista los hogares. Con ?disponible=true devuelve solo los disponibles."""
    return service.listar(disponible)


@router.get("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def obtener_hogar(hogar_id: int, service: HogarTransitoService = Depends(get_hogar_transito_service)):
    return service.obtener(hogar_id)


@router.post("/hogares-transito", response_model=HogarTransitoRead, status_code=status.HTTP_201_CREATED)
def crear_hogar(datos: HogarTransitoCreate, service: HogarTransitoService = Depends(get_hogar_transito_service)):
    return service.crear(datos)


@router.patch("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def actualizar_hogar(
    hogar_id: int,
    datos: HogarTransitoUpdate,
    service: HogarTransitoService = Depends(get_hogar_transito_service),
):
    return service.actualizar(hogar_id, datos)


@router.get("/hogares-transito/{hogar_id}/asignaciones", response_model=list[AsignacionRead])
def listar_asignaciones(
    hogar_id: int,
    activas: bool = False,
    service: HogarTransitoService = Depends(get_hogar_transito_service),
):
    """Animales que pasaron por el hogar. Con ?activas=true, solo los que están actualmente."""
    return service.listar_asignaciones(hogar_id, activas)


@router.post(
    "/hogares-transito/{hogar_id}/asignaciones",
    response_model=AsignacionRead,
    status_code=status.HTTP_201_CREATED,
)
def asignar_animal(
    hogar_id: int,
    datos: AsignacionCreate,
    service: HogarTransitoService = Depends(get_hogar_transito_service),
):
    return service.asignar_animal(hogar_id, datos)


@router.patch("/asignaciones-transito/{asignacion_id}/egreso", response_model=AsignacionRead)
def registrar_egreso(
    asignacion_id: int,
    datos: AsignacionEgreso,
    service: HogarTransitoService = Depends(get_hogar_transito_service),
):
    return service.registrar_egreso(asignacion_id, datos)
