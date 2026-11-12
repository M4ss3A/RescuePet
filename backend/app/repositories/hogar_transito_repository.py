from sqlmodel import Session, col, select

from app.models import AsignacionTransito, HogarTransito


def listar(session: Session, disponible: bool | None = None) -> list[HogarTransito]:
    consulta = select(HogarTransito).order_by(col(HogarTransito.id))
    if disponible is not None:
        consulta = consulta.where(col(HogarTransito.disponible) == disponible)
    return list(session.exec(consulta).all())


def obtener_por_id(session: Session, hogar_id: int) -> HogarTransito | None:
    return session.get(HogarTransito, hogar_id)


def guardar(session: Session, hogar: HogarTransito) -> HogarTransito:
    session.add(hogar)
    session.commit()
    session.refresh(hogar)
    return hogar


def listar_asignaciones(session: Session, hogar_id: int, solo_activas: bool = False) -> list[AsignacionTransito]:
    consulta = (
        select(AsignacionTransito)
        .where(col(AsignacionTransito.hogar_transito_id) == hogar_id)
        .order_by(col(AsignacionTransito.fecha_ingreso))
    )
    if solo_activas:
        consulta = consulta.where(col(AsignacionTransito.fecha_salida).is_(None))
    return list(session.exec(consulta).all())


def obtener_asignacion_activa_de_animal(session: Session, animal_id: int) -> AsignacionTransito | None:
    consulta = select(AsignacionTransito).where(
        col(AsignacionTransito.animal_id) == animal_id,
        col(AsignacionTransito.fecha_salida).is_(None),
    )
    return session.exec(consulta).first()


def obtener_asignacion(session: Session, asignacion_id: int) -> AsignacionTransito | None:
    return session.get(AsignacionTransito, asignacion_id)


def guardar_asignacion(session: Session, asignacion: AsignacionTransito) -> AsignacionTransito:
    session.add(asignacion)
    session.commit()
    session.refresh(asignacion)
    return asignacion
