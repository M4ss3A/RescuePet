# Cambios Tecnicos y justificacion

Este documento registra los cambios realizados sobre las decisiones técnicas presentadas en la segunda entrega ([Arquitectura y módulos](./Arquitectura_y_Modulos.md)) y explica el motivo de cada uno.

## Resumen

| Aspecto | Segunda entrega | Decisión actual |
|---|---|---|
| Lenguaje del backend | Java | Python |
| Framework del backend | Spring Boot | FastAPI |
| Persistencia / ORM | Spring Data JPA + Hibernate | SQLModel (SQLAlchemy + Pydantic) |
| Validación y DTOs | DTOs Java + Bean Validation | Modelos Pydantic / SQLModel |
| Documentación de la API | Swagger / OpenAPI | Swagger / OpenAPI (generado automáticamente por FastAPI) |
| Base de datos de desarrollo | H2 | PostgreSQL |
| Base de datos desplegada | MySQL | PostgreSQL |
| Frontend | HTML, CSS, JavaScript y TypeScript | React + TypeScript + Vite + Tailwind CSS |

Se mantienen sin cambios: la arquitectura cliente-servidor, la API REST con intercambio en JSON, la organización por capas, el modelo relacional (tablas, columnas y relaciones), el despliegue en Railway y Netlify, Postman y Git/GitHub.

---

## 1. Backend: de Java + Spring Boot a Python + FastAPI

### Cambio
El backend se desarrollará en **Python con FastAPI** en lugar de Java con Spring Boot. Sigue siendo una **API REST** que intercambia JSON con el frontend, por lo que el contrato entre ambas partes no se modifica.

### Justificación
- **Conocimiento actualizado del equipo:** FastAPI, SQLModel y la conexión con bases de datos relacionales fueron trabajados recientemente en la cursada (Programación IV). Esto reduce la curva de aprendizaje y permite enfocar el tiempo en las reglas de negocio del sistema.
- **Menor cantidad de código repetitivo:** en FastAPI un mismo modelo puede cumplir el rol de entidad de base de datos y de esquema de validación. En Spring Boot cada recurso requiere entidad, repositorio, DTO, mapeo y configuración por separado. Con trece tablas en el modelo, esta diferencia impacta en los tiempos de desarrollo.
- **Validación integrada:** Pydantic valida tipos, campos obligatorios y formatos de los datos de entrada y devuelve errores claros (HTTP 422) sin código adicional.
- **Documentación automática:** FastAPI genera la especificación OpenAPI y la interfaz Swagger UI (`/docs`) a partir del propio código, lo que mantiene la documentación de la API siempre sincronizada con la implementación.
- **Afinidad con el frontend:** los modelos tipados de Pydantic se corresponden de forma directa con las interfaces TypeScript del frontend, lo que facilita acordar el formato de las solicitudes y respuestas.
- **Despliegue sin cambios:** Railway soporta aplicaciones Python, por lo que la estrategia de despliegue definida se mantiene.

### Equivalencia de la arquitectura por capas
La organización en capas presentada en la segunda entrega se conserva con su equivalente en FastAPI:

| Spring Boot (segunda entrega) | FastAPI (actual) | Responsabilidad |
|---|---|---|
| `@RestController` | Routers (`APIRouter`) | Reciben las solicitudes HTTP y devuelven las respuestas. |
| `@Service` | Services | Contienen las reglas de negocio. |
| `JpaRepository` | Repositories | Acceden a la base de datos mediante SQLModel. |
| Entidades JPA | Modelos SQLModel (`table=True`) | Representan las tablas. |
| DTOs | Esquemas Pydantic / SQLModel | Definen los datos de entrada y salida de la API. |
| Inyección de dependencias de Spring | `Depends()` de FastAPI | Proveen la sesión de base de datos, el usuario autenticado, etc. |

```text
Frontend (React)
   ↓  HTTP / JSON
API REST (FastAPI)
   ↓
Routers
   ↓
Services
   ↓
Repositories (SQLModel)
   ↓
PostgreSQL
```

