from sqlalchemy.dialects.postgresql import UUID
import uuid

from . import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(
        str(UUID(as_uuid=True)),
        db.String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    request_timestamp = db.Column(db.DateTime)
    service = db.Column(db.String())
    url = db.Column(db.String())
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.DateTime)
