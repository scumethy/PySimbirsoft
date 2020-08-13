import aiosmtplib
from email.message import EmailMessage
from aio_pika import connect_robust, IncomingMessage
import json


async def on_message(message: IncomingMessage):
    message = json.loads(message.body.decode("utf-8"))

    em = EmailMessage()
    em["From"] = "root@localhost"
    em["To"] = message["recipient"]
    em["Subject"] = "testik"
    em.set_content(message["text"])

    await aiosmtplib.send(em, hostname="email", port=25)


async def listen(loop):
    connection = await connect_robust("amqp://guest:guest@rabbit/", loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue("mail")
    await queue.consume(on_message, no_ack=True)