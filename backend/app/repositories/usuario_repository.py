from sqlmodel import Session

from app.models import Usuario


def obtener_por_id(session: Session, usuario_id: int) -> Usuario | None:
    return session.get(Usuario, usuario_id)