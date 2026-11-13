from app.core.errors import Conflicto, NoEncontrado, SinPermiso
from app.core.uow import UnitOfWork
from app.models import Rescate
from app.models.enums import RolNombre
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate
from app.schemas.usuario import UsuarioPublic


class RescateService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _verificar_animal(self, animal_id: int) -> None:
        if self.uow.animales.obtener_por_id(animal_id) is None:
            raise NoEncontrado("Animal no encontrado")

    def _obtener_o_error(self, animal_id: int) -> Rescate:
        self._verificar_animal(animal_id)
        rescate = self.uow.rescates.obtener_por_animal(animal_id)
        if rescate is None:
            raise NoEncontrado("El animal no tiene un rescate registrado")
        return rescate

    def obtener(self, animal_id: int) -> RescateRead:
        with self.uow:
            return RescateRead.model_validate(self._obtener_o_error(animal_id))

    def registrar(self, animal_id: int, datos: RescateCreate, rescatista: UsuarioPublic) -> RescateRead:
        """El rescatista es el usuario logueado (el router ya verificó que tenga el rol RESCATISTA)."""
        with self.uow:
            self._verificar_animal(animal_id)
            if self.uow.rescates.obtener_por_animal(animal_id) is not None:
                raise Conflicto("El animal ya tiene un rescate registrado")
            rescate = Rescate(animal_id=animal_id, rescatista_id=rescatista.id, **datos.model_dump())
            return RescateRead.model_validate(self.uow.rescates.agregar(rescate))

    def actualizar(self, animal_id: int, datos: RescateUpdate, usuario: UsuarioPublic) -> RescateRead:
        """Solo puede corregirlo el rescatista que lo registró o un administrador."""
        with self.uow:
            rescate = self._obtener_o_error(animal_id)
            if rescate.rescatista_id != usuario.id and not usuario.tiene_rol(RolNombre.ADMINISTRADOR):
                raise SinPermiso("Solo el rescatista que registró el rescate puede modificarlo")
            rescate.sqlmodel_update(datos.model_dump(exclude_unset=True))
            return RescateRead.model_validate(self.uow.rescates.agregar(rescate))
