import json

from fastapi import APIRouter, Depends, Response
from aio_pika import connect, Message

from src.api import goods_service, user_service, mail_service
from src.api.schemas import ItemModel
from src.api.views.users import get_user_by_token
from src import config

goods_router = APIRouter()


# TODO: !- change all routes parameters format to pydantic models -!
@goods_router.post("/items/add")
async def add_item(item: ItemModel, user_id: str = Depends(get_user_by_token)):
    # request to goods service with item as dict if user verified
    item_data = item.dict()
    item_data.update({"user_id": user_id})
    resp = await goods_service.add_item(item_data)
    return resp


@goods_router.put("/items/update/{item_id}")
async def update_item(
        item_id, item: ItemModel, user_id: str = Depends(get_user_by_token)
):
    item_data = item.dict()
    item_data.update({"user_id": user_id})
    resp = await goods_service.update_item(item_data, item_id)
    return resp


@goods_router.delete("/items/delete/{item_id}")
async def delete_item(item_id, user_id: str = Depends(get_user_by_token)):
    resp = await goods_service.delete_item(item_id)
    return resp


# TODO: make connection in initializator
async def send_rabbitmq(msg):
    connection = await connect(config.RABBITMQ_DSN)

    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(json.dumps(msg).encode("utf-8")), routing_key="mail"
    )

    await connection.close()


@goods_router.get("/items/show/{item_id}")
async def get_full_item(item_id):
    resp = await goods_service.get_full_item(item_id)

    # TODO: use message templates from mail service
    # send email notification message every 10 view
    views_count = resp.get("views")

    if views_count % 10 == 0:
        template = "Your item has been viewed {count} times"
        message_text = template.format(count=views_count)

        # get author email from user service
        author_user_id = resp.get("user_id")
        us_resp = await user_service.userinfo(author_user_id)
        author = us_resp.get("user")
        author_email = author.get("username")

        # send message
        message_data = {
            "text": message_text,
            "recipient": author_email,
        }
        await send_rabbitmq(message_data)

    return resp


@goods_router.get("/items/show/short/{item_id}")
async def get_short_item(item_id):
    resp = await goods_service.get_short_item(item_id)
    return resp


@goods_router.get("/tags")
async def get_all_tags():
    resp = await goods_service.get_all_tags()
    return resp
