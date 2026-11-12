from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings


engine = create_engine(settings.database_url)


def create_db_and_tables() -> None:
    """Crea en la base las tablas de todos los modelos SQLModel que existan."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: abre una sesión por cada request y la cierra al terminar."""
    with Session(engine) as session:
        yield session