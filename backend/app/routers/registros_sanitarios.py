from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.registro_sanitario import (
    RegistroSanitarioCreate,
    RegistroSanitarioRead,
    RegistroSanitarioUpdate,
)
from app.services import registro_sanitario_service

router = APIRouter(prefix="/api", tags=["Registros sanitarios"])


@router.get("/animales/{animal_id}/registros-sanitarios", response_model=list[RegistroSanitarioRead])
def listar_historial(animal_id: int, session: Session = Depends(get_session)):
    """Historial sanitario del animal, ordenado por fecha."""
    return registro_sanitario_service.listar_historial(session, animal_id)


@router.post(
    "/animales/{animal_id}/registros-sanitarios",
    response_model=RegistroSanitarioRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_registro(animal_id: int, datos: RegistroSanitarioCreate, session: Session = Depends(get_session)):
    return registro_sanitario_service.crear_registro(session, animal_id, datos)


@router.patch("/registros-sanitarios/{registro_id}", response_model=RegistroSanitarioRead)
def actualizar_registro(registro_id: int, datos: RegistroSanitarioUpdate, session: Session = Depends(get_session)):
    return registro_sanitario_service.actualizar_registro(session, registro_id, datos)


@router.delete("/registros-sanitarios/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_registro(registro_id: int, session: Session = Depends(get_session)):
    registro_sanitario_service.eliminar_registro(session, registro_id)