from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import GestorAnimales, UsuarioActual
from app.core.uow import UnitOfWork
from app.schemas.adopcion import AdopcionRead, AdopcionUpdate, SeguimientoCreate, SeguimientoRead
from app.services.adopcion_service import AdopcionService

router = APIRouter(prefix="/api/v1/adopciones", tags=["Adopciones y seguimientos"])


def get_adopcion_service() -> AdopcionService:
    return AdopcionService(UnitOfWork())


Servicio = Annotated[AdopcionService, Depends(get_adopcion_service)]


@router.get("", response_model=list[AdopcionRead])
def listar_adopciones(usuario: UsuarioActual, service: Servicio, solicitud_id: int | None = None):
    return service.listar(usuario, solicitud_id)


@router.get("/{adopcion_id}", response_model=AdopcionRead)
def obtener_adopcion(adopcion_id: int, usuario: UsuarioActual, service: Servicio):
    return service.obtener(adopcion_id, usuario)


@router.patch("/{adopcion_id}", response_model=AdopcionRead)
def actualizar_adopcion(adopcion_id: int, datos: AdopcionUpdate, usuario: GestorAnimales, service: Servicio):
    return service.actualizar(adopcion_id, datos, usuario)


@router.get("/{adopcion_id}/seguimientos", response_model=list[SeguimientoRead])
def listar_seguimientos(adopcion_id: int, usuario: UsuarioActual, service: Servicio):
    return service.listar_seguimientos(adopcion_id, usuario)


@router.post("/{adopcion_id}/seguimientos", response_model=SeguimientoRead, status_code=status.HTTP_201_CREATED)
def crear_seguimiento(adopcion_id: int, datos: SeguimientoCreate, usuario: GestorAnimales, service: Servicio):
    return service.crear_seguimiento(adopcion_id, datos, usuario)