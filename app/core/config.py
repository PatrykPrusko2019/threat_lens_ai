from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "ThreatLeans AI"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "threatlens"
    db_user: str = "postgres"
    db_password: str = "postgres"

    secret_key: str = "change-this-in-env-later"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
settings = Settings()