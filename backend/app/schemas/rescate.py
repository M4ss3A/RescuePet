from datetime import date

from pydantic import Field

from app.schemas.base import CamelModel

class RescateCreate(CamelModel):
    """Datos para registrar el rescate. El rescatista es el usuario logueado, no se envía."""

    fecha_rescate: date
    ubicacion: str = Field(min_length=1, max_length=255)
    descripcion: str | None = None


class RescateUpdate(CamelModel):
    """Datos que se pueden corregir de un rescate. Todos opcionales."""

    fecha_rescate: date | None = None
    ubicacion: str | None = Field(default=None, min_length=1, max_length=255)
    descripcion: str | None = None


class RescateRead(CamelModel):
    id: int
    animal_id: int
    rescatista_id: int
    fecha_rescate: date
    ubicacion: str
    descripcion: str | None