from enum import Enum


class RolNombre(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    RESCATISTA = "RESCATISTA"
    HOGAR_TRANSITO = "HOGAR_TRANSITO"
    ADOPTANTE = "ADOPTANTE"


class Especie(str, Enum):
    PERRO = "Perro"
    GATO = "Gato"
    OTRO = "Otro"


class Tamano(str, Enum):
    PEQUENO = "Pequeño"
    MEDIANO = "Mediano"
    GRANDE = "Grande"


class Sexo(str, Enum):
    MACHO = "Macho"
    HEMBRA = "Hembra"


class EstadoAnimal(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    EN_TRANSITO = "EN_TRANSITO"
    EN_PROCESO_ADOPCION = "EN_PROCESO_ADOPCION"
    ADOPTADO = "ADOPTADO"
    INACTIVO = "INACTIVO"


class TipoRegistroSanitario(str, Enum):
    VACUNA = "VACUNA"
    TRATAMIENTO = "TRATAMIENTO"
    CONSULTA = "CONSULTA"


class EstadoPublicacion(str, Enum):
    ACTIVA = "ACTIVA"
    PAUSADA = "PAUSADA"
    FINALIZADA = "FINALIZADA"


class EstadoSolicitud(str, Enum):
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"
    CANCELADA = "CANCELADA"


class EstadoAdopcion(str, Enum):
    EN_SEGUIMIENTO = "EN_SEGUIMIENTO"
    FINALIZADA = "FINALIZADA"