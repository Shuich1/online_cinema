import datetime
import uuid
from dataclasses import dataclass

from src.services.database import db


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id: uuid
    user_id: str
    user_agent: str
    host: str
    auth_data: datetime.datetime
    created: datetime.datetime

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('user.id'))
    user_agent = db.Column(db.String(255))
    host = db.Column(db.String(255))
    auth_data = db.Column(db.DateTime)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
