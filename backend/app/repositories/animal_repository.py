from sqlmodel import Session, select

from app.models import Animal, FotoAnimal
from app.models.enums import EstadoAnimal


def listar(session: Session, estado: EstadoAnimal | None = None) -> list[Animal]:
    consulta = select(Animal).order_by(Animal.id) # type: ignore
    if estado is not None:
        consulta = consulta.where(Animal.estado == estado)
    return list(session.exec(consulta).all())


def obtener_por_id(session: Session, animal_id: int) -> Animal | None:
    return session.get(Animal, animal_id)


def guardar(session: Session, animal: Animal) -> Animal:
    session.add(animal)
    session.commit()
    session.refresh(animal)
    return animal


def obtener_foto_principal(session: Session, animal_id: int) -> FotoAnimal | None:
    consulta = select(FotoAnimal).where(FotoAnimal.animal_id == animal_id, FotoAnimal.es_principal)
    return session.exec(consulta).first()


def guardar_foto(session: Session, foto: FotoAnimal) -> FotoAnimal:
    session.add(foto)
    session.commit()
    session.refresh(foto)
    return foto