from pydantic import BaseSettings, PostgresDsn


class ConfigDB(BaseSettings):
    DSN: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config_db: ConfigDB = ConfigDB(_env_file=".env")
