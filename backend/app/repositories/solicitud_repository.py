from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import Publicacion, SolicitudAdopcion
from app.models.enums import EstadoSolicitud


class SolicitudRepository(BaseRepository[SolicitudAdopcion]):
    modelo = SolicitudAdopcion

    def listar(
        self,
        estado: EstadoSolicitud | None = None,
        adoptante_id: int | None = None,
        autor_publicacion_id: int | None = None,
    ) -> list[SolicitudAdopcion]:
        consulta = select(SolicitudAdopcion).order_by(col(SolicitudAdopcion.fecha_solicitud).desc())
        if estado is not None:
            consulta = consulta.where(col(SolicitudAdopcion.estado) == estado)
        if adoptante_id is not None:
            consulta = consulta.where(col(SolicitudAdopcion.adoptante_id) == adoptante_id)
        if autor_publicacion_id is not None:
            consulta = consulta.join(Publicacion).where(col(Publicacion.autor_id) == autor_publicacion_id)
        return list(self.session.exec(consulta).all())

    def obtener_de_adoptante(self, publicacion_id: int, adoptante_id: int) -> SolicitudAdopcion | None:
        consulta = select(SolicitudAdopcion).where(
            col(SolicitudAdopcion.publicacion_id) == publicacion_id,
            col(SolicitudAdopcion.adoptante_id) == adoptante_id,
        )
        return self.session.exec(consulta).first()

    def listar_pendientes_de_publicacion(self, publicacion_id: int) -> list[SolicitudAdopcion]:
        consulta = select(SolicitudAdopcion).where(
            col(SolicitudAdopcion.publicacion_id) == publicacion_id,
            col(SolicitudAdopcion.estado) == EstadoSolicitud.PENDIENTE,
        )
        return list(self.session.exec(consulta).all())