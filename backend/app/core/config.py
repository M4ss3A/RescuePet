from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación, leída desde variables de entorno o el archivo .env."""

    app_name: str = "RescuePet API"
    database_url: str
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte 'http://a.com,http://b.com' en una lista de orígenes."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()  # type: ignore