import aioredis

from .config import REDIS


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((REDIS["HOST"], REDIS["PORT"]))
    app["redis_pool"] = pool
    return pool


async def set_ttl(redis_pool, key, seconds):
    await redis_pool.expire(key, seconds)


async def save_pair(redis_pool, key, value):
    await redis_pool.set(key, value)


async def del_pair(redis_pool, key):
    await redis_pool.delete(key)


async def check_key_redis(redis_pool, key):
    return await redis_pool.exists(key)
