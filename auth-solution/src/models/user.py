import datetime
import uuid

from flask_security import UserMixin
from src.services.database import db

from .user_roles import RolesUsers


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    roles = db.relationship(
        'Role',
        secondary='roles_users',
        backref=db.backref('users', lazy='dynamic')
    )
    auth_history = db.relationship("AuthHistory", backref="user")
