from datetime import date

from app.core.errors import NoEncontrado, ReglaDeNegocio
from app.core.uow import UnitOfWork
from app.models import RegistroSanitario
from app.schemas.registro_sanitario import (
    RegistroSanitarioCreate,
    RegistroSanitarioRead,
    RegistroSanitarioUpdate,
)


class RegistroSanitarioService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _verificar_animal(self, animal_id: int) -> None:
        if self.uow.animales.obtener_por_id(animal_id) is None:
            raise NoEncontrado("Animal no encontrado")

    @staticmethod
    def _verificar_fecha(fecha: date | None) -> None:
        """Un registro sanitario documenta algo que ya ocurrió: no puede tener fecha futura."""
        if fecha is not None and fecha > date.today():
            raise ReglaDeNegocio("La fecha no puede ser futura")

    def _obtener_o_error(self, registro_id: int) -> RegistroSanitario:
        registro = self.uow.registros_sanitarios.obtener_por_id(registro_id)
        if registro is None:
            raise NoEncontrado("Registro sanitario no encontrado")
        return registro

    def listar_historial(self, animal_id: int) -> list[RegistroSanitarioRead]:
        with self.uow:
            self._verificar_animal(animal_id)
            registros = self.uow.registros_sanitarios.listar_por_animal(animal_id)
            return [RegistroSanitarioRead.model_validate(r) for r in registros]

    def crear(self, animal_id: int, datos: RegistroSanitarioCreate) -> RegistroSanitarioRead:
        self._verificar_fecha(datos.fecha)  # se valida antes de abrir la transacción
        with self.uow:
            self._verificar_animal(animal_id)
            registro = RegistroSanitario(animal_id=animal_id, **datos.model_dump())
            return RegistroSanitarioRead.model_validate(self.uow.registros_sanitarios.agregar(registro))

    def actualizar(self, registro_id: int, datos: RegistroSanitarioUpdate) -> RegistroSanitarioRead:
        self._verificar_fecha(datos.fecha)
        with self.uow:
            registro = self._obtener_o_error(registro_id)
            registro.sqlmodel_update(datos.model_dump(exclude_unset=True))
            return RegistroSanitarioRead.model_validate(self.uow.registros_sanitarios.agregar(registro))

    def eliminar(self, registro_id: int) -> None:
        """Borrado físico: se usa para corregir un registro cargado por error."""
        with self.uow:
            self.uow.registros_sanitarios.eliminar(self._obtener_o_error(registro_id))
