from app.schemas.base import CamelModel


class ResumenAnimales(CamelModel):
    total: int
    por_estado: dict[str, int]


class ResumenSolicitudes(CamelModel):
    total: int
    por_estado: dict[str, int]


class ResumenAdopciones(CamelModel):
    total: int
    en_seguimiento: int
    finalizadas: int
    del_mes: int


class ResumenHogares(CamelModel):
    total: int
    disponibles: int
    animales_alojados: int


class Estadisticas(CamelModel):
    animales: ResumenAnimales
    solicitudes: ResumenSolicitudes
    adopciones: ResumenAdopciones
    hogares_transito: ResumenHogares