import datetime
import uuid
from dataclasses import dataclass

from flask_security import RoleMixin
from src.services.database import db
from src.core.config import db_config

from .user_roles import RolesUsers


@dataclass
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    __table_args__ = {"schema": db_config.db}

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
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    users = db.relationship(
            'User',
            secondary='roles_users',
            back_populates='role'
    )
