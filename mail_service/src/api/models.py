from sqlalchemy.dialects.postgresql import UUID
import uuid

from . import db


class Temp(db.Model):
    __tablename__ = "templates"

    id = db.Column(
        str(UUID(as_uuid=True)),
        db.String,
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String())
    text = db.Column(db.String())
