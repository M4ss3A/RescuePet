from fastapi import HTTPException, status
from sqlmodel import Session

from app.models import Rescate
from app.models.enums import RolNombre
from app.repositories import animal_repository, rescate_repository, usuario_repository
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate


def _verificar_animal(session: Session, animal_id: int) -> None:
    if animal_repository.obtener_por_id(session, animal_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")


def _verificar_rescatista(session: Session, usuario_id: int) -> None:
    """El rescatista tiene que existir y tener el rol RESCATISTA."""
    usuario = usuario_repository.obtener_por_id(session, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rescatista no encontrado")
    if RolNombre.RESCATISTA not in [rol.nombre for rol in usuario.roles]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no tiene el rol RESCATISTA")


def _obtener_o_404(session: Session, animal_id: int) -> Rescate:
    _verificar_animal(session, animal_id)
    rescate = rescate_repository.obtener_por_animal(session, animal_id)
    if rescate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El animal no tiene un rescate registrado")
    return rescate


def obtener_rescate(session: Session, animal_id: int) -> RescateRead:
    return RescateRead.model_validate(_obtener_o_404(session, animal_id))


def registrar_rescate(session: Session, animal_id: int, datos: RescateCreate) -> RescateRead:
    _verificar_animal(session, animal_id)
    if rescate_repository.obtener_por_animal(session, animal_id) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El animal ya tiene un rescate registrado")
    _verificar_rescatista(session, datos.rescatista_id)
    rescate = Rescate(animal_id=animal_id, **datos.model_dump())
    return RescateRead.model_validate(rescate_repository.guardar(session, rescate))


def actualizar_rescate(session: Session, animal_id: int, datos: RescateUpdate) -> RescateRead:
    rescate = _obtener_o_404(session, animal_id)
    rescate.sqlmodel_update(datos.model_dump(exclude_unset=True))
    return RescateRead.model_validate(rescate_repository.guardar(session, rescate))