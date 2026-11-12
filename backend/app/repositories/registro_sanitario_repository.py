from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import RegistroSanitario


class RegistroSanitarioRepository(BaseRepository[RegistroSanitario]):
    modelo = RegistroSanitario

    def listar_por_animal(self, animal_id: int) -> list[RegistroSanitario]:
        consulta = (
            select(RegistroSanitario)
            .where(col(RegistroSanitario.animal_id) == animal_id)
            .order_by(col(RegistroSanitario.fecha), col(RegistroSanitario.id))
        )
        return list(self.session.exec(consulta).all())
