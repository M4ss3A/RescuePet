from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import Adoptante, GestorAnimales, UsuarioActual
from app.core.uow import UnitOfWork
from app.models.enums import EstadoSolicitud
from app.schemas.adopcion import AdopcionRead
from app.schemas.solicitud import AprobacionDatos, SolicitudCreate, SolicitudRead
from app.services.solicitud_service import SolicitudService

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Solicitudes de adopción"])


def get_solicitud_service() -> SolicitudService:
    return SolicitudService(UnitOfWork())


Servicio = Annotated[SolicitudService, Depends(get_solicitud_service)]


@router.post("", response_model=SolicitudRead, status_code=status.HTTP_201_CREATED)
def crear_solicitud(datos: SolicitudCreate, adoptante: Adoptante, service: Servicio):
    return service.crear(datos, adoptante)


@router.get("/mias", response_model=list[SolicitudRead])
def mis_solicitudes(adoptante: Adoptante, service: Servicio):
    return service.listar_mias(adoptante)


@router.get("", response_model=list[SolicitudRead])
def solicitudes_recibidas(usuario: GestorAnimales, service: Servicio, estado: EstadoSolicitud | None = None):
    return service.listar_recibidas(usuario, estado)


@router.get("/{solicitud_id}", response_model=SolicitudRead)
def obtener_solicitud(solicitud_id: int, usuario: UsuarioActual, service: Servicio):
    return service.obtener(solicitud_id, usuario)


@router.post("/{solicitud_id}/cancelar", response_model=SolicitudRead)
def cancelar_solicitud(solicitud_id: int, adoptante: Adoptante, service: Servicio):
    return service.cancelar(solicitud_id, adoptante)


@router.post("/{solicitud_id}/rechazar", response_model=SolicitudRead)
def rechazar_solicitud(solicitud_id: int, usuario: GestorAnimales, service: Servicio):
    return service.rechazar(solicitud_id, usuario)


@router.post("/{solicitud_id}/aprobar", response_model=AdopcionRead, status_code=status.HTTP_201_CREATED)
def aprobar_solicitud(
    solicitud_id: int, usuario: GestorAnimales, service: Servicio, datos: AprobacionDatos | None = None
):
    return service.aprobar(solicitud_id, datos or AprobacionDatos(), usuario)