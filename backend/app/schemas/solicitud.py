from datetime import date, datetime
from decimal import Decimal

from pydantic import Field

from app.models.enums import EstadoSolicitud, TipoVivienda
from app.schemas.base import CamelModel


class SolicitudCreate(CamelModel):
    animal_id: int
    tipo_vivienda: TipoVivienda
    tiene_patio: bool
    tiene_otros_animales: bool
    experiencia_previa: str | None = None
    motivo: str = Field(min_length=1)


class SolicitudRead(CamelModel):
    id: int
    publicacion_id: int
    animal_id: int
    adoptante_id: int
    fecha_solicitud: datetime
    estado: EstadoSolicitud
    tipo_vivienda: TipoVivienda
    tiene_patio: bool
    tiene_otros_animales: bool
    experiencia_previa: str | None
    motivo: str
    puntaje_compatibilidad: Decimal | None


class AprobacionDatos(CamelModel):
    fecha_adopcion: date | None = None
    observaciones: str | None = None