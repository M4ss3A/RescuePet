# Database

RescuePet utilizará una base de datos relacional PostgreSQL, tanto para el desarrollo local como para la versión desplegada.
El acceso a los datos se realizará desde el backend mediante SQLModel (SQLAlchemy + Pydantic). Ver [Cambios técnicos y justificación](../docs/cambios_tecnicos.md).


## Entidades y atributos principales

- Usuario:	id, nombre, apellido, email, contrasenaHash, telefono, direccion, activo, fechaRegistro.
- Rol:	id, nombre, descripcion.
- UsuarioRol:	usuarioId, rolId.
- Animal:	id, nombre, especie, raza, sexo, edadAproximada, tamano, descripcion, estado, fechaAlta.
- Rescate:	id, animalId, rescatistaId, fechaRescate, ubicacion, descripcion.
- FotoAnimal:	id, animalId, url, descripcion, esPrincipal.
- RegistroSanitario:	id, animalId, tipo, fecha, descripcion, veterinario.
- HogarTransito:	id, responsableId, direccion, capacidad, disponible, observaciones.
- AsignacionTransito:	id, animalId, hogarTransitoId, fechaIngreso, fechaSalida, observaciones.
- Publicacion:	id, animalId, autorId, titulo, descripcion, fechaPublicacion, estado.
- SolicitudAdopcion:	id, publicacionId, adoptanteId, fechaSolicitud, estado, tipoVivienda, tienePatio, tieneOtrosAnimales, experienciaPrevia, motivo, puntajeCompatibilidad.
- Adopcion:	id, solicitudId, fechaAdopcion, estado, observaciones.
- Seguimiento:	id, adopcionId, fecha, observaciones, estadoGeneral, resultado.

Las relaciones y cardinalidades se representarán en el diagrama entidad-relación. El modelo fisico se documentara en el archivo schema.sql.

## Valores permitidos

Las columnas de tipo estado o categoría se almacenan como `VARCHAR`. Los valores válidos se controlan desde el backend mediante enumeraciones (`backend/app/models/enums.py`):

| Tabla.columna | Valores |
|---|---|
| roles.nombre | ADMINISTRADOR, RESCATISTA, HOGAR_TRANSITO, ADOPTANTE |
| animales.especie | Perro, Gato, Otro |
| animales.sexo | Macho, Hembra |
| animales.tamano | Pequeño, Mediano, Grande |
| animales.estado | DISPONIBLE, EN_TRANSITO, EN_PROCESO_ADOPCION, ADOPTADO, INACTIVO |
| registros_sanitarios.tipo | VACUNA, TRATAMIENTO, CONSULTA |
| publicaciones.estado | ACTIVA, PAUSADA, FINALIZADA |
| solicitudes_adopcion.estado | PENDIENTE, APROBADA, RECHAZADA, CANCELADA |
| adopciones.estado | EN_SEGUIMIENTO, FINALIZADA |

Las fechas con hora se almacenan en UTC.


## Restricciones de unicidad

- Un usuario por email.
- Un rescate por animal.
- Una adopción por solicitud.
- Un adoptante no puede enviar más de una solicitud a la misma publicación.

## Índices principales

Se definieron índices para optimizar las consultas más frecuentes del sistema:

- Busqueda de usuarios por email.
- Consulta de animales segun su estado.
- Consulta cronológica de registros sanitarios.
- Búsqueda de hogares de tránsito disponibles.
- Consulta de asignaciones actuales de cada animal.
- Listado de publicaciones por estado y fecha.
- Consulta de solicitudes por publicación, adoptante y estado.
- Consulta cronológica de los seguimientos de una adopción.

Los campos unicos, como el correo del usuario, el nombre del rol, el rescate asociado a un animal y la solicitud asociada a una adopcion, también generan índices para evitar valores duplicados.
