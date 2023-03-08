import datetime
import uuid
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from dataclasses import dataclass

from src.services.database import db
from src.core.config import db_config


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = (
            UniqueConstraint('id', 'user_device_type'),
            ForeignKeyConstraint(['user_id', 'email'],
                                 [f'{db_config.db}.user.id', f'{db_config.db}.user.email']),
            {
                    'postgresql_partition_by': 'LIST (user_device_type)',
                    'schema': db_config.db
            }

    )

    id: uuid
    user_id: str
    email: str
    user_agent: str
    host: str
    auth_date: datetime.datetime
    user_device_type: str

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = db.Column(db.UUID(as_uuid=True))
    email = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))
    host = db.Column(db.String(255))
    auth_date = db.Column(db.DateTime)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.auth_date}>'
