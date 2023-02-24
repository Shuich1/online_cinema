import datetime
import uuid
from dataclasses import dataclass

from flask_security import RoleMixin
from src.services.database import db


@dataclass
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id: uuid
    name: str
    created: datetime.datetime

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.now())
