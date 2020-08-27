import json

import aioredis
import uuid

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from aio_pika import connect, Message

from src import config
from src.api import user_service

users_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")


async def get_user_by_token(token: str = Depends(oauth2_scheme)):
    print(token)
    if token:
        resp = await user_service.verify_user(token)
        if resp.get("status") == 205:
            return resp.get("user_id")


@users_router.post("/account/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    us_resp = await user_service.login(form_data.username, form_data.password)

    if us_resp.get("status") == 205:
        return {
            "access_token": us_resp["access"],
            "token_type": "bearer",
            "refresh_token": us_resp["refresh"],
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@users_router.get("/account/create/confirm/{token}")
async def confirm(token: str):
    # get login from redis
    redis_pool = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT)
    )
    login = await redis_pool.get(token, encoding="utf-8")
    if login:
        reg_data = json.dumps(dict(login=login, confirmed=True))
        await redis_pool.set(token, reg_data)

    return {"status": 202, "message": "E-Mail confirmed"}


@users_router.post("/account/create/finish")
async def finish_reg(token: str, password: str):
    redis_pool = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT)
    )
    reg_data_json = await redis_pool.get(token, encoding="utf-8")
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


@users_router.post("/account/create")
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


@users_router.post("/user/info")
async def userinfo(user_id: str):
    us_resp = await user_service.userinfo(user_id)
    return us_resp


@users_router.get("/account/logout")
async def logout(request: Request):
    cookies = dict(request.cookies)
    access_token = cookies.get("access")
    refresh_token_id = cookies.get("refresh")
    us_resp = await user_service.logout(access_token, refresh_token_id)
    return us_resp


@users_router.post("/account/refreshtokens")
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

# TODO: create unified errors in general service
