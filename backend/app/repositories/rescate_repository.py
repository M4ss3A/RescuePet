from sqlmodel import Session, col, select

from app.models import Rescate


def obtener_por_animal(session: Session, animal_id: int) -> Rescate | None:
    consulta = select(Rescate).where(col(Rescate.animal_id) == animal_id)
    return session.exec(consulta).first()


def guardar(session: Session, rescate: Rescate) -> Rescate:
    session.add(rescate)
    session.commit()
    session.refresh(rescate)
    return rescate