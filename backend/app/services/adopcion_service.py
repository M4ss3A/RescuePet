from datetime import date

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio, SinPermiso
from app.core.uow import UnitOfWork
from app.models import Adopcion, Seguimiento
from app.models.enums import EstadoAdopcion, RolNombre
from app.schemas.adopcion import AdopcionRead, AdopcionUpdate, SeguimientoCreate, SeguimientoRead
from app.schemas.usuario import UsuarioPublic


class AdopcionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    # Funciones auxiliares 

    @staticmethod
    def _a_respuesta(adopcion: Adopcion) -> AdopcionRead:
        solicitud = adopcion.solicitud
        return AdopcionRead(
            **adopcion.model_dump(warnings=False),
            animal_id=solicitud.publicacion.animal_id,
            adoptante_id=solicitud.adoptante_id,
        )

    def _obtener_o_error(self, adopcion_id: int) -> Adopcion:
        adopcion = self.uow.adopciones.obtener_por_id(adopcion_id)
        if adopcion is None:
            raise NoEncontrado("Adopción no encontrada")
        return adopcion

    @staticmethod
    def _es_responsable(adopcion: Adopcion, usuario: UsuarioPublic) -> bool:
        return adopcion.solicitud.publicacion.autor_id == usuario.id or usuario.tiene_rol(RolNombre.ADMINISTRADOR)

    def _verificar_responsable(self, adopcion: Adopcion, usuario: UsuarioPublic) -> None:
        if not self._es_responsable(adopcion, usuario):
            raise SinPermiso("Solo el responsable de la adopción puede realizar esta acción")

    def _verificar_acceso(self, adopcion: Adopcion, usuario: UsuarioPublic) -> None:
        if adopcion.solicitud.adoptante_id != usuario.id:
            self._verificar_responsable(adopcion, usuario)

    # Adopciones 

    def listar(self, usuario: UsuarioPublic, solicitud_id: int | None = None) -> list[AdopcionRead]:
        with self.uow:
            usuario_id = None if usuario.tiene_rol(RolNombre.ADMINISTRADOR) else usuario.id
            adopciones = self.uow.adopciones.listar(solicitud_id=solicitud_id, usuario_id=usuario_id)
            return [self._a_respuesta(a) for a in adopciones]

    def obtener(self, adopcion_id: int, usuario: UsuarioPublic) -> AdopcionRead:
        with self.uow:
            adopcion = self._obtener_o_error(adopcion_id)
            self._verificar_acceso(adopcion, usuario)
            return self._a_respuesta(adopcion)

    def actualizar(self, adopcion_id: int, datos: AdopcionUpdate, usuario: UsuarioPublic) -> AdopcionRead:
        with self.uow:
            adopcion = self._obtener_o_error(adopcion_id)
            self._verificar_responsable(adopcion, usuario)
            adopcion.sqlmodel_update(datos.model_dump(exclude_unset=True))
            return self._a_respuesta(self.uow.adopciones.agregar(adopcion))

    # Seguimientos 

    def listar_seguimientos(self, adopcion_id: int, usuario: UsuarioPublic) -> list[SeguimientoRead]:
        with self.uow:
            adopcion = self._obtener_o_error(adopcion_id)
            self._verificar_acceso(adopcion, usuario)
            return [SeguimientoRead.model_validate(s) for s in self.uow.seguimientos.listar_por_adopcion(adopcion_id)]

    def crear_seguimiento(
        self, adopcion_id: int, datos: SeguimientoCreate, usuario: UsuarioPublic
    ) -> SeguimientoRead:
        with self.uow:
            adopcion = self._obtener_o_error(adopcion_id)
            self._verificar_responsable(adopcion, usuario)
            if adopcion.estado == EstadoAdopcion.FINALIZADA:
                raise Conflicto("El seguimiento de esta adopción ya fue cerrado")
            if datos.fecha > date.today():
                raise ReglaDeNegocio("La fecha no puede ser futura")
            if datos.fecha < adopcion.fecha_adopcion:
                raise ReglaDeNegocio("La fecha no puede ser anterior a la adopción")
            seguimiento = Seguimiento(adopcion_id=adopcion_id, **datos.model_dump())
            return SeguimientoRead.model_validate(self.uow.seguimientos.agregar(seguimiento))