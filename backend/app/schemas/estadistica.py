from app.schemas.base import CamelModel


class ConteoPorEstado(CamelModel):
    estado: str
    cantidad: int


class ConteoPorMes(CamelModel):
    mes: str  # formato "AAAA-MM"
    cantidad: int


class ResumenGeneral(CamelModel):
    total_animales: int
    disponibles: int
    hogares_activos: int
    animales_en_hogares: int
    total_adopciones: int


class Estadisticas(CamelModel):

    resumen: ResumenGeneral
    animales_por_estado: list[ConteoPorEstado]
    solicitudes_por_estado: list[ConteoPorEstado]
    adopciones_por_mes: list[ConteoPorMes]