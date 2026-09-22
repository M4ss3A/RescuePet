# Segunda entrega — Arquitectura y módulos

Esta entrega documentara la arquitectura general de RescuePet, los módulos que formaran parte del sistema y el modelo inicial de la base de datos.

La segunda entrega incluirá:

* Arquitectura general del sistema.
* Listado definitivo de módulos.
* Entidades, atributos y relaciones.
* Diagrama de entidad-relación.
* Esquema inicial de la base de datos.


## Arquitectura general

RescuePet utiliza una arquitectura cliente-servidor organizada por capas. El frontend se comunica con el backend mediante una API REST.

La arquitectura esta compuesta por:

* **Frontend:** interfaz desarrollada con HTML5, CSS3, JavaScript y TypeScript.
* **Controller:** recibe las solicitudes HTTP y devolvuelve las respuestas de la API.
* **Service:** contiene las reglas de negocio y coordina las operaciones del sistema.
* **Repository:** gestiona el acceso a los datos mediante Spring Data JPA.
* **Persistencia:** se implementa con JPA/Hibernate.
* **Base de datos:** se utiliza  H2 para el desarrollo y las pruebas locales, y MySQL para la versión desplegada.

La información se intercambia entre el frontend y el backend mediante solicitudes HTTP y respuestas en formato JSON.

```text
Frontend
   ↓
API REST
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
MySQL
```

El backend desarrollado con Spring Boot será desplegado en Railway y el frontend será publicado en Netlify.


## Modulos del sistema

Organizados por prioridad.

### Prioridad alta
- **Gestión de usuarios y roles**: permitirá registrar y administrar los datos básicos de los usuarios, diferenciando sus responsabilidades dentro del sistema.
- **Gestión de animales y rescates**: permitirá registrar animales rescatados, su estado general y la información relacionada con el rescate.
- **Publicaciones de adopción**: permitirá publicar y consultar los animales que se encuentren disponibles para ser adoptados.
- **Solicitudes de adopción**: permitirá que los interesados envíen una solicitud y que los responsables puedan evaluarla, aprobarla o rechazarla.
- **Gestión de adopciones**: permitirá registrar la adopción de un animal a partir de una solicitud aprobada y actualizar su estado.

*Estos módulos conformarán el producto mínimo viable de RescuePet.*

### Prioridad media
- **Gestión sanitaria**: permitirá registrar controles veterinarios, vacunas y tratamientos de los animales.
- **Gestión de hogares de tránsito**: permitirá registrar hogares disponibles y asociar temporalmente animales rescatados.
- **Seguimiento posterior a la adopción**: permitirá registrar observaciones y novedades sobre la adaptación del animal.

### Prioridad baja
- **Panel de información**: permitirá visualizar cantidades y estados generales relacionados con animales, solicitudes y adopciones.







