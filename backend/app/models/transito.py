from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Index, Text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.animal import Animal
    from app.models.usuario import Usuario


class HogarTransito(SQLModel, table=True):
    __tablename__ = "hogares_transito" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    responsable_id: int = Field(foreign_key="usuarios.id")
    direccion: str = Field(max_length=255)
    capacidad: int
    disponible: bool = Field(default=True, index=True)
    observaciones: str | None = Field(default=None, sa_type=Text)

    responsable: "Usuario" = Relationship(back_populates="hogares_transito")
    asignaciones: list["AsignacionTransito"] = Relationship(back_populates="hogar_transito")


class AsignacionTransito(SQLModel, table=True):
    """Registra la estadía de un animal en un hogar. fecha_salida vacía = asignación actual."""

    __tablename__ = "asignaciones_transito" # type: ignore
    __table_args__ = (Index("idx_asignaciones_animal_salida", "animal_id", "fecha_salida"),)

    id: int | None = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animales.id")
    hogar_transito_id: int = Field(foreign_key="hogares_transito.id")
    fecha_ingreso: date
    fecha_salida: date | None = None
    observaciones: str | None = Field(default=None, sa_type=Text)

    animal: "Animal" = Relationship(back_populates="asignaciones_transito")
    hogar_transito: HogarTransito = Relationship(back_populates="asignaciones")