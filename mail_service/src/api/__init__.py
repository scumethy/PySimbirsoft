from gino_starlette import Gino

from .. import config

db = Gino(dsn=config.DB_DSN)
