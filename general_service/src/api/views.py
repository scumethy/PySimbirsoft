import json

import aioredis
import uuid
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
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


@router.post("/account/login")
async def login(username: str, password: str):
    us_resp = await user_service.login(username, password)

    response_content = dict(status=us_resp["status"], message=us_resp["message"])
    response = JSONResponse(content=response_content)
    response.set_cookie(key="access", value=us_resp["access"])
    response.set_cookie(key="refresh", value=us_resp["refresh"])
    return response


@router.post("/user/info")
async def userinfo(request: Request):
    access_token = dict(request.cookies).get("access")
    us_resp = await user_service.userinfo(access_token)
    return us_resp


@router.get("/account/logout")
async def logout(request: Request):
    cookies = dict(request.cookies)
    access_token = cookies.get("access")
    refresh_token_id = cookies.get("refresh")
    us_resp = await user_service.logout(access_token, refresh_token_id)
    return us_resp


@router.post("/account/refreshtokens")
async def refresh_tokens(request: Request):
    # get tokens from user cookies
    cookies = dict(request.cookies)
    access_token = cookies.get("access")
    refresh_token_id = cookies.get("refresh")
    # request to user service for create new tokens
    us_resp = await user_service.refreshtokens(access_token, refresh_token_id)

    # create response and put cookies
    response_content = dict(status=us_resp["status"], message=us_resp["message"])
    response = JSONResponse(content=response_content)
    response.set_cookie(key="access", value=us_resp["access"])
    response.set_cookie(key="refresh", value=us_resp["refresh"])
    return response


def init_app(app):
    app.include_router(router)
