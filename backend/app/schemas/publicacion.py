from datetime import datetime

from pydantic import Field, field_validator

from app.models.enums import EstadoPublicacion
from app.schemas.base import CamelModel


class PublicacionCreate(CamelModel):
    animal_id: int
    titulo: str = Field(min_length=1, max_length=150)
    descripcion: str = Field(min_length=1)


class PublicacionUpdate(CamelModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, min_length=1)
    estado: EstadoPublicacion | None = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, estado: EstadoPublicacion | None) -> EstadoPublicacion | None:
        if estado == EstadoPublicacion.FINALIZADA:
            raise ValueError("Una publicación se finaliza automáticamente al aprobarse una adopción")
        return estado


class PublicacionRead(CamelModel):
    id: int
    animal_id: int
    autor_id: int
    titulo: str
    descripcion: str
    fecha_publicacion: datetime
    estado: EstadoPublicacion