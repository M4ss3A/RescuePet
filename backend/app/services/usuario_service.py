from app.core.errors import Conflicto, NoAutenticado, NoEncontrado, ReglaDeNegocio
from app.core.security import create_access_token, hash_password, verify_password
from app.core.uow import UnitOfWork
from app.models import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioPublic


def a_usuario_public(usuario: Usuario) -> UsuarioPublic:
    """Arma la vista pública con los nombres de los roles (se llama dentro de un bloque `with`)."""
    datos = usuario.model_dump(exclude={"contrasena_hash"})
    return UsuarioPublic(**datos, roles=[rol.nombre for rol in usuario.roles])


class UsuarioService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def registrar(self, datos: UsuarioCreate) -> UsuarioPublic:
        with self.uow:
            if self.uow.usuarios.obtener_por_email(datos.email) is not None:
                raise Conflicto("Ya existe un usuario con ese email")
            rol = self.uow.roles.obtener_por_nombre(datos.rol.value)
            if rol is None:
                raise ReglaDeNegocio("Rol inexistente")
            usuario = Usuario(
                **datos.model_dump(exclude={"password", "rol"}),
                contrasena_hash=hash_password(datos.password),
                roles=[rol],
            )
            return a_usuario_public(self.uow.usuarios.agregar(usuario))

    def autenticar(self, email: str, password: str) -> tuple[str, UsuarioPublic]:
        """Devuelve el token y el usuario. El mismo mensaje para email o contraseña incorrectos,
        así la respuesta no revela cuál de los dos falló."""
        with self.uow:
            usuario = self.uow.usuarios.obtener_por_email(email)
            if usuario is None or not verify_password(password, usuario.contrasena_hash):
                raise NoAutenticado("Credenciales incorrectas")
            if not usuario.activo:
                raise ReglaDeNegocio("Cuenta de usuario desactivada")
            token = create_access_token({"sub": usuario.email, "roles": [r.nombre for r in usuario.roles]})
            return token, a_usuario_public(usuario)

    def listar(self) -> list[UsuarioPublic]:
        with self.uow:
            return [a_usuario_public(u) for u in self.uow.usuarios.listar()]

    def cambiar_estado(self, usuario_id: int, activo: bool, admin_id: int) -> UsuarioPublic:
        """Activa o desactiva una cuenta (baja lógica). Es idempotente."""
        if not activo and usuario_id == admin_id:
            raise ReglaDeNegocio("Un administrador no puede desactivar su propia cuenta")
        with self.uow:
            usuario = self.uow.usuarios.obtener_por_id(usuario_id)
            if usuario is None:
                raise NoEncontrado("Usuario no encontrado")
            usuario.activo = activo
            return a_usuario_public(self.uow.usuarios.agregar(usuario))
