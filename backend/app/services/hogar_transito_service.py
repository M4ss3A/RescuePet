from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio, SinPermiso
from app.core.uow import UnitOfWork
from app.models import AsignacionTransito, HogarTransito
from app.models.enums import EstadoAnimal, RolNombre
from app.schemas.hogar_transito import (
    AsignacionCreate,
    AsignacionEgreso,
    AsignacionRead,
    HogarTransitoCreate,
    HogarTransitoRead,
    HogarTransitoUpdate,
)
from app.schemas.usuario import UsuarioPublic


class HogarTransitoService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    #Funciones auxiliares 

    def _obtener_hogar_o_error(self, hogar_id: int) -> HogarTransito:
        hogar = self.uow.hogares.obtener_por_id(hogar_id)
        if hogar is None:
            raise NoEncontrado("Hogar de tránsito no encontrado")
        return hogar

    @staticmethod
    def _verificar_dueno_o_admin(hogar: HogarTransito, usuario: UsuarioPublic) -> None:
        """Solo el responsable del hogar o un administrador pueden gestionarlo."""
        if hogar.responsable_id != usuario.id and not usuario.tiene_rol(RolNombre.ADMINISTRADOR):
            raise SinPermiso("Solo el responsable del hogar puede realizar esta acción")

    #Hogares 

    def listar(self, disponible: bool | None = None) -> list[HogarTransitoRead]:
        with self.uow:
            return [HogarTransitoRead.model_validate(h) for h in self.uow.hogares.listar(disponible)]

    def obtener(self, hogar_id: int) -> HogarTransitoRead:
        with self.uow:
            return HogarTransitoRead.model_validate(self._obtener_hogar_o_error(hogar_id))

    def crear(self, datos: HogarTransitoCreate, responsable: UsuarioPublic) -> HogarTransitoRead:
        """El responsable es el usuario logueado (el router ya verificó el rol HOGAR_TRANSITO)."""
        with self.uow:
            hogar = self.uow.hogares.agregar(HogarTransito(responsable_id=responsable.id, **datos.model_dump()))
            return HogarTransitoRead.model_validate(hogar)

    def actualizar(self, hogar_id: int, datos: HogarTransitoUpdate, usuario: UsuarioPublic) -> HogarTransitoRead:
        with self.uow:
            hogar = self._obtener_hogar_o_error(hogar_id)
            self._verificar_dueno_o_admin(hogar, usuario)
            cambios = datos.model_dump(exclude_unset=True)
            if "capacidad" in cambios:
                ocupados = self.uow.asignaciones.contar_activas(hogar_id)
                if cambios["capacidad"] < ocupados:
                    raise ReglaDeNegocio(f"La capacidad no puede ser menor a los {ocupados} animales alojados")
            hogar.sqlmodel_update(cambios)
            return HogarTransitoRead.model_validate(self.uow.hogares.agregar(hogar))

    #Asignaciones 

    def listar_asignaciones(
        self, hogar_id: int, usuario: UsuarioPublic, solo_activas: bool = False
    ) -> list[AsignacionRead]:
        """Las ven los rescatistas, los administradores y el responsable del hogar."""
        with self.uow:
            hogar = self._obtener_hogar_o_error(hogar_id)
            if not usuario.tiene_rol(RolNombre.RESCATISTA):
                self._verificar_dueno_o_admin(hogar, usuario)
            asignaciones = self.uow.asignaciones.listar_por_hogar(hogar_id, solo_activas)
            return [AsignacionRead.model_validate(a) for a in asignaciones]

    def asignar_animal(self, hogar_id: int, datos: AsignacionCreate) -> AsignacionRead:
        with self.uow:
            hogar = self._obtener_hogar_o_error(hogar_id)
            if not hogar.disponible:
                raise ReglaDeNegocio("El hogar no está disponible")
            if self.uow.asignaciones.contar_activas(hogar_id) >= hogar.capacidad:
                raise ReglaDeNegocio("El hogar no tiene lugar disponible")

            animal = self.uow.animales.obtener_por_id(datos.animal_id)
            if animal is None:
                raise NoEncontrado("Animal no encontrado")
            if animal.estado in (EstadoAnimal.ADOPTADO, EstadoAnimal.INACTIVO):
                raise ReglaDeNegocio(f"No se puede asignar un animal {EstadoAnimal(animal.estado).value}")
            if self.uow.asignaciones.obtener_activa_de_animal(datos.animal_id) is not None:
                raise Conflicto("El animal ya está en un hogar de tránsito")

            # Dos escrituras en la misma transacción: si una falla, el Unit of Work deshace las dos
            animal.estado = EstadoAnimal.EN_TRANSITO
            self.uow.animales.agregar(animal)
            asignacion = self.uow.asignaciones.agregar(
                AsignacionTransito(hogar_transito_id=hogar_id, **datos.model_dump())
            )
            return AsignacionRead.model_validate(asignacion)

    def registrar_egreso(self, asignacion_id: int, datos: AsignacionEgreso, usuario: UsuarioPublic) -> AsignacionRead:
        with self.uow:
            asignacion = self.uow.asignaciones.obtener_por_id(asignacion_id)
            if asignacion is None:
                raise NoEncontrado("Asignación no encontrada")
            if not usuario.tiene_rol(RolNombre.RESCATISTA):
                self._verificar_dueno_o_admin(self._obtener_hogar_o_error(asignacion.hogar_transito_id), usuario)
            if asignacion.fecha_salida is not None:
                raise Conflicto("La asignación ya fue finalizada")
            if datos.fecha_salida < asignacion.fecha_ingreso:
                raise ReglaDeNegocio("La fecha de salida no puede ser anterior al ingreso")

            asignacion.fecha_salida = datos.fecha_salida
            if datos.observaciones is not None:
                asignacion.observaciones = datos.observaciones
            self.uow.asignaciones.agregar(asignacion)

            # Si el animal seguía EN_TRANSITO, vuelve a estar DISPONIBLE
            animal = self.uow.animales.obtener_por_id(asignacion.animal_id)
            if animal is not None and animal.estado == EstadoAnimal.EN_TRANSITO:
                animal.estado = EstadoAnimal.DISPONIBLE
                self.uow.animales.agregar(animal)

            return AsignacionRead.model_validate(asignacion)