from typing import TYPE_CHECKING

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ahora_utc

if TYPE_CHECKING:
    from app.models.adopcion import Publicacion, SolicitudAdopcion
    from app.models.animal import Rescate
    from app.models.transito import HogarTransito

class UsuarioRol(SQLModel, table=True):
    """Tabla intermedia de la relación N:N entre usuarios y roles."""

    __tablename__ = "usuario_roles" # type: ignore

    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    rol_id: int = Field(foreign_key="roles.id", primary_key=True, index=True)


class Rol(SQLModel, table=True):
    __tablename__ = "roles" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    descripcion: str | None = Field(default=None, max_length=255)

    usuarios: list["Usuario"] = Relationship(back_populates="roles", link_model=UsuarioRol)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellido: str = Field(max_length=100)
    email: str = Field(max_length=150, unique=True)
    contrasena_hash: str = Field(max_length=255)
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = Field(default=None, max_length=255)
    activo: bool = Field(default=True)
    fecha_registro: datetime = Field(default_factory=ahora_utc)

    roles: list[Rol] = Relationship(back_populates="usuarios", link_model=UsuarioRol)


    rescates: list["Rescate"] = Relationship(back_populates="rescatista")
    hogares_transito: list["HogarTransito"] = Relationship(back_populates="responsable")
    publicaciones: list["Publicacion"] = Relationship(back_populates="autor")
    solicitudes: list["SolicitudAdopcion"] = Relationship(back_populates="adoptante")