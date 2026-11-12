from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.hogar_transito import (
    AsignacionCreate,
    AsignacionEgreso,
    AsignacionRead,
    HogarTransitoCreate,
    HogarTransitoRead,
    HogarTransitoUpdate,
)
from app.services import hogar_transito_service

router = APIRouter(prefix="/api", tags=["Hogares de tránsito"])


@router.get("/hogares-transito", response_model=list[HogarTransitoRead])
def listar_hogares(disponible: bool | None = None, session: Session = Depends(get_session)):
    """Lista los hogares. Con ?disponible=true devuelve solo los disponibles."""
    return hogar_transito_service.listar_hogares(session, disponible)


@router.get("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def obtener_hogar(hogar_id: int, session: Session = Depends(get_session)):
    return hogar_transito_service.obtener_hogar(session, hogar_id)


@router.post("/hogares-transito", response_model=HogarTransitoRead, status_code=status.HTTP_201_CREATED)
def crear_hogar(datos: HogarTransitoCreate, session: Session = Depends(get_session)):
    return hogar_transito_service.crear_hogar(session, datos)


@router.patch("/hogares-transito/{hogar_id}", response_model=HogarTransitoRead)
def actualizar_hogar(hogar_id: int, datos: HogarTransitoUpdate, session: Session = Depends(get_session)):
    return hogar_transito_service.actualizar_hogar(session, hogar_id, datos)


@router.get("/hogares-transito/{hogar_id}/asignaciones", response_model=list[AsignacionRead])
def listar_asignaciones(hogar_id: int, activas: bool = False, session: Session = Depends(get_session)):
    """Animales que pasaron por el hogar. Con ?activas=true, solo los que están actualmente."""
    return hogar_transito_service.listar_asignaciones(session, hogar_id, activas)


@router.post(
    "/hogares-transito/{hogar_id}/asignaciones",
    response_model=AsignacionRead,
    status_code=status.HTTP_201_CREATED,
)
def asignar_animal(hogar_id: int, datos: AsignacionCreate, session: Session = Depends(get_session)):
    return hogar_transito_service.asignar_animal(session, hogar_id, datos)


@router.patch("/asignaciones-transito/{asignacion_id}/egreso", response_model=AsignacionRead)
def registrar_egreso(asignacion_id: int, datos: AsignacionEgreso, session: Session = Depends(get_session)):
    return hogar_transito_service.registrar_egreso(session, asignacion_id, datos)
