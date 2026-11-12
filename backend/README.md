# Backend
API y lógica de negocio de RescuePet.

## Tecnologías
- Python
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- Uvicorn
- PostgreSQL
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

5. Copiar el archivo `.env.example` con el nombre `.env` y completar la contraseña de PostgreSQL en `DATABASE_URL`.

6. Iniciar el servidor:
   ```bash
   fastapi dev app/main.py
   ```

Al iniciar, el backend crea automáticamente las tablas en la base de datos.

La API queda disponible en `http://localhost:8000` y la documentación interactiva (Swagger UI) en `http://localhost:8000/docs`.

Para verificar que funciona, el endpoint `GET /api/health` debe responder `{"status": "ok"}`.