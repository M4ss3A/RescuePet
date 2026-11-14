# Backend
API REST y logica de negocio de RescuePet.

## Tecnologías
- **Python 3.13** y **FastAPI**
- **SQLModel** (SQLAlchemy + Pydantic) como ORM
- **PostgreSQL** como base de datos
- **JWT** (`python-jose`) en cookie HttpOnly para la autenticación
- **bcrypt** (`passlib`) para el hash de contraseñas
- **pytest** para las pruebas automatizadas
- **Swagger / OpenAPI**: documentación generada automáticamente por FastAPI

## Arquitectura
El backend está organizado en capas. Cada pedido HTTP recorre la siguiente cadena:

```text
Router  →  Service  →  Unit of Work  →  Repository  →  PostgreSQL
(HTTP)     (reglas)    (transacción)    (consultas)
```

| Capa | Responsabilidad |
|---|---|
| **Router** | Define el endpoint, valida los datos de entrada (schemas) y los permisos (`require_role`). |
| **Service** | Aplica las reglas de negocio. No conoce HTTP: ante un problema lanza un error de dominio. |
| **Unit of Work** | Abre la sesión, comparte una única transacción entre los repositorios y hace `commit` si todo salió bien o `rollback` si hubo un error. Es la única capa que confirma cambios. |
| **Repository** | Realiza las consultas con SQLModel. Usa `flush()`, nunca `commit()`. |

Los errores de dominio (`NoEncontrado`, `Conflicto`, `ReglaDeNegocio`, `SinPermiso`, `NoAutenticado`) se traducen a respuestas HTTP (404, 409, 400, 403 y 401) en un único manejador registrado en `main.py`.

### Estructura de carpetas
```text
backend/
├── app/
│   ├── main.py                 # Crea la aplicación, CORS, manejador de errores y routers
│   ├── datos_demo.py           # Script de carga de datos de ejemplo
│   ├── core/
│   │   ├── config.py           # Configuración leída del archivo .env
│   │   ├── database.py         # Conexión a PostgreSQL y creación de tablas
│   │   ├── uow.py              # Unit of Work
│   │   ├── base_repository.py  # Repositorio genérico (obtener, agregar, eliminar)
│   │   ├── errors.py           # Errores de dominio y su traducción a HTTP
│   │   ├── security.py         # Hash de contraseñas y tokens JWT
│   │   ├── deps.py             # Usuario actual y control de roles
│   │   └── seed.py             # Roles y administrador inicial
│   ├── models/                 # Tablas (SQLModel) y enumeraciones
│   ├── schemas/                # Datos de entrada y salida de la API (DTO)
│   ├── repositories/           # Consultas a la base de datos
│   ├── services/               # Reglas de negocio
│   └── routers/                # Endpoints
├── tests/                      # Pruebas automatizadas (pytest)
├── pytest.ini
├── requirements.txt
└── .env.example
```

## Requisitos
- Python 3.13 o superior
- PostgreSQL

## Instalación y ejecución

1. Crear una base de datos vacía llamada `rescuepet` en PostgreSQL (por ejemplo, desde pgAdmin).

2. Ubicarse en la carpeta del backend:
   ```bash
   cd backend
   ```

3. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   ```
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Linux / macOS: `source .venv/bin/activate`

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Copiar el archivo `.env.example` con el nombre `.env` y completar los valores (ver la sección siguiente).

6. Iniciar el servidor:
   ```bash
   fastapi dev app/main.py
   ```

Al iniciar, el backend crea las tablas, carga los roles del sistema y, si está configurado, el administrador inicial.

La API queda disponible en `http://localhost:8000` y la documentación interactiva (Swagger UI) en `http://localhost:8000/docs`. Para verificar que funciona, `GET /api/v1/health` debe responder `{"status": "ok"}`.

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DATABASE_URL` | Sí | Conexión a PostgreSQL: `postgresql+psycopg://USUARIO:CONTRASEÑA@localhost:5432/rescuepet` |
| `SECRET_KEY` | Sí | Clave para firmar los tokens JWT. Mínimo 32 caracteres. Si falta, la aplicación no inicia. |
| `CORS_ORIGINS` | No | Orígenes del frontend separados por coma. Por defecto: `http://localhost:5173` |
| `ADMIN_EMAIL` | No | Email del administrador inicial. |
| `ADMIN_PASSWORD` | No | Contraseña del administrador inicial. |

