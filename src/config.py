from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""

    # Configuration PostgreSQL (selon run_postgres.sh)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "bdf_demo"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5434

    @property
    def database_url(self) -> str:
        """URL de connexion à la base de données"""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
