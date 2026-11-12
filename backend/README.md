# Backend
API y lógica de negocio de RescuePet.

## Tecnologías
- Python
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- Uvicorn
- SQLite (desarrollo) / MySQL (producción)
- JWT para autenticación

## Organización por capas
```text
Routers → Services → Repositories → Base de datos
```

- **Routers:** definen los endpoints REST y reciben las solicitudes HTTP.
- **Services:** contienen las reglas de negocio.
- **Repositories:** acceden a la base de datos mediante SQLModel.
- **Models / Schemas:** representan las tablas y los datos de entrada y salida de la API.

La documentación interactiva de la API estará disponible en `/docs` (Swagger UI) al ejecutar el servidor.

Las instrucciones de instalación se agregarán junto con la primera versión ejecutable.