from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate
from app.services import rescate_service


router = APIRouter(prefix="/api/animales/{animal_id}/rescate", tags=["Rescates"])


@router.get("", response_model=RescateRead)
def obtener_rescate(animal_id: int, session: Session = Depends(get_session)):
    return rescate_service.obtener_rescate(session, animal_id)


@router.post("", response_model=RescateRead, status_code=status.HTTP_201_CREATED)
def registrar_rescate(animal_id: int, datos: RescateCreate, session: Session = Depends(get_session)):
    return rescate_service.registrar_rescate(session, animal_id, datos)


@router.patch("", response_model=RescateRead)
def actualizar_rescate(animal_id: int, datos: RescateUpdate, session: Session = Depends(get_session)):
    return rescate_service.actualizar_rescate(session, animal_id, datos)