from datetime import date, timedelta

from app.core.database import create_db_and_tables
from app.core.seed import cargar_roles
from app.core.uow import UnitOfWork
from app.models.enums import (
    Especie,
    EstadoPublicacion,
    RolNombre,
    Sexo,
    Tamano,
    TipoRegistroSanitario,
    TipoVivienda,
)
from app.schemas.animal import AnimalCreate
from app.schemas.hogar_transito import AsignacionCreate, HogarTransitoCreate
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate
from app.schemas.registro_sanitario import RegistroSanitarioCreate
from app.schemas.rescate import RescateCreate
from app.schemas.solicitud import AprobacionDatos, SolicitudCreate
from app.schemas.adopcion import SeguimientoCreate
from app.schemas.usuario import UsuarioCreate, UsuarioPublic
from app.services.adopcion_service import AdopcionService
from app.services.animal_service import AnimalService
from app.services.hogar_transito_service import HogarTransitoService
from app.services.publicacion_service import PublicacionService
from app.services.registro_sanitario_service import RegistroSanitarioService
from app.services.rescate_service import RescateService
from app.services.solicitud_service import SolicitudService
from app.services.usuario_service import UsuarioService

CONTRASENA_DEMO = "Demo1234!"
HOY = date.today()


def hace(dias: int) -> date:
    return HOY - timedelta(days=dias)


def foto(nombre: str) -> str:
    return f"https://placehold.co/600x400?text={nombre}"


def crear_usuario(nombre: str, apellido: str, email: str, rol: RolNombre) -> UsuarioPublic:
    return UsuarioService(UnitOfWork()).registrar(
        UsuarioCreate(nombre=nombre, apellido=apellido, email=email, password=CONTRASENA_DEMO, rol=rol)
    )


def ya_cargados() -> bool:
    with UnitOfWork() as uow:
        return uow.usuarios.obtener_por_email("lucia@demo.com") is not None


