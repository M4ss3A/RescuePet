from datetime import date

from pydantic import Field

from app.schemas.base import CamelModel


class HogarTransitoCreate(CamelModel):
    direccion: str = Field(min_length=1, max_length=255)
    capacidad: int = Field(ge=1, le=20)
    disponible: bool = True
    observaciones: str | None = None


class HogarTransitoUpdate(CamelModel):
    """Datos modificables del hogar. El responsable no se cambia."""

    direccion: str | None = Field(default=None, min_length=1, max_length=255)
    capacidad: int | None = Field(default=None, ge=1, le=20)
    disponible: bool | None = None
    observaciones: str | None = None


class HogarTransitoRead(CamelModel):
    id: int
    responsable_id: int
    direccion: str
    capacidad: int
    disponible: bool
    observaciones: str | None


class AsignacionCreate(CamelModel):
    """Ingreso de un animal a un hogar de tránsito."""

    animal_id: int
    fecha_ingreso: date
    observaciones: str | None = None


class AsignacionEgreso(CamelModel):
    """Salida del animal del hogar de tránsito."""

    fecha_salida: date
    observaciones: str | None = None


class AsignacionRead(CamelModel):
    id: int
    animal_id: int
    hogar_transito_id: int
    fecha_ingreso: date
    fecha_salida: date | None
    observaciones: str | None
