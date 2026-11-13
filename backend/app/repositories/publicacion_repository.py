from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import Publicacion
from app.models.enums import EstadoPublicacion


class PublicacionRepository(BaseRepository[Publicacion]):
    modelo = Publicacion

    def listar(self, estado: EstadoPublicacion | None = None, autor_id: int | None = None) -> list[Publicacion]:
        consulta = select(Publicacion).order_by(col(Publicacion.fecha_publicacion).desc())
        if estado is not None:
            consulta = consulta.where(col(Publicacion.estado) == estado)
        if autor_id is not None:
            consulta = consulta.where(col(Publicacion.autor_id) == autor_id)
        return list(self.session.exec(consulta).all())

    def obtener_vigente_de_animal(self, animal_id: int) -> Publicacion | None:
        """Publicación ACTIVA o PAUSADA del animal (como máximo hay una que no esté finalizada)."""
        consulta = select(Publicacion).where(
            col(Publicacion.animal_id) == animal_id,
            col(Publicacion.estado) != EstadoPublicacion.FINALIZADA,
        )
        return self.session.exec(consulta).first()
