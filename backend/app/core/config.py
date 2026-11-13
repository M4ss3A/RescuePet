from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, leída desde variables de entorno o el archivo .env."""

    app_name: str = "RescuePet API"
    database_url: str
    cors_origins: str = "http://localhost:5173"

    # Seguridad (JWT)
    secret_key: str = Field(min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Administrador inicial 
    admin_email: str | None = None
    admin_password: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte 'http://a.com,http://b.com' en una lista de orígenes."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()  # type: ignore