from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.deps import SoloAdmin, UsuarioActual
from app.core.uow import UnitOfWork
from app.schemas.usuario import LoginRespuesta, UsuarioCreate, UsuarioPublic
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/api/v1", tags=["Autenticación y usuarios"])


def get_usuario_service() -> UsuarioService:
    return UsuarioService(UnitOfWork())


Servicio = Annotated[UsuarioService, Depends(get_usuario_service)]


@router.post("/auth/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def registrar(datos: UsuarioCreate, service: Servicio):
    """Registro público. El rol ADMINISTRADOR no se puede elegir."""
    return service.registrar(datos)


@router.post("/auth/token", response_model=LoginRespuesta)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, service: Servicio):
    """Login con formulario OAuth2: en 'username' va el email. El token viaja en una cookie HttpOnly."""
    token, usuario = service.autenticar(form_data.username, form_data.password)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        samesite=settings.cookie_samesite,
        secure=settings.cookie_secure,
    )
    return LoginRespuesta(mensaje="Login exitoso", usuario=usuario)


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(
        "access_token",
        httponly=True,
        samesite=settings.cookie_samesite,
        secure=settings.cookie_secure,
    )
    return {"mensaje": "Sesión cerrada"}


@router.get("/auth/me", response_model=UsuarioPublic)
def perfil(usuario: UsuarioActual):
    return usuario


@router.get("/admin/usuarios", response_model=list[UsuarioPublic])
def listar_usuarios(_admin: SoloAdmin, service: Servicio):
    return service.listar()


@router.post("/admin/usuarios/{usuario_id}/activar", response_model=UsuarioPublic)
def activar_usuario(usuario_id: int, admin: SoloAdmin, service: Servicio):
    return service.cambiar_estado(usuario_id, activo=True, admin_id=admin.id)


@router.post("/admin/usuarios/{usuario_id}/desactivar", response_model=UsuarioPublic)
def desactivar_usuario(usuario_id: int, admin: SoloAdmin, service: Servicio):
    return service.cambiar_estado(usuario_id, activo=False, admin_id=admin.id)
