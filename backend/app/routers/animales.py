from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.models.enums import EstadoAnimal
from app.schemas.animal import AnimalCreate, AnimalRead, AnimalUpdate
from app.services import animal_service

router = APIRouter(prefix="/api/animales", tags=["Animales"])


@router.get("", response_model=list[AnimalRead])
def listar_animales(estado: EstadoAnimal | None = None, session: Session = Depends(get_session)):
    """Lista los animales. Con ?estado=DISPONIBLE devuelve solo los disponibles."""
    return animal_service.listar_animales(session, estado)


@router.get("/{animal_id}", response_model=AnimalRead)
def obtener_animal(animal_id: int, session: Session = Depends(get_session)):
    return animal_service.obtener_animal(session, animal_id)


@router.post("", response_model=AnimalRead, status_code=status.HTTP_201_CREATED)
def crear_animal(datos: AnimalCreate, session: Session = Depends(get_session)):
    return animal_service.crear_animal(session, datos)


@router.patch("/{animal_id}", response_model=AnimalRead)
def actualizar_animal(animal_id: int, datos: AnimalUpdate, session: Session = Depends(get_session)):
    return animal_service.actualizar_animal(session, animal_id, datos)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def dar_de_baja_animal(animal_id: int, session: Session = Depends(get_session)):
    animal_service.dar_de_baja_animal(session, animal_id)