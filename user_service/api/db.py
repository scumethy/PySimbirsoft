import asyncpgsa
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
)

from .utils import get_password_hash, get_unique_uuid, verify_password, user_to_json
from .config import DB

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", String(36), primary_key=True, unique=True),
    Column("username", String(64), nullable=False, unique=True),
    Column("password_hash", String(100), nullable=False),
)


async def get_user_by_username(db_pool, username):
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow(users.select().where(users.c.username == username))
        result = user_to_json(user)
    return result


async def get_user_by_id(db_pool, id):
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow(users.select().where(users.c.id == id))
        result = user_to_json(user)
    return result


async def add_user(db_pool, username, password):
    userid = get_unique_uuid()
    password_hash = get_password_hash(password)
    async with db_pool.acquire() as conn:
        query = users.insert().values(
            id=userid, username=username, password_hash=password_hash
        )
        await conn.fetch(query)


async def verify_user_data(db_pool, username, password):
    user = await get_user_by_username(db_pool, username)
    if user:
        password_hash = user["password_hash"]
        if verify_password(password_hash, password):
            return user


async def init_db(app):
    dsn = construct_db_url()
    pool = await asyncpgsa.create_pool(dsn=dsn)
    app["db_pool"] = pool
    return pool


def construct_db_url():
    DSN = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        DB["USER"], DB["PASSWORD"], DB["HOST"], DB["PORT"], DB["NAME"]
    )
    return DSN
