from datetime import datetime

from pydantic import EmailStr, Field, field_validator

from app.models.enums import RolNombre
from app.schemas.base import CamelModel


ROLES_REGISTRABLES = {RolNombre.ADOPTANTE, RolNombre.RESCATISTA, RolNombre.HOGAR_TRANSITO}


class UsuarioCreate(CamelModel):
    """Datos del registro público. La contraseña llega en texto plano y el service guarda su hash."""

    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=150)
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=30)
    direccion: str | None = Field(default=None, max_length=255)
    rol: RolNombre = RolNombre.ADOPTANTE

    @field_validator("password")
    @classmethod
    def validar_largo_en_bytes(cls, password: str) -> str:
        # bcrypt procesa solo los primeros 72 bytes (las tildes ocupan más de 1 byte)
        if len(password.encode("utf-8")) > 72:
            raise ValueError("La contraseña no puede superar los 72 bytes")
        return password

    @field_validator("rol")
    @classmethod
    def validar_rol(cls, rol: RolNombre) -> RolNombre:
        if rol not in ROLES_REGISTRABLES:
            raise ValueError("No se puede registrar un usuario con ese rol")
        return rol


class UsuarioPublic(CamelModel):
    """Vista pública del usuario: nunca incluye la contraseña ni su hash."""

    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None
    direccion: str | None
    activo: bool
    fecha_registro: datetime
    roles: list[str]
    
    def tiene_rol(self, rol: RolNombre) -> bool:
        return rol.value in self.roles


class LoginRespuesta(CamelModel):
    mensaje: str
    usuario: UsuarioPublic
