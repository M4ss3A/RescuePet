# Database

RescuePet utilizará una base de datos relacional. Durante el desarrollo y las pruebas locales se utilizará H2, mientras que la versión desplegada utilizará MySQL.
El acceso a los datos se realizará desde el backend mediante Spring Data JPA y Hibernate.


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