def cargar() -> None:
    create_db_and_tables()
    cargar_roles()
    if ya_cargados():
        print("Los datos demo ya están cargados. No se hizo ningún cambio.")
        return

    # Usuarios 
    lucia = crear_usuario("Lucía", "Fernández", "lucia@demo.com", RolNombre.RESCATISTA)
    martin = crear_usuario("Martín", "Gómez", "martin@demo.com", RolNombre.RESCATISTA)
    carla = crear_usuario("Carla", "Ríos", "carla@demo.com", RolNombre.HOGAR_TRANSITO)
    juan = crear_usuario("Juan", "Pérez", "juan@demo.com", RolNombre.ADOPTANTE)
    sofia = crear_usuario("Sofía", "Díaz", "sofia@demo.com", RolNombre.ADOPTANTE)

    animales = AnimalService(UnitOfWork())
    rescates = RescateService(UnitOfWork())
    salud = RegistroSanitarioService(UnitOfWork())
    hogares = HogarTransitoService(UnitOfWork())
    publicaciones = PublicacionService(UnitOfWork())
    solicitudes = SolicitudService(UnitOfWork())
    adopciones = AdopcionService(UnitOfWork())

    # Animales con su rescate
    datos_animales = [
        ("Toby", Especie.PERRO, "Mestizo", Sexo.MACHO, 3, Tamano.GRANDE,
        "Grandote, juguetón y muy cariñoso. Se lleva bien con chicos.", lucia, "Barrio Alberdi", 60),
        ("Luna", Especie.GATO, "Común europeo", Sexo.HEMBRA, 1, Tamano.PEQUENO,
        "Tranquila y curiosa. Le encanta dormir al sol.", lucia, "Plaza España", 45),
        ("Rocky", Especie.PERRO, "Mestizo", Sexo.MACHO, 5, Tamano.MEDIANO,
        "Compañero ideal para caminatas. Ya está castrado.", martin, "Villa Allende", 90),
        ("Mora", Especie.GATO, None, Sexo.HEMBRA, 2, Tamano.PEQUENO,
        "Algo tímida al principio, muy mimosa después.", martin, "Barrio Güemes", 20),
        ("Simba", Especie.PERRO, "Labrador mestizo", Sexo.MACHO, 4, Tamano.GRANDE,
        "Energía de sobra. Necesita un hogar con espacio.", martin, "Río Ceballos", 30),
        ("Copito", Especie.OTRO, "Conejo", Sexo.MACHO, 1, Tamano.PEQUENO,
        "Conejo enano, muy sociable.", lucia, "Nueva Córdoba", 15),
    ]
    ids = {}
    for nombre, especie, raza, sexo, edad, tamano, descripcion, rescatista, lugar, dias in datos_animales:
        animal = animales.crear(
            AnimalCreate(nombre=nombre, especie=especie, raza=raza, sexo=sexo, edad_aproximada=edad,
                        tamano=tamano, descripcion=descripcion, foto_url=foto(nombre))
        )
        ids[nombre] = animal.id
        rescates.registrar(
            animal.id,
            RescateCreate(fecha_rescate=hace(dias), ubicacion=f"{lugar}, Córdoba",
                        descripcion=f"Rescatado en {lugar}."),
            rescatista,
        )

    # Historial sanitario 
    for nombre, tipo, dias, descripcion in [
        ("Toby", TipoRegistroSanitario.CONSULTA, 58, "Control general al ingreso. Buen estado."),
        ("Toby", TipoRegistroSanitario.VACUNA, 50, "Vacuna antirrábica."),
        ("Luna", TipoRegistroSanitario.VACUNA, 40, "Triple felina."),
        ("Rocky", TipoRegistroSanitario.TRATAMIENTO, 85, "Desparasitación interna y externa."),
        ("Rocky", TipoRegistroSanitario.VACUNA, 80, "Vacuna séxtuple."),
        ("Simba", TipoRegistroSanitario.CONSULTA, 25, "Control de peso. Sano."),
    ]:
        salud.crear(
            ids[nombre],
            RegistroSanitarioCreate(tipo=tipo, fecha=hace(dias), descripcion=descripcion, veterinario="Dra. Paula Sosa"),
        )

    # Hogar de tránsito con Luna alojada 
    hogar = hogares.crear(
        HogarTransitoCreate(direccion="Alta Córdoba, Córdoba", capacidad=3,
                            observaciones="Casa con patio. Acepta perros y gatos."),
        carla,
    )
    hogares.asignar_animal(hogar.id, AsignacionCreate(animal_id=ids["Luna"], fecha_ingreso=hace(40)))

    # Publicaciones 
    pub_toby = publicaciones.crear(
        PublicacionCreate(animal_id=ids["Toby"], titulo="Toby busca una familia con patio",
                        descripcion="Perro grande, sano y vacunado. Ideal para una casa con espacio."),
        lucia,
    )
    publicaciones.crear(
        PublicacionCreate(animal_id=ids["Luna"], titulo="Luna, gatita tranquila",
                        descripcion="Está en un hogar de tránsito. Vacunada y lista para adoptar."),
        lucia,
    )
    publicaciones.crear(
        PublicacionCreate(animal_id=ids["Rocky"], titulo="Rocky, el compañero ideal",
                        descripcion="Tranquilo y castrado. Se adapta a casa o departamento."),
        martin,
    )
    pub_simba = publicaciones.crear(
        PublicacionCreate(animal_id=ids["Simba"], titulo="Simba necesita espacio",
                        descripcion="Labrador mestizo con mucha energía."),
        martin,
    )
    publicaciones.actualizar(pub_simba.id, PublicacionUpdate(estado=EstadoPublicacion.PAUSADA), martin)

    # Solicitudes
    solicitudes.crear(
        SolicitudCreate(animal_id=ids["Toby"], tipo_vivienda=TipoVivienda.CASA_CON_PATIO, tiene_patio=True,
                        tiene_otros_animales=False, experiencia_previa="Crecí con perros grandes.",
                        motivo="Tenemos una casa con patio grande y tiempo para paseos largos todos los días."),
        juan,
    )
    solicitudes.crear(
        SolicitudCreate(animal_id=ids["Toby"], tipo_vivienda=TipoVivienda.DEPARTAMENTO, tiene_patio=False,
                        tiene_otros_animales=True, motivo="Me encantan los perros."),
        sofia,
    )
    solicitud_rocky = solicitudes.crear(
        SolicitudCreate(animal_id=ids["Rocky"], tipo_vivienda=TipoVivienda.CASA_SIN_PATIO, tiene_patio=False,
                        tiene_otros_animales=False, experiencia_previa="Tuve un perro durante 10 años.",
                        motivo="Busco un compañero tranquilo para salir a caminar."),
        sofia,
    )

    # Adopcion concretada (Rocky → Sofía) con un seguimiento 
    adopcion = solicitudes.aprobar(
        solicitud_rocky.id,
        AprobacionDatos(fecha_adopcion=hace(14), observaciones="Se entregó con collar y libreta sanitaria."),
        martin,
    )
    adopciones.crear_seguimiento(
        adopcion.id,
        SeguimientoCreate(fecha=hace(7), estado_general="Muy bien", resultado="Adaptado",
                    observaciones="Se adaptó rápido. Duerme en su cucha y sale a caminar a diario."),
        martin,
    )

    print("Datos demo cargados.")
    print(f"Usuarios (contraseña para todos: {CONTRASENA_DEMO}):")
    for usuario in (lucia, martin, carla, juan, sofia):
        print(f"  - {usuario.email:<18} {', '.join(usuario.roles)}")
    print(f"Publicación de Toby (id {pub_toby.id}) con 2 solicitudes pendientes para aprobar.")


if __name__ == "__main__":
    cargar()