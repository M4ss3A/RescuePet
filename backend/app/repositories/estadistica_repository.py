from typing import Any

from sqlmodel import Session, col, extract, func, select

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

    def total_adopciones(self) -> int:
        return self.session.exec(select(func.count()).select_from(Adopcion)).one()

    def adopciones_por_mes(self) -> list[tuple[int, int, int]]:
        anio = extract("year", col(Adopcion.fecha_adopcion))
        mes = extract("month", col(Adopcion.fecha_adopcion))
        consulta = select(anio, mes, func.count()).group_by(anio, mes).order_by(anio, mes)
        return [(int(a), int(m), c) for a, m, c in self.session.exec(consulta).all()]

    def hogares_por_disponibilidad(self) -> dict[str, int]:
        return self._contar_por(col(HogarTransito.disponible))

    def animales_alojados(self) -> int:
        consulta = select(func.count()).select_from(AsignacionTransito).where(
            col(AsignacionTransito.fecha_salida).is_(None)
        )
        return self.session.exec(consulta).one()
