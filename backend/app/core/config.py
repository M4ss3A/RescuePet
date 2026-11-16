from typing import Literal
from pydantic import Field, field_validator
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
    
    # Cookie del token: en local (http) quedan asi; en producción (https) se cambian desde las variables de entorno
    cookie_secure: bool = False
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"

    # Administrador inicial 
    admin_email: str | None = None
    admin_password: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @field_validator("database_url")
    @classmethod
    def usar_driver_psycopg(cls, valor: str) -> str:
        """Railway entrega la URL como 'postgresql://...'; SQLModel necesita 'postgresql+psycopg://...'."""
        if valor.startswith("postgresql://"):
            return valor.replace("postgresql://", "postgresql+psycopg://", 1)
        if valor.startswith("postgres://"):
            return valor.replace("postgres://", "postgresql+psycopg://", 1)
        return valor

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte 'http://a.com,http://b.com' en una lista de orígenes."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()  # type: ignore