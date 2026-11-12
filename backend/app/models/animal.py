from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Index, String, Text
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ahora_utc
from app.models.enums import Especie, EstadoAnimal, Sexo, Tamano, TipoRegistroSanitario

if TYPE_CHECKING:
    from app.models.adopcion import Publicacion
    from app.models.transito import AsignacionTransito
    from app.models.usuario import Usuario


class Animal(SQLModel, table=True):
    __tablename__ = "animales"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    especie: Especie = Field(sa_type=String(50))
    raza: str | None = Field(default=None, max_length=100)
    sexo: Sexo | None = Field(default=None, sa_type=String(20))
    edad_aproximada: int | None = None
    tamano: Tamano | None = Field(default=None, sa_type=String(30))
    descripcion: str | None = Field(default=None, sa_type=Text)
    estado: EstadoAnimal = Field(default=EstadoAnimal.DISPONIBLE, sa_type=String(30), index=True)
    fecha_alta: datetime = Field(default_factory=ahora_utc)

    rescate: "Rescate" = Relationship(back_populates="animal", sa_relationship_kwargs={"uselist": False})
    fotos: list["FotoAnimal"] = Relationship(back_populates="animal")
    registros_sanitarios: list["RegistroSanitario"] = Relationship(back_populates="animal")
    asignaciones_transito: list["AsignacionTransito"] = Relationship(back_populates="animal")
    publicaciones: list["Publicacion"] = Relationship(back_populates="animal")


class Rescate(SQLModel, table=True):
    """Relación 1:1 con Animal: cada animal tiene un único rescate (animal_id UNIQUE)."""

    __tablename__ = "rescates"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animales.id", unique=True)
    rescatista_id: int = Field(foreign_key="usuarios.id")
    fecha_rescate: date
    ubicacion: str = Field(max_length=255)
    descripcion: str | None = Field(default=None, sa_type=Text)

    animal: Animal = Relationship(back_populates="rescate")
    rescatista: "Usuario" = Relationship(back_populates="rescates")


class FotoAnimal(SQLModel, table=True):
    __tablename__ = "fotos_animal"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animales.id")
    url: str = Field(max_length=500)
    descripcion: str | None = Field(default=None, max_length=255)
    es_principal: bool = Field(default=False)

    animal: Animal = Relationship(back_populates="fotos")


class RegistroSanitario(SQLModel, table=True):
    __tablename__ = "registros_sanitarios"  # type: ignore
    __table_args__ = (Index("idx_registros_sanitarios_animal_fecha", "animal_id", "fecha"),)

    id: int | None = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animales.id")
    tipo: TipoRegistroSanitario = Field(sa_type=String(50))
    fecha: date
    descripcion: str = Field(sa_type=Text)
    veterinario: str | None = Field(default=None, max_length=150)

    animal: Animal = Relationship(back_populates="registros_sanitarios")