Para generar una `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

El archivo `.env` contiene datos sensibles y está excluido del repositorio. Solo se versiona `.env.example`.

## Datos de ejemplo
Para cargar datos de prueba (usuarios de cada rol, animales, un hogar de tránsito, publicaciones, solicitudes y una adopción con seguimiento):
```bash
python -m app.datos_demo
```

Los datos se cargan a través de los mismos services que usa la API, por lo que cumplen todas las reglas de negocio. Si ya están cargados, el script no realiza cambios.

| Usuario | Rol |
|---|---|
| `lucia@demo.com` | RESCATISTA |
| `martin@demo.com` | RESCATISTA |
| `carla@demo.com` | HOGAR_TRANSITO |
| `juan@demo.com` | ADOPTANTE |
| `sofia@demo.com` | ADOPTANTE |

Contraseña de todos los usuarios de ejemplo: `Demo1234!`

## Pruebas automatizadas
```bash
pytest
```

Las pruebas no necesitan PostgreSQL ni el servidor en ejecución: cada test crea una base **SQLite en memoria**, la utiliza en lugar de la base real y la descarta al terminar. Cubren la autenticación, los permisos por rol y por dueño, las reglas de negocio de cada módulo, el cálculo del puntaje de compatibilidad, la aprobación de una adopción como transacción única y el rollback del Unit of Work.

## Autenticación
- **Registro:** `POST /api/v1/auth/register`. Se puede elegir el rol ADOPTANTE (por defecto), RESCATISTA u HOGAR_TRANSITO. El rol ADMINISTRADOR no se puede registrar.
- **Login:** `POST /api/v1/auth/token` con un formulario OAuth2: en el campo `username` se envía el **email**. El token JWT se guarda en una **cookie HttpOnly** (`access_token`) que el navegador envía automáticamente en cada pedido.
- **Logout:** `POST /api/v1/auth/logout`.

En Swagger, iniciar sesión con el endpoint `/auth/token` (no con el botón *Authorize*). Desde el frontend, los pedidos deben enviarse con `credentials: 'include'` (fetch) o `withCredentials: true` (Axios).

Las contraseñas se almacenan con hash bcrypt. En cada pedido se valida el token y se busca al usuario en la base, por lo que una cuenta desactivada pierde el acceso de inmediato.

## Endpoints
Todos los endpoints tienen el prefijo `/api/v1`. Las respuestas usan nombres de campo en camelCase.

| Módulo | Método y ruta | Acceso |
|---|---|---|
| **Autenticación** | `POST /auth/register` · `POST /auth/token` · `POST /auth/logout` | Público |
| | `GET /auth/me` | Usuario logueado |
| **Usuarios** | `GET /admin/usuarios` · `POST /admin/usuarios/{id}/activar` · `POST /admin/usuarios/{id}/desactivar` | Administrador |
| **Animales** | `GET /animales` (filtro `?estado=`) · `GET /animales/{id}` | Público |
| | `POST /animales` · `PATCH /animales/{id}` · `DELETE /animales/{id}` (baja lógica) | Rescatista, Administrador |
| **Rescates** | `GET` · `POST` · `PATCH /animales/{id}/rescate` | Rescatista, Administrador (editar: quien lo registró) |
| **Registros sanitarios** | `GET /animales/{id}/registros-sanitarios` | Público |
| | `POST /animales/{id}/registros-sanitarios` · `PATCH` · `DELETE /registros-sanitarios/{id}` | Rescatista, Hogar de tránsito, Administrador |
| **Hogares de tránsito** | `GET /hogares-transito` (filtro `?disponible=`) · `GET /hogares-transito/{id}` | Rescatista, Hogar de tránsito, Administrador |
| | `POST /hogares-transito` | Hogar de tránsito (queda como responsable) |
| | `PATCH /hogares-transito/{id}` | Responsable del hogar, Administrador |
| | `GET /hogares-transito/{id}/asignaciones` (filtro `?activas=`) | Rescatista, Administrador, responsable del hogar |
| | `POST /hogares-transito/{id}/asignaciones` | Rescatista, Administrador |
| | `PATCH /asignaciones-transito/{id}/egreso` | Rescatista, Administrador, responsable del hogar |
| **Publicaciones** | `GET /publicaciones` (filtro `?estado=`) · `GET /publicaciones/{id}` | Público |
| | `POST /publicaciones` · `PATCH /publicaciones/{id}` (editar, pausar, reactivar) | Rescatista, Administrador (editar: el autor) |
| **Solicitudes** | `POST /solicitudes` · `GET /solicitudes/mias` · `POST /solicitudes/{id}/cancelar` | Usuario logueado |
| | `GET /solicitudes` (recibidas, filtro `?estado=`) | Rescatista (las de sus publicaciones), Administrador |
| | `GET /solicitudes/{id}` | El solicitante, el autor de la publicación, Administrador |
| | `POST /solicitudes/{id}/aprobar` · `POST /solicitudes/{id}/rechazar` | Autor de la publicación, Administrador |
| **Adopciones** | `GET /adopciones` (filtro `?solicitudId=`) · `GET /adopciones/{id}` | Participantes de la adopción, Administrador |
| | `PATCH /adopciones/{id}` (cerrar seguimiento) | Responsable, Administrador |
| **Seguimientos** | `GET /adopciones/{id}/seguimientos` | Participantes de la adopción, Administrador |
| | `POST /adopciones/{id}/seguimientos` | Responsable, Administrador |
| **Estadísticas** | `GET /estadisticas` | Rescatista, Administrador |
| **Estado** | `GET /health` | Público |

El detalle de cada endpoint (campos, tipos y respuestas posibles) está disponible en Swagger (`/docs`).

## Reglas de negocio principales
- **Baja lógica de animales:** un animal no se elimina; pasa a estado `INACTIVO` para conservar su historial.
- **Rescates:** cada animal tiene un único rescate. El rescatista es el usuario logueado.
- **Registros sanitarios:** no se aceptan fechas futuras.
- **Hogares de tránsito:** no se puede superar la capacidad del hogar. Al ingresar a un hogar, el animal pasa a `EN_TRANSITO`; al egresar, vuelve a `DISPONIBLE`.
- **Publicaciones:** solo se publican animales disponibles o en tránsito, con una única publicación vigente por animal. Pueden pausarse y reactivarse; se finalizan automáticamente al concretarse la adopción.
- **Solicitudes:** se envían sobre un animal publicado; el backend identifica su publicación activa. Un usuario no puede solicitar un animal que publicó ni enviar dos solicitudes para el mismo animal.
- **Puntaje de compatibilidad (0 a 100):** se calcula al recibir la solicitud según el tipo de vivienda en relación con el tamaño del animal (40), el patio (10), la experiencia previa (20), la presencia de otros animales (10) y el detalle del motivo (20). Las reglas están en `app/services/compatibilidad.py`.
- **Aprobación de una solicitud (transacción única):** se aprueba la solicitud, se crea la adopción, el animal pasa a `ADOPTADO`, la publicación se finaliza, las demás solicitudes pendientes se rechazan y, si el animal estaba en un hogar de tránsito, se registra su egreso. Si cualquier paso falla, el Unit of Work deshace todos los cambios.
- **Seguimientos:** las fechas no pueden ser futuras ni anteriores a la adopción, y no se cargan seguimientos en una adopción finalizada.