from fastapi import APIRouter, Depends, status

from app.core.deps import GestorAnimales, Rescatista
from app.core.uow import UnitOfWork
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate
from app.services.rescate_service import RescateService


router = APIRouter(prefix="/api/v1/animales/{animal_id}/rescate", tags=["Rescates"])


def get_rescate_service() -> RescateService:
    return RescateService(UnitOfWork())


@router.get("", response_model=RescateRead)
def obtener_rescate(animal_id: int, _usuario: GestorAnimales, service: RescateService = Depends(get_rescate_service)):
    return service.obtener(animal_id)


@router.post("", response_model=RescateRead, status_code=status.HTTP_201_CREATED)
def registrar_rescate(
    animal_id: int, datos: RescateCreate, rescatista: Rescatista, service: RescateService = Depends(get_rescate_service)
):
    """El rescatista es el usuario logueado."""
    return service.registrar(animal_id, datos, rescatista)


@router.patch("", response_model=RescateRead)
def actualizar_rescate(
    animal_id: int, datos: RescateUpdate, usuario: GestorAnimales, service: RescateService = Depends(get_rescate_service)
):
    return service.actualizar(animal_id, datos, usuario)
