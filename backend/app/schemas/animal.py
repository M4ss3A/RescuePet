from datetime import datetime

from pydantic import Field

from app.models.enums import Especie, EstadoAnimal, Sexo, Tamano
from app.schemas.base import CamelModel


class AnimalCreate(CamelModel):
    """Datos que se reciben para dar de alta un animal."""

    nombre: str = Field(min_length=1, max_length=100)
    especie: Especie
    raza: str | None = Field(default=None, max_length=100)
    sexo: Sexo | None = None
    edad_aproximada: int | None = Field(default=None, ge=0, le=40)
    tamano: Tamano | None = None
    descripcion: str | None = None
    estado: EstadoAnimal = EstadoAnimal.DISPONIBLE
    foto_url: str | None = Field(default=None, max_length=500)


class AnimalUpdate(CamelModel):
    """Datos que se pueden modificar. Todos son opcionales: solo se cambia lo que se envía."""

    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    especie: Especie | None = None
    raza: str | None = Field(default=None, max_length=100)
    sexo: Sexo | None = None
    edad_aproximada: int | None = Field(default=None, ge=0, le=40)
    tamano: Tamano | None = None
    descripcion: str | None = None
    estado: EstadoAnimal | None = None
    foto_url: str | None = Field(default=None, max_length=500)


class AnimalRead(CamelModel):
    """Datos que devuelve la API sobre un animal."""

    id: int
    nombre: str
    especie: Especie
    raza: str | None
    sexo: Sexo | None
    edad_aproximada: int | None
    tamano: Tamano | None
    descripcion: str | None
    estado: EstadoAnimal
    fecha_alta: datetime
    foto_url: str | None = None