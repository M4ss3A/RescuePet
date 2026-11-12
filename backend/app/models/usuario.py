from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ahora_utc


class UsuarioRol(SQLModel, table=True):
    """Tabla intermedia de la relación N:N entre usuarios y roles."""

    __tablename__ = "usuario_roles"

    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    rol_id: int = Field(foreign_key="roles.id", primary_key=True, index=True)


class Rol(SQLModel, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    descripcion: str | None = Field(default=None, max_length=255)

    usuarios: list["Usuario"] = Relationship(back_populates="roles", link_model=UsuarioRol)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

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