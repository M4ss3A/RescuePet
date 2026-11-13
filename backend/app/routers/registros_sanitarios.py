from fastapi import APIRouter, Depends, status

from app.core.deps import GestorSalud
from app.core.uow import UnitOfWork
from app.schemas.registro_sanitario import (
    RegistroSanitarioCreate,
    RegistroSanitarioRead,
    RegistroSanitarioUpdate,
)
from app.services.registro_sanitario_service import RegistroSanitarioService

router = APIRouter(prefix="/api/v1", tags=["Registros sanitarios"])


def get_registro_sanitario_service() -> RegistroSanitarioService:
    return RegistroSanitarioService(UnitOfWork())


@router.get("/animales/{animal_id}/registros-sanitarios", response_model=list[RegistroSanitarioRead])
def listar_historial(animal_id: int, service: RegistroSanitarioService = Depends(get_registro_sanitario_service)):
    """Público. Historial sanitario del animal, ordenado por fecha."""
    return service.listar_historial(animal_id)


@router.post(
    "/animales/{animal_id}/registros-sanitarios",
    response_model=RegistroSanitarioRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_registro(
    animal_id: int,
    datos: RegistroSanitarioCreate,
    _usuario: GestorSalud,
    service: RegistroSanitarioService = Depends(get_registro_sanitario_service),
):
    return service.crear(animal_id, datos)


@router.patch("/registros-sanitarios/{registro_id}", response_model=RegistroSanitarioRead)
def actualizar_registro(
    registro_id: int,
    datos: RegistroSanitarioUpdate,
    _usuario: GestorSalud,
    service: RegistroSanitarioService = Depends(get_registro_sanitario_service),
):
    return service.actualizar(registro_id, datos)


@router.delete("/registros-sanitarios/{registro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_registro(
    registro_id: int,
    _usuario: GestorSalud,
    service: RegistroSanitarioService = Depends(get_registro_sanitario_service),
):
    service.eliminar(registro_id)