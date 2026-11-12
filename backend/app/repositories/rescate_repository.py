from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import Rescate


class RescateRepository(BaseRepository[Rescate]):
    modelo = Rescate

    def obtener_por_animal(self, animal_id: int) -> Rescate | None:
        consulta = select(Rescate).where(col(Rescate.animal_id) == animal_id)
        return self.session.exec(consulta).first()
