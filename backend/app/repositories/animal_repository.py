from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import Animal, FotoAnimal
from app.models.enums import EstadoAnimal


class AnimalRepository(BaseRepository[Animal]):
    modelo = Animal

    def listar(self, estado: EstadoAnimal | None = None) -> list[Animal]:
        consulta = select(Animal).order_by(col(Animal.id))
        if estado is not None:
            consulta = consulta.where(col(Animal.estado) == estado)
        return list(self.session.exec(consulta).all())

    def obtener_foto_principal(self, animal_id: int) -> FotoAnimal | None:
        consulta = select(FotoAnimal).where(col(FotoAnimal.animal_id) == animal_id, col(FotoAnimal.es_principal))
        return self.session.exec(consulta).first()

    def guardar_foto(self, foto: FotoAnimal) -> FotoAnimal:
        self.session.add(foto)
        self.session.flush()
        return foto
