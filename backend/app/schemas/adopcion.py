from datetime import date

from pydantic import Field

from app.models.enums import EstadoAdopcion
from app.schemas.base import CamelModel


class AdopcionRead(CamelModel):
    id: int
    solicitud_id: int
    animal_id: int
    adoptante_id: int
    fecha_adopcion: date
    estado: EstadoAdopcion
    observaciones: str | None


class AdopcionUpdate(CamelModel):
    estado: EstadoAdopcion | None = None
    observaciones: str | None = None


class SeguimientoCreate(CamelModel):
    fecha: date
    observaciones: str | None = None
    estado_general: str | None = Field(default=None, max_length=100)
    resultado: str | None = Field(default=None, max_length=100)


class SeguimientoRead(CamelModel):
    id: int
    adopcion_id: int
    fecha: date
    observaciones: str | None
    estado_general: str | None
    resultado: str | None