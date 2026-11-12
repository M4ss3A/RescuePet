from sqlmodel import col, select

from app.core.base_repository import BaseRepository
from app.models import AsignacionTransito, HogarTransito


class HogarTransitoRepository(BaseRepository[HogarTransito]):
    modelo = HogarTransito

    def listar(self, disponible: bool | None = None) -> list[HogarTransito]:
        consulta = select(HogarTransito).order_by(col(HogarTransito.id))
        if disponible is not None:
            consulta = consulta.where(col(HogarTransito.disponible) == disponible)
        return list(self.session.exec(consulta).all())


class AsignacionTransitoRepository(BaseRepository[AsignacionTransito]):
    modelo = AsignacionTransito

    def listar_por_hogar(self, hogar_id: int, solo_activas: bool = False) -> list[AsignacionTransito]:
        consulta = (
            select(AsignacionTransito)
            .where(col(AsignacionTransito.hogar_transito_id) == hogar_id)
            .order_by(col(AsignacionTransito.fecha_ingreso))
        )
        if solo_activas:
            consulta = consulta.where(col(AsignacionTransito.fecha_salida).is_(None))
        return list(self.session.exec(consulta).all())

    def contar_activas(self, hogar_id: int) -> int:
        return len(self.listar_por_hogar(hogar_id, solo_activas=True))

    def obtener_activa_de_animal(self, animal_id: int) -> AsignacionTransito | None:
        consulta = select(AsignacionTransito).where(
            col(AsignacionTransito.animal_id) == animal_id,
            col(AsignacionTransito.fecha_salida).is_(None),
        )
        return self.session.exec(consulta).first()
