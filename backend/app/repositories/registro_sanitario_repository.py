from sqlmodel import Session, col, select

from app.models import RegistroSanitario


def listar_por_animal(session: Session, animal_id: int) -> list[RegistroSanitario]:
    consulta = (
        select(RegistroSanitario)
        .where(col(RegistroSanitario.animal_id) == animal_id)
        .order_by(col(RegistroSanitario.fecha), col(RegistroSanitario.id))
    )
    return list(session.exec(consulta).all())


def obtener_por_id(session: Session, registro_id: int) -> RegistroSanitario | None:
    return session.get(RegistroSanitario, registro_id)


def guardar(session: Session, registro: RegistroSanitario) -> RegistroSanitario:
    session.add(registro)
    session.commit()
    session.refresh(registro)
    return registro


def eliminar(session: Session, registro: RegistroSanitario) -> None:
    session.delete(registro)
    session.commit()