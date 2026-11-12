from sqlmodel import SQLModel, create_engine

from app import models  # noqa: F401  (registra los modelos para crear las tablas)
from app.core.config import settings

engine = create_engine(settings.database_url)


def create_db_and_tables() -> None:
    """Crea en la base las tablas de todos los modelos SQLModel que existan."""
    SQLModel.metadata.create_all(engine)
