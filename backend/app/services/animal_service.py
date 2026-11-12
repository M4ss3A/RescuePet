from fastapi import HTTPException, status
from sqlmodel import Session

from app.models import Animal, FotoAnimal
from app.models.enums import EstadoAnimal
from app.repositories import animal_repository
from app.schemas.animal import AnimalCreate, AnimalRead, AnimalUpdate


def _a_respuesta(session: Session, animal: Animal) -> AnimalRead:
    """Convierte el modelo en la respuesta de la API, agregando la URL de la foto principal."""
    respuesta = AnimalRead.model_validate(animal)
    foto = animal_repository.obtener_foto_principal(session, animal.id) # type: ignore
    respuesta.foto_url = foto.url if foto else None
    return respuesta


def _obtener_o_404(session: Session, animal_id: int) -> Animal:
    animal = animal_repository.obtener_por_id(session, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")
    return animal


def _guardar_foto_principal(session: Session, animal_id: int, url: str) -> None:
    """Crea la foto principal del animal o actualiza su URL si ya existía."""
    foto = animal_repository.obtener_foto_principal(session, animal_id)
    if foto is None:
        foto = FotoAnimal(animal_id=animal_id, url=url, es_principal=True)
    else:
        foto.url = url
    animal_repository.guardar_foto(session, foto)


def listar_animales(session: Session, estado: EstadoAnimal | None = None) -> list[AnimalRead]:
    animales = animal_repository.listar(session, estado)
    return [_a_respuesta(session, animal) for animal in animales]


def obtener_animal(session: Session, animal_id: int) -> AnimalRead:
    animal = _obtener_o_404(session, animal_id)
    return _a_respuesta(session, animal)


def crear_animal(session: Session, datos: AnimalCreate) -> AnimalRead:
    animal = Animal(**datos.model_dump(exclude={"foto_url"}))
    animal = animal_repository.guardar(session, animal)
    if datos.foto_url:
        _guardar_foto_principal(session, animal.id, datos.foto_url) # type: ignore
    return _a_respuesta(session, animal)


def actualizar_animal(session: Session, animal_id: int, datos: AnimalUpdate) -> AnimalRead:
    animal = _obtener_o_404(session, animal_id)
    cambios = datos.model_dump(exclude_unset=True, exclude={"foto_url"})
    animal.sqlmodel_update(cambios)
    animal = animal_repository.guardar(session, animal)
    if datos.foto_url:
        _guardar_foto_principal(session, animal.id, datos.foto_url) # type: ignore
    return _a_respuesta(session, animal)


def dar_de_baja_animal(session: Session, animal_id: int) -> None:
    """Baja lógica: el animal no se borra, pasa a INACTIVO para conservar su historial."""
    animal = _obtener_o_404(session, animal_id)
    animal.estado = EstadoAnimal.INACTIVO
    animal_repository.guardar(session, animal)