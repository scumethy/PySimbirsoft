import os
from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret
from dotenv import load_dotenv
load_dotenv()

config = Config(".env")

DB_DRIVER = config("DB_DRIVER", default="postgresql")
DB_HOST = config("PG_HOST")
DB_PORT = config("PG_PORT", cast=int, default=None)
DB_USER = config("PG_USER", default=None)
DB_PASSWORD = config("PG_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_NAME", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
MONITORING_URL = os.getenv("MONITORING_URL")
GOODS_SERVICE_URL = os.getenv("GOODS_SERVICE_URL")
MAIL_SERVICE_URL = os.getenv("MAIL_SERVICE_URL")

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_DSN = "amqp://{user}:{password}@{host}/".format(
    user=RABBITMQ_USER, password=RABBITMQ_PASS, host=RABBITMQ_HOST
)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
