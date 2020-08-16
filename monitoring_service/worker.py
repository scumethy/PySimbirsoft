from celery import Celery
from api.models import Event

celery_app = Celery("celery", broker="amqp://guest:guest@rabbit/")


@celery_app.task(name="create-event")
async def send_task(self, **params):
    try:
        await Event.create(**params)
    except Exception as exc:
        raise self.retry(exc=exc, max_retries=3)
