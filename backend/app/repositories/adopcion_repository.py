from sqlmodel import col, or_, select

from app.core.base_repository import BaseRepository
from app.models import Adopcion, Publicacion, Seguimiento, SolicitudAdopcion


class AdopcionRepository(BaseRepository[Adopcion]):
    modelo = Adopcion

    def listar(self, solicitud_id: int | None = None, usuario_id: int | None = None) -> list[Adopcion]:
        """Con usuario_id, devuelve las adopciones donde participa: como autor de la publicación
        o como adoptante."""
        consulta = (
            select(Adopcion)
            .join(SolicitudAdopcion)
            .join(Publicacion)
            .order_by(col(Adopcion.fecha_adopcion).desc())
        )
        if solicitud_id is not None:
            consulta = consulta.where(col(Adopcion.solicitud_id) == solicitud_id)
        if usuario_id is not None:
            consulta = consulta.where(
                or_(col(Publicacion.autor_id) == usuario_id, col(SolicitudAdopcion.adoptante_id) == usuario_id)
            )
        return list(self.session.exec(consulta).all())


class SeguimientoRepository(BaseRepository[Seguimiento]):
    modelo = Seguimiento

    def listar_por_adopcion(self, adopcion_id: int) -> list[Seguimiento]:
        consulta = (
            select(Seguimiento)
            .where(col(Seguimiento.adopcion_id) == adopcion_id)
            .order_by(col(Seguimiento.fecha), col(Seguimiento.id))
        )
        return list(self.session.exec(consulta).all())