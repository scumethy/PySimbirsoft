from pydantic import BaseSettings
from pydantic.fields import Field

__all__ = ["config"]


class Config(BaseSettings):
    db_user: str = Field(None, env="PG_USER", required=True)

    db_pass: str = Field(None, env="PG_PASSWORD", required=True)

    db_host: str = Field(None, env="PG_HOST", required=True)

    db_port: str = Field(None, env="PG_PORT", required=True)

    db_name: str = Field(None, env="DB_NAME", required=True)

    redis_host: str = Field(None, env="REDIS_HOST", required=True)

    redis_port: str = Field(None, env="REDIS_PORT", required=True)

    jwt_secret: str = Field(None, env="SECRET", required=True)

    jwt_algo: str = Field(None, env="ALGORITHM", required=True)


config = Config()
