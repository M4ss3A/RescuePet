from sqlmodel import Session, select

from app.core.database import engine
from app.models import Rol
from app.models.enums import RolNombre


ROLES_INICIALES = {
    RolNombre.ADMINISTRADOR: "Administra usuarios, permisos y configuraciones generales.",
    RolNombre.RESCATISTA: "Representa a un rescatista o protector y gestiona rescates, animales y publicaciones de adopción.",
    RolNombre.HOGAR_TRANSITO: "Informa disponibilidad y aloja animales temporalmente.",
    RolNombre.ADOPTANTE: "Consulta publicaciones y realiza solicitudes de adopción.",
}

def cargar_roles() -> None:
    """Inserta los roles del sistema si todavía no existen."""
    with Session(engine) as session:
        existentes = set(session.exec(select(Rol.nombre)).all())
        for nombre, descripcion in ROLES_INICIALES.items():
            if nombre.value not in existentes:
                session.add(Rol(nombre=nombre.value, descripcion=descripcion))
        session.commit()