from fastapi import HTTPException, status
from sqlmodel import Session

from app.models import AsignacionTransito, HogarTransito
from app.models.enums import EstadoAnimal, RolNombre
from app.repositories import animal_repository, hogar_transito_repository, usuario_repository
from app.schemas.hogar_transito import (
    AsignacionCreate,
    AsignacionEgreso,
    AsignacionRead,
    HogarTransitoCreate,
    HogarTransitoRead,
    HogarTransitoUpdate,
)

# --- Hogares ---


def _obtener_hogar_o_404(session: Session, hogar_id: int) -> HogarTransito:
    hogar = hogar_transito_repository.obtener_por_id(session, hogar_id)
    if hogar is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hogar de tránsito no encontrado")
    return hogar


def _verificar_responsable(session: Session, usuario_id: int) -> None:
    """El responsable tiene que existir y tener el rol HOGAR_TRANSITO."""
    usuario = usuario_repository.obtener_por_id(session, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsable no encontrado")
    if RolNombre.HOGAR_TRANSITO not in [rol.nombre for rol in usuario.roles]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no tiene el rol HOGAR_TRANSITO"
        )


def listar_hogares(session: Session, disponible: bool | None = None) -> list[HogarTransitoRead]:
    hogares = hogar_transito_repository.listar(session, disponible)
    return [HogarTransitoRead.model_validate(h) for h in hogares]


def obtener_hogar(session: Session, hogar_id: int) -> HogarTransitoRead:
    return HogarTransitoRead.model_validate(_obtener_hogar_o_404(session, hogar_id))


def crear_hogar(session: Session, datos: HogarTransitoCreate) -> HogarTransitoRead:
    _verificar_responsable(session, datos.responsable_id)
    hogar = HogarTransito(**datos.model_dump())
    return HogarTransitoRead.model_validate(hogar_transito_repository.guardar(session, hogar))


def actualizar_hogar(session: Session, hogar_id: int, datos: HogarTransitoUpdate) -> HogarTransitoRead:
    hogar = _obtener_hogar_o_404(session, hogar_id)
    cambios = datos.model_dump(exclude_unset=True)
    if "capacidad" in cambios:
        ocupados = len(hogar_transito_repository.listar_asignaciones(session, hogar_id, solo_activas=True))
        if cambios["capacidad"] < ocupados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La capacidad no puede ser menor a los {ocupados} animales alojados",
            )
    hogar.sqlmodel_update(cambios)
    return HogarTransitoRead.model_validate(hogar_transito_repository.guardar(session, hogar))


# --- Asignaciones ---


def listar_asignaciones(session: Session, hogar_id: int, solo_activas: bool = False) -> list[AsignacionRead]:
    _obtener_hogar_o_404(session, hogar_id)
    asignaciones = hogar_transito_repository.listar_asignaciones(session, hogar_id, solo_activas)
    return [AsignacionRead.model_validate(a) for a in asignaciones]


def asignar_animal(session: Session, hogar_id: int, datos: AsignacionCreate) -> AsignacionRead:
    hogar = _obtener_hogar_o_404(session, hogar_id)
    if not hogar.disponible:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El hogar no está disponible")

    ocupados = len(hogar_transito_repository.listar_asignaciones(session, hogar_id, solo_activas=True))
    if ocupados >= hogar.capacidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El hogar no tiene lugar disponible")

    animal = animal_repository.obtener_por_id(session, datos.animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")
    if animal.estado in (EstadoAnimal.ADOPTADO, EstadoAnimal.INACTIVO):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"No se puede asignar un animal {animal.estado.value}"
        )
    if hogar_transito_repository.obtener_asignacion_activa_de_animal(session, datos.animal_id) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El animal ya está en un hogar de tránsito")

    # El animal pasa a EN_TRANSITO y se guarda junto con la asignación en un mismo commit
    animal.estado = EstadoAnimal.EN_TRANSITO
    session.add(animal)
    asignacion = AsignacionTransito(hogar_transito_id=hogar_id, **datos.model_dump())
    return AsignacionRead.model_validate(hogar_transito_repository.guardar_asignacion(session, asignacion))


def registrar_egreso(session: Session, asignacion_id: int, datos: AsignacionEgreso) -> AsignacionRead:
    asignacion = hogar_transito_repository.obtener_asignacion(session, asignacion_id)
    if asignacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación no encontrada")
    if asignacion.fecha_salida is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La asignación ya fue finalizada")
    if datos.fecha_salida < asignacion.fecha_ingreso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de salida no puede ser anterior al ingreso"
        )

    asignacion.fecha_salida = datos.fecha_salida
    if datos.observaciones is not None:
        asignacion.observaciones = datos.observaciones

    # Si el animal seguía EN_TRANSITO, vuelve a estar DISPONIBLE
    animal = animal_repository.obtener_por_id(session, asignacion.animal_id)
    if animal is not None and animal.estado == EstadoAnimal.EN_TRANSITO:
        animal.estado = EstadoAnimal.DISPONIBLE
        session.add(animal)

    return AsignacionRead.model_validate(hogar_transito_repository.guardar_asignacion(session, asignacion))
