import datetime
import uuid

from src.services.database import db
from src.core.config import db_config


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    __table_args__ = {'schema': db_config.db}

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    user_id = db.Column(
        'user_id',
        db.UUID(as_uuid=True),
        db.ForeignKey(f'{db_config.db}.user.id')
    )
    role_id = db.Column(
        'role_id',
        db.UUID(as_uuid=True),
        db.ForeignKey(f'{db_config.db}.role.id')
    )
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
