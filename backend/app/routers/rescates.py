from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate
from app.services.rescate_service import RescateService

# El rescate pertenece a un animal (relación 1:1), por eso la ruta cuelga de /animales/{id}
router = APIRouter(prefix="/api/v1/animales/{animal_id}/rescate", tags=["Rescates"])


def get_rescate_service() -> RescateService:
    return RescateService(UnitOfWork())


@router.get("", response_model=RescateRead)
def obtener_rescate(animal_id: int, service: RescateService = Depends(get_rescate_service)):
    return service.obtener(animal_id)


@router.post("", response_model=RescateRead, status_code=status.HTTP_201_CREATED)
def registrar_rescate(animal_id: int, datos: RescateCreate, service: RescateService = Depends(get_rescate_service)):
    return service.registrar(animal_id, datos)


@router.patch("", response_model=RescateRead)
def actualizar_rescate(animal_id: int, datos: RescateUpdate, service: RescateService = Depends(get_rescate_service)):
    return service.actualizar(animal_id, datos)
