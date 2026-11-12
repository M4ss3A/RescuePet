from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
from app.core.uow import UnitOfWork
from app.models import Rescate
from app.models.enums import RolNombre
from app.schemas.rescate import RescateCreate, RescateRead, RescateUpdate


class RescateService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _verificar_animal(self, animal_id: int) -> None:
        if self.uow.animales.obtener_por_id(animal_id) is None:
            raise NoEncontrado("Animal no encontrado")

    def _verificar_rescatista(self, usuario_id: int) -> None:
        """El rescatista tiene que existir y tener el rol RESCATISTA."""
        usuario = self.uow.usuarios.obtener_por_id(usuario_id)
        if usuario is None:
            raise NoEncontrado("Rescatista no encontrado")
        if RolNombre.RESCATISTA not in [rol.nombre for rol in usuario.roles]:
            raise ReglaDeNegocio("El usuario no tiene el rol RESCATISTA")

    def _obtener_o_error(self, animal_id: int) -> Rescate:
        self._verificar_animal(animal_id)
        rescate = self.uow.rescates.obtener_por_animal(animal_id)
        if rescate is None:
            raise NoEncontrado("El animal no tiene un rescate registrado")
        return rescate

    def obtener(self, animal_id: int) -> RescateRead:
        with self.uow:
            return RescateRead.model_validate(self._obtener_o_error(animal_id))

    def registrar(self, animal_id: int, datos: RescateCreate) -> RescateRead:
        with self.uow:
            self._verificar_animal(animal_id)
            if self.uow.rescates.obtener_por_animal(animal_id) is not None:
                raise Conflicto("El animal ya tiene un rescate registrado")
            self._verificar_rescatista(datos.rescatista_id)
            rescate = self.uow.rescates.agregar(Rescate(animal_id=animal_id, **datos.model_dump()))
            return RescateRead.model_validate(rescate)

    def actualizar(self, animal_id: int, datos: RescateUpdate) -> RescateRead:
        with self.uow:
            rescate = self._obtener_o_error(animal_id)
            rescate.sqlmodel_update(datos.model_dump(exclude_unset=True))
            return RescateRead.model_validate(self.uow.rescates.agregar(rescate))
