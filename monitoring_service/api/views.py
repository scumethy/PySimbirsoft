from fastapi import APIRouter

from worker import send_task
from .schemas import EventModel

router = APIRouter()


@router.post("/api/monitoring_service/event")
async def add_event(event: EventModel):
    await send_task.delay(**event.dict())


def init_app(app):
    app.include_router(router)
