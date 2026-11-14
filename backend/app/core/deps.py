from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.models.enums import RolNombre
from app.schemas.usuario import UsuarioPublic
from app.services.usuario_service import a_usuario_public


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:  # type: ignore[override]
        token = request.cookies.get("access_token")
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No autenticado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UsuarioPublic:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or payload.get("sub") is None:
        raise credenciales_invalidas
    with UnitOfWork() as uow:
        usuario = uow.usuarios.obtener_por_email(payload["sub"])
        if usuario is None:
            raise credenciales_invalidas
        return a_usuario_public(usuario)


def get_current_active_user(
    current_user: Annotated[UsuarioPublic, Depends(get_current_user)],
) -> UsuarioPublic:
    if not current_user.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cuenta de usuario desactivada")
    return current_user


def require_role(allowed_roles: list[RolNombre]):
    def role_checker(
        current_user: Annotated[UsuarioPublic, Depends(get_current_active_user)],
    ) -> UsuarioPublic:
        permitidos = {rol.value for rol in allowed_roles}
        if permitidos.isdisjoint(current_user.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de: {sorted(permitidos)}",
            )
        return current_user

    return role_checker


# Alias para usar en los routers
UsuarioActual = Annotated[UsuarioPublic, Depends(get_current_active_user)]
SoloAdmin = Annotated[UsuarioPublic, Depends(require_role([RolNombre.ADMINISTRADOR]))]


# Combinaciones de roles que usan los routers
GestorAnimales = Annotated[UsuarioPublic, Depends(require_role([RolNombre.RESCATISTA, RolNombre.ADMINISTRADOR]))]
Rescatista = Annotated[UsuarioPublic, Depends(require_role([RolNombre.RESCATISTA]))]
GestorSalud = Annotated[
    UsuarioPublic,
    Depends(require_role([RolNombre.RESCATISTA, RolNombre.HOGAR_TRANSITO, RolNombre.ADMINISTRADOR])),
]
ResponsableHogar = Annotated[UsuarioPublic, Depends(require_role([RolNombre.HOGAR_TRANSITO]))]


Adoptante = Annotated[UsuarioPublic, Depends(require_role([RolNombre.ADOPTANTE]))]