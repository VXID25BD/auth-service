from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_ACCESS_SECRET: str = "JWT-ACCESS-SECRET"
    ALGORITHM: str = "SHA256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
