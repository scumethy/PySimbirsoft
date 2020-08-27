from gino_starlette import Gino
import aioredis

from src import config
from src.api.integrate import (
    UserServiceAPI,
    MonitoringServiceAPI,
    GoodsServiceAPI,
    MailServiceAPI,
)

db = Gino(dsn=config.DB_DSN)

user_service = UserServiceAPI(config.USER_SERVICE_URL)
monitoring = MonitoringServiceAPI(config.MONITORING_URL)
goods_service = GoodsServiceAPI(config.GOODS_SERVICE_URL)
mail_service = MailServiceAPI(config.MAIL_SERVICE_URL)
