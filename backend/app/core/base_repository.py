from sqlmodel import Session, SQLModel


class BaseRepository[T: SQLModel]:
    """Operaciones comunes a todos los repositorios. Usa flush(), nunca commit():
    la transacción la confirma el Unit of Work."""

    modelo: type[T]

    def __init__(self, session: Session) -> None:
        self.session = session

    def obtener_por_id(self, entidad_id: int) -> T | None:
        return self.session.get(self.modelo, entidad_id)

    def agregar(self, entidad: T) -> T:
        self.session.add(entidad)
        self.session.flush()  # envía el INSERT/UPDATE y obtiene el id, sin confirmar
        return entidad

    def eliminar(self, entidad: T) -> None:
        self.session.delete(entidad)
        self.session.flush()
