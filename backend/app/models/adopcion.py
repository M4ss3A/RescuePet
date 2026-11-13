from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ahora_utc
from app.models.enums import EstadoAdopcion, EstadoPublicacion, EstadoSolicitud, TipoVivienda

if TYPE_CHECKING:
    from app.models.animal import Animal
    from app.models.usuario import Usuario


class Publicacion(SQLModel, table=True):
    __tablename__ = "publicaciones" # type: ignore
    __table_args__ = (Index("idx_publicaciones_estado_fecha", "estado", "fecha_publicacion"),)

    id: int | None = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animales.id")
    autor_id: int = Field(foreign_key="usuarios.id")
    titulo: str = Field(max_length=150)
    descripcion: str = Field(sa_type=Text)
    fecha_publicacion: datetime = Field(default_factory=ahora_utc)
    estado: EstadoPublicacion = Field(default=EstadoPublicacion.ACTIVA, sa_type=String(30))

    animal: "Animal" = Relationship(back_populates="publicaciones")
    autor: "Usuario" = Relationship(back_populates="publicaciones")
    solicitudes: list["SolicitudAdopcion"] = Relationship(back_populates="publicacion")


class SolicitudAdopcion(SQLModel, table=True):
    __tablename__ = "solicitudes_adopcion" # type: ignore
    __table_args__ = (
        # Un adoptante no puede enviar dos solicitudes a la misma publicación
        UniqueConstraint("publicacion_id", "adoptante_id", name="uq_solicitud_publicacion_adoptante"),
        Index("idx_solicitudes_publicacion_estado", "publicacion_id", "estado"),
        Index("idx_solicitudes_adoptante_estado", "adoptante_id", "estado"),
    )

    id: int | None = Field(default=None, primary_key=True)
    publicacion_id: int = Field(foreign_key="publicaciones.id")
    adoptante_id: int = Field(foreign_key="usuarios.id")
    fecha_solicitud: datetime = Field(default_factory=ahora_utc)
    estado: EstadoSolicitud = Field(default=EstadoSolicitud.PENDIENTE, sa_type=String(30))
    tipo_vivienda: TipoVivienda = Field(sa_type=String(50))
    tiene_patio: bool
    tiene_otros_animales: bool
    experiencia_previa: str | None = Field(default=None, sa_type=Text)
    motivo: str = Field(sa_type=Text)
    puntaje_compatibilidad: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)

    publicacion: Publicacion = Relationship(back_populates="solicitudes")
    adoptante: "Usuario" = Relationship(back_populates="solicitudes")
    adopcion: "Adopcion" = Relationship(back_populates="solicitud", sa_relationship_kwargs={"uselist": False})


class Adopcion(SQLModel, table=True):
    """Relación 1:1 con SolicitudAdopcion: se crea a partir de una solicitud aprobada."""

    __tablename__ = "adopciones" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    solicitud_id: int = Field(foreign_key="solicitudes_adopcion.id", unique=True)
    fecha_adopcion: date
    estado: EstadoAdopcion = Field(default=EstadoAdopcion.EN_SEGUIMIENTO, sa_type=String(30))
    observaciones: str | None = Field(default=None, sa_type=Text)

    solicitud: SolicitudAdopcion = Relationship(back_populates="adopcion")
    seguimientos: list["Seguimiento"] = Relationship(back_populates="adopcion")


class Seguimiento(SQLModel, table=True):
    __tablename__ = "seguimientos" # type: ignore
    __table_args__ = (Index("idx_seguimientos_adopcion_fecha", "adopcion_id", "fecha"),)

    id: int | None = Field(default=None, primary_key=True)
    adopcion_id: int = Field(foreign_key="adopciones.id")
    fecha: date
    observaciones: str | None = Field(default=None, sa_type=Text)
    estado_general: str | None = Field(default=None, max_length=100)
    resultado: str | None = Field(default=None, max_length=100)

    adopcion: Adopcion = Relationship(back_populates="seguimientos")