from datetime import date
from typing import Any

from sqlmodel import Session, col, func, select

from app.models import Adopcion, Animal, AsignacionTransito, HogarTransito, SolicitudAdopcion


class EstadisticaRepository:
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def _contar_por(self, columna: Any) -> dict[str, int]:
        consulta = select(columna, func.count()).group_by(columna)
        return {str(valor): cantidad for valor, cantidad in self.session.exec(consulta).all()}

    def animales_por_estado(self) -> dict[str, int]:
        return self._contar_por(col(Animal.estado))

    def solicitudes_por_estado(self) -> dict[str, int]:
        return self._contar_por(col(SolicitudAdopcion.estado))

    def adopciones_por_estado(self) -> dict[str, int]:
        return self._contar_por(col(Adopcion.estado))

    def adopciones_desde(self, fecha: date) -> int:
        consulta = select(func.count()).select_from(Adopcion).where(col(Adopcion.fecha_adopcion) >= fecha)
        return self.session.exec(consulta).one()

    def hogares_por_disponibilidad(self) -> dict[str, int]:
        return self._contar_por(col(HogarTransito.disponible))

    def animales_alojados(self) -> int:
        consulta = select(func.count()).select_from(AsignacionTransito).where(
            col(AsignacionTransito.fecha_salida).is_(None)
        )
        return self.session.exec(consulta).one()