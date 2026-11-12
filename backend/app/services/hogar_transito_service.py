from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
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


class HogarTransitoService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    # --- Funciones auxiliares ---

    def _obtener_hogar_o_error(self, hogar_id: int) -> HogarTransito:
        hogar = self.uow.hogares.obtener_por_id(hogar_id)
        if hogar is None:
            raise NoEncontrado("Hogar de tránsito no encontrado")
        return hogar

    def _verificar_responsable(self, usuario_id: int) -> None:
        """El responsable tiene que existir y tener el rol HOGAR_TRANSITO."""
        usuario = self.uow.usuarios.obtener_por_id(usuario_id)
        if usuario is None:
            raise NoEncontrado("Responsable no encontrado")
        if RolNombre.HOGAR_TRANSITO not in [rol.nombre for rol in usuario.roles]:
            raise ReglaDeNegocio("El usuario no tiene el rol HOGAR_TRANSITO")

    # --- Hogares ---

    def listar(self, disponible: bool | None = None) -> list[HogarTransitoRead]:
        with self.uow:
            return [HogarTransitoRead.model_validate(h) for h in self.uow.hogares.listar(disponible)]

    def obtener(self, hogar_id: int) -> HogarTransitoRead:
        with self.uow:
            return HogarTransitoRead.model_validate(self._obtener_hogar_o_error(hogar_id))

    def crear(self, datos: HogarTransitoCreate) -> HogarTransitoRead:
        with self.uow:
            self._verificar_responsable(datos.responsable_id)
            hogar = self.uow.hogares.agregar(HogarTransito(**datos.model_dump()))
            return HogarTransitoRead.model_validate(hogar)

    def actualizar(self, hogar_id: int, datos: HogarTransitoUpdate) -> HogarTransitoRead:
        with self.uow:
            hogar = self._obtener_hogar_o_error(hogar_id)
            cambios = datos.model_dump(exclude_unset=True)
            if "capacidad" in cambios:
                ocupados = self.uow.asignaciones.contar_activas(hogar_id)
                if cambios["capacidad"] < ocupados:
                    raise ReglaDeNegocio(f"La capacidad no puede ser menor a los {ocupados} animales alojados")
            hogar.sqlmodel_update(cambios)
            return HogarTransitoRead.model_validate(self.uow.hogares.agregar(hogar))

    # --- Asignaciones ---

    def listar_asignaciones(self, hogar_id: int, solo_activas: bool = False) -> list[AsignacionRead]:
        with self.uow:
            self._obtener_hogar_o_error(hogar_id)
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

    def registrar_egreso(self, asignacion_id: int, datos: AsignacionEgreso) -> AsignacionRead:
        with self.uow:
            asignacion = self.uow.asignaciones.obtener_por_id(asignacion_id)
            if asignacion is None:
                raise NoEncontrado("Asignación no encontrada")
            if asignacion.fecha_salida is not None:
                raise Conflicto("La asignación ya fue finalizada")
            if datos.fecha_salida < asignacion.fecha_ingreso:
                raise ReglaDeNegocio("La fecha de salida no puede ser anterior al ingreso")

            asignacion.fecha_salida = datos.fecha_salida
            if datos.observaciones is not None:
                asignacion.observaciones = datos.observaciones
            self.uow.asignaciones.agregar(asignacion)

            # Si el animal seguía EN_TRANSITO, vuelve a estar DISPONIBLE (misma transacción)
            animal = self.uow.animales.obtener_por_id(asignacion.animal_id)
            if animal is not None and animal.estado == EstadoAnimal.EN_TRANSITO:
                animal.estado = EstadoAnimal.DISPONIBLE
                self.uow.animales.agregar(animal)

            return AsignacionRead.model_validate(asignacion)
