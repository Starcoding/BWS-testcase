from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASIC_AUTH_USERNAME: str = "admin"
    BASIC_AUTH_PASSWORD: str = "admin"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    DEBUG: bool = False

    @computed_field  # type: ignore
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
