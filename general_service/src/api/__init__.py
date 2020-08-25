from gino_starlette import Gino
import aioredis

from src import config
from src.api.integrate import UserServiceAPI

db = Gino(dsn=config.DB_DSN)

user_service = UserServiceAPI(config.USER_SERVICE_URL)
