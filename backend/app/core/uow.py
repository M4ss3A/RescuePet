from sqlmodel import Session

from app.core.database import engine
from app.repositories.animal_repository import AnimalRepository
from app.repositories.hogar_transito_repository import AsignacionTransitoRepository, HogarTransitoRepository
from app.repositories.registro_sanitario_repository import RegistroSanitarioRepository
from app.repositories.rescate_repository import RescateRepository
from app.repositories.usuario_repository import RolRepository, UsuarioRepository
from app.repositories.adopcion_repository import AdopcionRepository, SeguimientoRepository
from app.repositories.publicacion_repository import PublicacionRepository
from app.repositories.solicitud_repository import SolicitudRepository
from app.repositories.estadistica_repository import EstadisticaRepository

class UnitOfWork:
    """Controla la transacción: abre la sesión, expone los repositorios que la comparten
    y al salir del bloque `with` hace commit si todo salió bien o rollback si hubo un error."""

    def __enter__(self) -> "UnitOfWork":
        self.session = Session(engine, expire_on_commit=False)
        self.usuarios = UsuarioRepository(self.session)
        self.roles = RolRepository(self.session)
        self.animales = AnimalRepository(self.session)
        self.rescates = RescateRepository(self.session)
        self.registros_sanitarios = RegistroSanitarioRepository(self.session)
        self.hogares = HogarTransitoRepository(self.session)
        self.asignaciones = AsignacionTransitoRepository(self.session)
        self.publicaciones = PublicacionRepository(self.session)
        self.solicitudes = SolicitudRepository(self.session)
        self.adopciones = AdopcionRepository(self.session)
        self.seguimientos = SeguimientoRepository(self.session)
        self.estadisticas = EstadisticaRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()

