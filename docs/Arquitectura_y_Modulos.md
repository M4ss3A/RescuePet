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








