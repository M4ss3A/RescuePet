from datetime import date

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio, SinPermiso
from app.core.uow import UnitOfWork
from app.models import Adopcion, SolicitudAdopcion
from app.models.enums import (
    EstadoAdopcion,
    EstadoAnimal,
    EstadoPublicacion,
    EstadoSolicitud,
    RolNombre,
    Tamano,
)
from app.schemas.adopcion import AdopcionRead
from app.schemas.solicitud import AprobacionDatos, SolicitudCreate, SolicitudRead
from app.schemas.usuario import UsuarioPublic
from app.services.compatibilidad import calcular_puntaje


class SolicitudService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    # Funciones auxiliares 

    @staticmethod
    def _a_respuesta(solicitud: SolicitudAdopcion) -> SolicitudRead:
        return SolicitudRead(**solicitud.model_dump(warnings=False), animal_id=solicitud.publicacion.animal_id)

    def _obtener_o_error(self, solicitud_id: int) -> SolicitudAdopcion:
        solicitud = self.uow.solicitudes.obtener_por_id(solicitud_id)
        if solicitud is None:
            raise NoEncontrado("Solicitud no encontrada")
        return solicitud

    @staticmethod
    def _verificar_autor_o_admin(solicitud: SolicitudAdopcion, usuario: UsuarioPublic) -> None:
        if solicitud.publicacion.autor_id != usuario.id and not usuario.tiene_rol(RolNombre.ADMINISTRADOR):
            raise SinPermiso("Solo el autor de la publicación puede gestionar esta solicitud")

    @staticmethod
    def _verificar_pendiente(solicitud: SolicitudAdopcion) -> None:
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            raise Conflicto(f"La solicitud ya está {EstadoSolicitud(solicitud.estado).value}")

    # Casos de uso 

    def crear(self, datos: SolicitudCreate, adoptante: UsuarioPublic) -> SolicitudRead:
        with self.uow:
            animal = self.uow.animales.obtener_por_id(datos.animal_id)
            if animal is None:
                raise NoEncontrado("Animal no encontrado")
            publicacion = self.uow.publicaciones.obtener_vigente_de_animal(datos.animal_id)
            if publicacion is None or publicacion.estado != EstadoPublicacion.ACTIVA:
                raise ReglaDeNegocio("El animal no está publicado para adopción")
            if publicacion.autor_id == adoptante.id:
                raise ReglaDeNegocio("No podés solicitar la adopción de un animal que publicaste")
            if self.uow.solicitudes.obtener_de_adoptante(publicacion.id, adoptante.id) is not None:  # type: ignore[arg-type]
                raise Conflicto("Ya enviaste una solicitud para este animal")

            puntaje = calcular_puntaje(
                tamano=Tamano(animal.tamano) if animal.tamano else None,
                tipo_vivienda=datos.tipo_vivienda,
                tiene_patio=datos.tiene_patio,
                experiencia_previa=datos.experiencia_previa,
                tiene_otros_animales=datos.tiene_otros_animales,
                motivo=datos.motivo,
            )
            solicitud = SolicitudAdopcion(
                publicacion_id=publicacion.id,  # type: ignore[arg-type]
                adoptante_id=adoptante.id,
                puntaje_compatibilidad=puntaje,
                **datos.model_dump(exclude={"animal_id"}),
            )
            return self._a_respuesta(self.uow.solicitudes.agregar(solicitud))

    def listar_mias(self, adoptante: UsuarioPublic) -> list[SolicitudRead]:
        with self.uow:
            return [self._a_respuesta(s) for s in self.uow.solicitudes.listar(adoptante_id=adoptante.id)]

    def listar_recibidas(self, usuario: UsuarioPublic, estado: EstadoSolicitud | None = None) -> list[SolicitudRead]:
        with self.uow:
            autor_id = None if usuario.tiene_rol(RolNombre.ADMINISTRADOR) else usuario.id
            solicitudes = self.uow.solicitudes.listar(estado=estado, autor_publicacion_id=autor_id)
            return [self._a_respuesta(s) for s in solicitudes]

    def obtener(self, solicitud_id: int, usuario: UsuarioPublic) -> SolicitudRead:
        with self.uow:
            solicitud = self._obtener_o_error(solicitud_id)
            if solicitud.adoptante_id != usuario.id:
                self._verificar_autor_o_admin(solicitud, usuario)
            return self._a_respuesta(solicitud)

    def cancelar(self, solicitud_id: int, adoptante: UsuarioPublic) -> SolicitudRead:
        with self.uow:
            solicitud = self._obtener_o_error(solicitud_id)
            if solicitud.adoptante_id != adoptante.id:
                raise SinPermiso("Solo el adoptante que envió la solicitud puede cancelarla")
            self._verificar_pendiente(solicitud)
            solicitud.estado = EstadoSolicitud.CANCELADA
            return self._a_respuesta(self.uow.solicitudes.agregar(solicitud))

    def rechazar(self, solicitud_id: int, usuario: UsuarioPublic) -> SolicitudRead:
        with self.uow:
            solicitud = self._obtener_o_error(solicitud_id)
            self._verificar_autor_o_admin(solicitud, usuario)
            self._verificar_pendiente(solicitud)
            solicitud.estado = EstadoSolicitud.RECHAZADA
            return self._a_respuesta(self.uow.solicitudes.agregar(solicitud))

    def aprobar(self, solicitud_id: int, datos: AprobacionDatos, usuario: UsuarioPublic) -> AdopcionRead:
        """Caso de uso central: todo ocurre en UNA transaccion. Si algo falla, el Unit of Work
        deshace todos los cambios y no queda una adopción a medias."""
        fecha = datos.fecha_adopcion or date.today()
        if fecha > date.today():
            raise ReglaDeNegocio("La fecha de adopción no puede ser futura")

        with self.uow:
            solicitud = self._obtener_o_error(solicitud_id)
            self._verificar_autor_o_admin(solicitud, usuario)
            self._verificar_pendiente(solicitud)
            publicacion = solicitud.publicacion
            animal = self.uow.animales.obtener_por_id(publicacion.animal_id)
            if animal is None:
                raise NoEncontrado("Animal no encontrado")

            # La solicitud queda aprobada
            solicitud.estado = EstadoSolicitud.APROBADA
            self.uow.solicitudes.agregar(solicitud)

            # Se crea la adopcion
            adopcion = self.uow.adopciones.agregar(
                Adopcion(
                    solicitud_id=solicitud_id,
                    fecha_adopcion=fecha,
                    estado=EstadoAdopcion.EN_SEGUIMIENTO,
                    observaciones=datos.observaciones,
                )
            )

            # El animal pasa a ADOPTADO
            animal.estado = EstadoAnimal.ADOPTADO
            self.uow.animales.agregar(animal)

            # La publicacion se finaliza
            publicacion.estado = EstadoPublicacion.FINALIZADA
            self.uow.publicaciones.agregar(publicacion)

            # Las demas solicitudes pendientes de la publicación se rechazan
            for otra in self.uow.solicitudes.listar_pendientes_de_publicacion(publicacion.id):  # type: ignore[arg-type]
                otra.estado = EstadoSolicitud.RECHAZADA
                self.uow.solicitudes.agregar(otra)

            # Si el animal estaba en un hogar de transito, se registra su salida
            asignacion = self.uow.asignaciones.obtener_activa_de_animal(animal.id)  # type: ignore[arg-type]
            if asignacion is not None:
                asignacion.fecha_salida = max(fecha, asignacion.fecha_ingreso)
                self.uow.asignaciones.agregar(asignacion)

            return AdopcionRead(
                **adopcion.model_dump(warnings=False), animal_id=animal.id, adoptante_id=solicitud.adoptante_id  # type: ignore[arg-type]
            )