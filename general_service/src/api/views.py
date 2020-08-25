import json

import aioredis
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from aio_pika import connect, Message

# from aio_pika import connect, Message

from src import config
from src.api import user_service

# from .models import Temp

router = APIRouter()


@router.get("/account/create/confirm/{token}")
async def confirm(token: str):
    # get login from redis
    redis_pool = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT)
    )
    login = await redis_pool.get(token, encoding='utf-8')
    if login:
        reg_data = json.dumps(dict(login=login, confirmed=True))
        await redis_pool.set(token, reg_data)

    return {"status": 202, "message": "E-Mail confirmed"}


@router.post("/account/create/finish")
async def finish_reg(token: str, password: str):
    # get login from redis
    redis_pool = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT)
    )
    reg_data_json = await redis_pool.get(token, encoding='utf-8')
    reg_data = json.loads(reg_data_json)
    if reg_data["confirmed"]:
        resp = await user_service.reg(reg_data["login"], password)
    return resp


async def send_rabbitmq(msg):
    connection = await connect(config.RABBITMQ_DSN)

    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(json.dumps(msg).encode("utf-8")), routing_key="mail"
    )

    await connection.close()


@router.post("/account/create")
async def register(login: str):
    # generate uuid token
    reg_token = str(uuid.uuid4())

    # add to redis pair token:login
    redis_pool = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT)
    )
    await redis_pool.set(reg_token, login)
    redis_pool.close()
    await redis_pool.wait_closed()

    # send email message with token
    confirm_link = f"{config.USER_SERVICE_URL}/account/create/confirm/{reg_token}"

    message_data = {"text": confirm_link, "recipient": login}
    await send_rabbitmq(message_data)

    return {"status": 202, "confirm_link": confirm_link}


def init_app(app):
    app.include_router(router)
