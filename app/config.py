from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_DSN: PostgresDsn = PostgresDsn("postgres://user:password@db:5432/bigtrip")


def get_config() -> Config:
    return Config()
