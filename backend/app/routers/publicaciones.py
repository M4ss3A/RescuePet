from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import GestorAnimales
from app.core.uow import UnitOfWork
from app.models.enums import EstadoPublicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionRead, PublicacionUpdate
from app.services.publicacion_service import PublicacionService

router = APIRouter(prefix="/api/v1/publicaciones", tags=["Publicaciones"])


def get_publicacion_service() -> PublicacionService:
    return PublicacionService(UnitOfWork())


Servicio = Annotated[PublicacionService, Depends(get_publicacion_service)]


@router.get("", response_model=list[PublicacionRead])
def listar_publicaciones(service: Servicio, estado: EstadoPublicacion | None = None):
    return service.listar(estado)


@router.get("/{publicacion_id}", response_model=PublicacionRead)
def obtener_publicacion(publicacion_id: int, service: Servicio):
    return service.obtener(publicacion_id)


@router.post("", response_model=PublicacionRead, status_code=status.HTTP_201_CREATED)
def crear_publicacion(datos: PublicacionCreate, autor: GestorAnimales, service: Servicio):
    return service.crear(datos, autor)


@router.patch("/{publicacion_id}", response_model=PublicacionRead)
def actualizar_publicacion(
    publicacion_id: int, datos: PublicacionUpdate, usuario: GestorAnimales, service: Servicio
):
    return service.actualizar(publicacion_id, datos, usuario)