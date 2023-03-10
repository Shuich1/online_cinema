import datetime
import uuid

from flask_security import UserMixin
from sqlalchemy import UniqueConstraint
from ..services.database import db
from ..core.config import db_config
from .user_roles import roles_users


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = (
            UniqueConstraint('id', 'email'),
            {
                    'postgresql_partition_by': 'RANGE (email)',
                    'schema': db_config.db
            }

    )

    id: uuid
    email: str
    password: str
    active: bool
    created: datetime.datetime
    updated: datetime.datetime

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    email = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('user', lazy='dynamic')
    )
    auth_history = db.relationship('AuthHistory', backref='user')
    social_account = db.relationship("SocialAccount", backref="user")

    def __repr__(self):
        return f'<User {self.id}:{self.email}>'
