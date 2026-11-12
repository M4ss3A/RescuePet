from datetime import date

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models import RegistroSanitario
from app.repositories import animal_repository, registro_sanitario_repository
from app.schemas.registro_sanitario import (
    RegistroSanitarioCreate,
    RegistroSanitarioRead,
    RegistroSanitarioUpdate,
)


def _verificar_animal(session: Session, animal_id: int) -> None:
    if animal_repository.obtener_por_id(session, animal_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")


def _verificar_fecha(fecha: date | None) -> None:
    """Un registro sanitario documenta algo que ya ocurrió: no puede tener fecha futura."""
    if fecha is not None and fecha > date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha no puede ser futura")


def _obtener_o_404(session: Session, registro_id: int) -> RegistroSanitario:
    registro = registro_sanitario_repository.obtener_por_id(session, registro_id)
    if registro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro sanitario no encontrado")
    return registro


def listar_historial(session: Session, animal_id: int) -> list[RegistroSanitarioRead]:
    _verificar_animal(session, animal_id)
    registros = registro_sanitario_repository.listar_por_animal(session, animal_id)
    return [RegistroSanitarioRead.model_validate(r) for r in registros]


def crear_registro(session: Session, animal_id: int, datos: RegistroSanitarioCreate) -> RegistroSanitarioRead:
    _verificar_animal(session, animal_id)
    _verificar_fecha(datos.fecha)
    registro = RegistroSanitario(animal_id=animal_id, **datos.model_dump())
    return RegistroSanitarioRead.model_validate(registro_sanitario_repository.guardar(session, registro))


def actualizar_registro(session: Session, registro_id: int, datos: RegistroSanitarioUpdate) -> RegistroSanitarioRead:
    registro = _obtener_o_404(session, registro_id)
    _verificar_fecha(datos.fecha)
    registro.sqlmodel_update(datos.model_dump(exclude_unset=True))
    return RegistroSanitarioRead.model_validate(registro_sanitario_repository.guardar(session, registro))


def eliminar_registro(session: Session, registro_id: int) -> None:
    """Borrado físico: se usa para corregir un registro cargado por error."""
    registro = _obtener_o_404(session, registro_id)
    registro_sanitario_repository.eliminar(session, registro)