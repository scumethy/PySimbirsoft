import os
from dotenv import load_dotenv

load_dotenv()

# postgres configs
DB = {
    "USER": os.getenv("PG_USER"),
    "PASSWORD": os.getenv("PG_PASSWORD"),
    "HOST": os.getenv("PG_HOST"),
    "PORT": os.getenv("PG_PORT"),
    "NAME": os.getenv("DB_NAME"),
}

# redis configs
REDIS = {"HOST": os.getenv("REDIS_HOST"), "PORT": os.getenv("REDIS_PORT")}

# jwt configs
JWT = {
    "SECRET": os.getenv("SECRET"),
    "ALGORITHM": os.getenv("ALGORITHM"),
}
