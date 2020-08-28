from celery import Celery
from api.models import Event

celery_app = Celery("celery", broker="amqp://guest:guest@rabbit/")


@celery_app.task(name="create-event")
async def send_task(**params):
    await Event.create(**params)
