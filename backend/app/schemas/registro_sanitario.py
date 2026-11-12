from datetime import date

from pydantic import Field

from app.models.enums import TipoRegistroSanitario
from app.schemas.base import CamelModel


class RegistroSanitarioCreate(CamelModel):
    """Datos para cargar una vacuna, tratamiento o consulta veterinaria."""

    tipo: TipoRegistroSanitario
    fecha: date
    descripcion: str = Field(min_length=1)
    veterinario: str | None = Field(default=None, max_length=150)


class RegistroSanitarioUpdate(CamelModel):
    tipo: TipoRegistroSanitario | None = None
    fecha: date | None = None
    descripcion: str | None = Field(default=None, min_length=1)
    veterinario: str | None = Field(default=None, max_length=150)


class RegistroSanitarioRead(CamelModel):
    id: int
    animal_id: int
    tipo: TipoRegistroSanitario
    fecha: date
    descripcion: str
    veterinario: str | None