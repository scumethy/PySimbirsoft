from gino_starlette import Gino

import config

db = Gino(dsn=config.DB_DSN)