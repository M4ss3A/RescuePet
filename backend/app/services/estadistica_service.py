from enum import Enum

from app.core.uow import UnitOfWork
from app.models.enums import EstadoAnimal, EstadoSolicitud
from app.schemas.estadistica import ConteoPorEstado, ConteoPorMes, Estadisticas, ResumenGeneral


def _por_estado(conteos: dict[str, int], estados: type[Enum]) -> list[ConteoPorEstado]:
    """Incluye todos los estados posibles, con 0 los que no tienen registros."""
    return [ConteoPorEstado(estado=e.value, cantidad=conteos.get(e.value, 0)) for e in estados]


class EstadisticaService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def obtener(self) -> Estadisticas:
        with self.uow:
            repo = self.uow.estadisticas
            animales = repo.animales_por_estado()
            hogares = repo.hogares_por_disponibilidad()

            return Estadisticas(
                resumen=ResumenGeneral(
                    total_animales=sum(animales.values()),
                    disponibles=animales.get(EstadoAnimal.DISPONIBLE.value, 0),
                    hogares_activos=hogares.get("True", 0),
                    animales_en_hogares=repo.animales_alojados(),
                    total_adopciones=repo.total_adopciones(),
                ),
                animales_por_estado=_por_estado(animales, EstadoAnimal),
                solicitudes_por_estado=_por_estado(repo.solicitudes_por_estado(), EstadoSolicitud),
                adopciones_por_mes=[
                    ConteoPorMes(mes=f"{anio:04d}-{mes:02d}", cantidad=cantidad)
                    for anio, mes, cantidad in repo.adopciones_por_mes()
                ],
            )