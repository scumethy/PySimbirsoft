import json

from fastapi import APIRouter
from pydantic import BaseModel
from aio_pika import connect, Message

from src import config
from .models import Temp

router = APIRouter()


@router.get("/api/temp/{id}")
async def get_temp(id: str):
    temp = await Temp.get_or_404(id)
    return temp.to_dict()


class TempModel(BaseModel):
    name: str
    text: str


class MailModel(BaseModel):
    temp_id: str
    recipient: str
    params: dict


@router.post("/api/temp")
async def add_temp(temp: TempModel):
    rv = await Temp.create(name=temp.name, text=temp.text)
    return rv.to_dict()


@router.delete("/api/temp/{id}")
async def delete_temp(id: str):
    temp = await Temp.get_or_404(id)
    await temp.delete()
    return dict(id=id)


async def send_rabbitmq(msg):
    connection = await connect(config.RABBITMQ_DSN)

    channel = await connection.channel()
    await channel.default_exchange.publish(
        Message(json.dumps(msg).encode("utf-8")), routing_key="mail"
    )

    await connection.close()


@router.post("/api/mail")
async def mailing(mail: MailModel):
    temp = await Temp.get_or_404(mail.temp_id)
    message_text = temp.text.format(**mail.params)
    message_data = {"text": message_text, "recipient": mail.recipient}
    await send_rabbitmq(message_data)

    return {"message": "Task added"}


def init_app(app):
    app.include_router(router)
