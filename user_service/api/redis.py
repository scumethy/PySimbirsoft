import aioredis

from user_service.config import config


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((config.redis_host, config.redis_port))
    app["redis_pool"] = pool
    return pool


async def close_redis(app):
    app["redis_pool"].close()
    app["redis_pool"].wait_closed()
    del app["redis_pool"]


async def set_ttl(redis_pool, key, seconds):
    await redis_pool.expire(key, seconds)


async def save_pair(redis_pool, key, value):
    await redis_pool.set(key, value)


async def del_pair(redis_pool, key):
    await redis_pool.delete(key)


async def check_key_redis(redis_pool, key):
    return await redis_pool.exists(key)
