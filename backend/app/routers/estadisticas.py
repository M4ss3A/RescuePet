from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import GestorAnimales
from app.core.uow import UnitOfWork
from app.schemas.estadistica import Estadisticas
from app.services.estadistica_service import EstadisticaService

router = APIRouter(prefix="/api/v1/estadisticas", tags=["Panel de información"])


def get_estadistica_service() -> EstadisticaService:
    return EstadisticaService(UnitOfWork())


@router.get("", response_model=Estadisticas)
def obtener_estadisticas(
    _usuario: GestorAnimales, service: Annotated[EstadisticaService, Depends(get_estadistica_service)]
):
    return service.obtener()