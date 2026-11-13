from app.core.base_repository import BaseRepository
from app.models import Usuario, Rol
from sqlmodel import col, select


class UsuarioRepository(BaseRepository[Usuario]):
    modelo = Usuario

    
    def obtener_por_email(self, email: str) -> Usuario | None:
        consulta = select(Usuario).where(col(Usuario.email) == email)
        return self.session.exec(consulta).first()

    def listar(self) -> list[Usuario]:
        return list(self.session.exec(select(Usuario).order_by(col(Usuario.id))).all())


class RolRepository(BaseRepository[Rol]):
    modelo = Rol

    def obtener_por_nombre(self, nombre: str) -> Rol | None:
        return self.session.exec(select(Rol).where(col(Rol.nombre) == nombre)).first()