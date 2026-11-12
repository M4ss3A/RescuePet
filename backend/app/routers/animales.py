from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork
from app.models.enums import EstadoAnimal
from app.schemas.animal import AnimalCreate, AnimalRead, AnimalUpdate
from app.services.animal_service import AnimalService

router = APIRouter(prefix="/api/v1/animales", tags=["Animales"])


def get_animal_service() -> AnimalService:
    """Construye el service con su Unit of Work. FastAPI lo inyecta con Depends."""
    return AnimalService(UnitOfWork())


@router.get("", response_model=list[AnimalRead])
def listar_animales(estado: EstadoAnimal | None = None, service: AnimalService = Depends(get_animal_service)):
    """Lista los animales. Con ?estado=DISPONIBLE devuelve solo los disponibles."""
    return service.listar(estado)


@router.get("/{animal_id}", response_model=AnimalRead)
def obtener_animal(animal_id: int, service: AnimalService = Depends(get_animal_service)):
    return service.obtener(animal_id)


@router.post("", response_model=AnimalRead, status_code=status.HTTP_201_CREATED)
def crear_animal(datos: AnimalCreate, service: AnimalService = Depends(get_animal_service)):
    return service.crear(datos)


@router.patch("/{animal_id}", response_model=AnimalRead)
def actualizar_animal(animal_id: int, datos: AnimalUpdate, service: AnimalService = Depends(get_animal_service)):
    return service.actualizar(animal_id, datos)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def dar_de_baja_animal(animal_id: int, service: AnimalService = Depends(get_animal_service)):
    service.dar_de_baja(animal_id)
