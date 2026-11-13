from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import engine
from app.core.security import hash_password
from app.models import Rol, Usuario
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



def cargar_admin() -> None:
    """Crea el administrador inicial con los datos del .env (ADMIN_EMAIL y ADMIN_PASSWORD), si no existe.
    La contraseña no está en el código: se lee del entorno."""
    if not settings.admin_email or not settings.admin_password:
        return
    with Session(engine) as session:
        if session.exec(select(Usuario).where(Usuario.email == settings.admin_email)).first():
            return
        rol_admin = session.exec(select(Rol).where(Rol.nombre == RolNombre.ADMINISTRADOR.value)).one()
        session.add(
            Usuario(
                nombre="Administrador",
                apellido="RescuePet",
                email=settings.admin_email,
                contrasena_hash=hash_password(settings.admin_password),
                roles=[rol_admin],
            )
        )
        session.commit()