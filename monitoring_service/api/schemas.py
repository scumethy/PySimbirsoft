from pydantic import BaseModel
from datetime import datetime


class EventModel(BaseModel):
    request_timestamp: datetime
    service: str
    url: str
    status_code: int
    response_time: float