### Consideraciones
- Spring Boot es una tecnología muy difundida. Para el alcance de este proyecto, FastAPI ofrece las mismas capacidades necesarias (API REST, validaciones, persistencia, documentación y autenticación) con menor complejidad de configuración.

---

## 2. Persistencia: de JPA/Hibernate a SQLModel

### Cambio
El acceso a datos se implementará con **SQLModel**, que combina SQLAlchemy (ORM) y Pydantic (validación).

### Justificación
- Cumple la misma función que JPA/Hibernate: mapear las tablas relacionales a clases y realizar las consultas sin escribir SQL manualmente.
- Permite definir las relaciones del modelo (1:1, 1:N y N:N) que ya figuran en el diagrama entidad-relación.
- Es la herramienta de persistencia trabajada en la cursada junto con PostgreSQL.

### Impacto en el modelo de datos
**El modelo relacional no cambia.** Las tablas, columnas, claves y relaciones definidas en [`database/schema.sql`](../database/schema.sql) y en el [diagrama entidad-relación](../database/Diagrama_E-R.md) siguen vigentes. Los modelos SQLModel del backend se construirán a partir de ese esquema.

---

## 3. Base de datos: de H2 y MySQL a PostgreSQL

### Cambio
Se utilizará **PostgreSQL** tanto para el desarrollo local como para la versión desplegada, en lugar de H2 (desarrollo) y MySQL (producción).

### Justificación
- **Tecnología trabajada en la cursada:** PostgreSQL es el motor de base de datos utilizado en Programación IV junto con FastAPI y SQLModel.
- **Mismo motor en desarrollo y producción:** al usar la misma base en ambos entornos se evitan diferencias de comportamiento entre motores distintos.
- **H2 no se integra con Python:** es una base de datos pensada para el ecosistema Java.
- **Despliegue sin cambios en la estrategia:** Railway ofrece PostgreSQL como servicio administrado, igual que MySQL.
- **Configuración por entorno:** la conexión se define con una variable de entorno (`DATABASE_URL`), por lo que pasar de la base local a la desplegada no requiere cambios en el código.

### Impacto en el modelo de datos
Las tablas, columnas, claves y relaciones no cambian. Solo se adaptó la sintaxis de [`database/schema.sql`](../database/schema.sql) a PostgreSQL:

| MySQL | PostgreSQL |
|---|---|
| `BIGINT AUTO_INCREMENT PRIMARY KEY` | `SERIAL PRIMARY KEY` |
| `DATETIME` | `TIMESTAMPTZ` (fecha y hora con zona horaria) |

Además, las claves primarias y foráneas pasaron de `BIGINT` a `INTEGER`. El rango de `INTEGER` (más de 2.000 millones de registros) es suficiente para el volumen esperado del sistema, ocupa la mitad de espacio y es el tipo que SQLModel utiliza por defecto para los identificadores.
---
## 4. Frontend: React + TypeScript + Vite + Tailwind CSS

### Cambio
En la segunda entrega el frontend se describió con HTML, CSS, JavaScript y TypeScript. La implementación se realiza con **React** y **TypeScript**, utilizando **Vite** como herramienta de desarrollo y **Tailwind CSS** para los estilos.

### Justificación
- React permite construir la interfaz con componentes reutilizables (por ejemplo, tarjetas de animales, encabezado y rutas protegidas por rol), lo que facilita el mantenimiento a medida que crecen las pantallas.
- TypeScript se mantiene y aporta tipado a los datos que se reciben de la API.
- Vite ofrece un entorno de desarrollo rápido y un proceso de compilación simple para el despliegue en Netlify.
- Tailwind CSS agiliza la maquetación con estilos consistentes.
- Son tecnologías trabajadas durante la carrera.

---

## Tecnologías definitivas

**Backend:** Python, FastAPI, SQLModel, Pydantic, Uvicorn, autenticación con JWT y contraseñas almacenadas con hash.

**Frontend:** React, TypeScript, Vite, Tailwind CSS.

**Base de datos:** modelo relacional con PostgreSQL, tanto para desarrollo como para la versión desplegada.

**Herramientas:** Swagger / OpenAPI, Postman, Git y GitHub.

**Despliegue:** backend y PostgreSQL en Railway; frontend en Netlify.