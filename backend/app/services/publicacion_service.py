from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio, SinPermiso
from app.core.uow import UnitOfWork
from app.models import Publicacion
from app.models.enums import EstadoAnimal, EstadoPublicacion, RolNombre
from app.schemas.publicacion import PublicacionCreate, PublicacionRead, PublicacionUpdate
from app.schemas.usuario import UsuarioPublic


class PublicacionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _obtener_o_error(self, publicacion_id: int) -> Publicacion:
        publicacion = self.uow.publicaciones.obtener_por_id(publicacion_id)
        if publicacion is None:
            raise NoEncontrado("Publicación no encontrada")
        return publicacion

    def listar(self, estado: EstadoPublicacion | None = None) -> list[PublicacionRead]:
        with self.uow:
            return [PublicacionRead.model_validate(p) for p in self.uow.publicaciones.listar(estado)]

    def obtener(self, publicacion_id: int) -> PublicacionRead:
        with self.uow:
            return PublicacionRead.model_validate(self._obtener_o_error(publicacion_id))

    def crear(self, datos: PublicacionCreate, autor: UsuarioPublic) -> PublicacionRead:
        with self.uow:
            animal = self.uow.animales.obtener_por_id(datos.animal_id)
            if animal is None:
                raise NoEncontrado("Animal no encontrado")
            if animal.estado not in (EstadoAnimal.DISPONIBLE, EstadoAnimal.EN_TRANSITO):
                raise ReglaDeNegocio("Solo se pueden publicar animales disponibles o en tránsito")
            if self.uow.publicaciones.obtener_vigente_de_animal(datos.animal_id) is not None:
                raise Conflicto("El animal ya tiene una publicación vigente")
            publicacion = Publicacion(autor_id=autor.id, **datos.model_dump())
            return PublicacionRead.model_validate(self.uow.publicaciones.agregar(publicacion))

    def actualizar(self, publicacion_id: int, datos: PublicacionUpdate, usuario: UsuarioPublic) -> PublicacionRead:
        with self.uow:
            publicacion = self._obtener_o_error(publicacion_id)
            if publicacion.autor_id != usuario.id and not usuario.tiene_rol(RolNombre.ADMINISTRADOR):
                raise SinPermiso("Solo el autor de la publicación puede modificarla")
            if publicacion.estado == EstadoPublicacion.FINALIZADA:
                raise Conflicto("La publicación ya está finalizada")
            publicacion.sqlmodel_update(datos.model_dump(exclude_unset=True))
            return PublicacionRead.model_validate(self.uow.publicaciones.agregar(publicacion))