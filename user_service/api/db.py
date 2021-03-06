from aiopg.sa import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

from user_service.config import config
import user_service.api.errors as errors
from .utils import get_password_hash, get_unique_uuid, verify_password, user_to_json


Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = "goods_users"
    id = Column(String(36), primary_key=True, unique=True)
    username = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)

    @classmethod
    async def get_user_by_id(cls, db_pool, user_id):
        user_t = cls.__table__
        async with db_pool.acquire() as conn:
            db_result = await conn.execute(
                user_t.select().where(user_t.c.id == user_id)
            )
            selected_line = await db_result.first()
            user = user_to_json(selected_line)
        return user

    @classmethod
    async def get_user_by_username(cls, db_pool, username):
        user_t = cls.__table__
        async with db_pool.acquire() as conn:
            db_result = await conn.execute(
                user_t.select().where(user_t.c.username == username)
            )
            selected_line = await db_result.first()
            if selected_line is not None:
                user = user_to_json(selected_line)
                return user

    @classmethod
    async def add_user(cls, db_pool, username, password):
        user_t = cls.__table__
        userid = get_unique_uuid()
        password_hash = get_password_hash(password)
        async with db_pool.acquire() as conn:
            try:
                await conn.execute(
                    user_t.insert().values(
                        id=userid, username=username, password_hash=password_hash
                    )
                )
            except:
                raise errors.BadRegData

    @classmethod
    async def verify_user_data(cls, db_pool, username, password):
        user = await User.get_user_by_username(db_pool, username)
        if user:
            password_hash = user["password_hash"]
            if verify_password(password_hash, password):
                return user


async def init_db(app):
    dsn = construct_db_url()
    pool = await create_engine(dsn)
    app["db_pool"] = pool
    return pool


async def close_pg(app):
    app["db_pool"].close()
    await app["db_pool"].wait_closed()
    del app["db_pool"]


def construct_db_url():
    DSN = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.db_user, config.db_pass, config.db_host, config.db_port, config.db_name
    )
    return DSN
