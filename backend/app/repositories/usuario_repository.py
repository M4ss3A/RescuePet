from app.core.base_repository import BaseRepository
from app.models import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    modelo = Usuario
