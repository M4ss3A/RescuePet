from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import Adopcion, Publicacion, Seguimiento, SolicitudAdopcion


class AdopcionRepository(BaseRepository[Adopcion]):
    modelo = Adopcion

    def listar(
        self,
        solicitud_id: int | None = None,
        adoptante_id: int | None = None,
        autor_publicacion_id: int | None = None,
    ) -> list[Adopcion]:
        consulta = select(Adopcion).join(SolicitudAdopcion).order_by(col(Adopcion.fecha_adopcion).desc())
        if solicitud_id is not None:
            consulta = consulta.where(col(Adopcion.solicitud_id) == solicitud_id)
        if adoptante_id is not None:
            consulta = consulta.where(col(SolicitudAdopcion.adoptante_id) == adoptante_id)
        if autor_publicacion_id is not None:
            consulta = consulta.join(Publicacion).where(col(Publicacion.autor_id) == autor_publicacion_id)
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