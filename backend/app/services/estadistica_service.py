from datetime import date
from enum import Enum

from app.core.uow import UnitOfWork
from app.models.enums import EstadoAdopcion, EstadoAnimal, EstadoSolicitud
from app.schemas.estadistica import (
    Estadisticas,
    ResumenAdopciones,
    ResumenAnimales,
    ResumenHogares,
    ResumenSolicitudes,
)


def _completar(conteos: dict[str, int], estados: type[Enum]) -> dict[str, int]:
    """Incluye todos los estados posibles, con 0 los que no tienen registros."""
    return {estado.value: conteos.get(estado.value, 0) for estado in estados}


class EstadisticaService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def obtener(self) -> Estadisticas:
        with self.uow:
            repo = self.uow.estadisticas

            animales = _completar(repo.animales_por_estado(), EstadoAnimal)
            solicitudes = _completar(repo.solicitudes_por_estado(), EstadoSolicitud)
            adopciones = _completar(repo.adopciones_por_estado(), EstadoAdopcion)
            hogares = repo.hogares_por_disponibilidad()
            primer_dia_del_mes = date.today().replace(day=1)

            return Estadisticas(
                animales=ResumenAnimales(total=sum(animales.values()), por_estado=animales),
                solicitudes=ResumenSolicitudes(total=sum(solicitudes.values()), por_estado=solicitudes),
                adopciones=ResumenAdopciones(
                    total=sum(adopciones.values()),
                    en_seguimiento=adopciones[EstadoAdopcion.EN_SEGUIMIENTO.value],
                    finalizadas=adopciones[EstadoAdopcion.FINALIZADA.value],
                    del_mes=repo.adopciones_desde(primer_dia_del_mes),
                ),
                hogares_transito=ResumenHogares(
                    total=sum(hogares.values()),
                    disponibles=hogares.get("True", 0),
                    animales_alojados=repo.animales_alojados(),
                ),
            )