from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_ADDRESS: str = "0.0.0.0:8080"
    POSTGRES_CONN: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str | int = "5432"


settings = Settings()
