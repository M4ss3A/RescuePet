import os


os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "clave-solo-para-tests-con-mas-de-32-caracteres"

from collections.abc import Callable, Iterator  # noqa: E402

import pytest  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Rol, Usuario  # noqa: E402
from app.models.enums import RolNombre  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402
from sqlmodel import Session, SQLModel, create_engine, select  # noqa: E402

CONTRASENA = "Clave1234!"

# StaticPool
engine_test = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


@pytest.fixture()
def base_de_datos(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Crea las tablas y los roles, y hace que el Unit of Work use la base de prueba."""
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        for rol in RolNombre:
            session.add(Rol(nombre=rol.value))
        session.commit()
    monkeypatch.setattr("app.core.uow.engine", engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture()
def cliente(base_de_datos: None) -> TestClient:
    """Cliente sin sesión iniciada."""
    return TestClient(app)


@pytest.fixture()
def crear_usuario(base_de_datos: None) -> Callable[..., TestClient]:


    def _crear(nombre: str, rol: RolNombre) -> TestClient:
        email = f"{nombre}@test.com"
        with Session(engine_test) as session:
            rol_db = session.exec(select(Rol).where(Rol.nombre == rol.value)).one()
            session.add(
                Usuario(
                    nombre=nombre,
                    apellido="Test",
                    email=email,
                    contrasena_hash=hash_password(CONTRASENA),
                    roles=[rol_db],
                )
            )
            session.commit()
        cliente = TestClient(app)
        respuesta = cliente.post("/api/v1/auth/token", data={"username": email, "password": CONTRASENA})
        assert respuesta.status_code == 200
        return cliente

    return _crear
