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