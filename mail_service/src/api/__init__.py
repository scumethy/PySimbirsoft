from gino_starlette import Gino

from src import config

db = Gino(dsn=config.DB_DSN)
