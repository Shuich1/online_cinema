import datetime
import uuid
from dataclasses import dataclass

from flask_security import RoleMixin, UserMixin
from sqlalchemy.dialects.postgresql import UUID
from src.services.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary='roles_users',
        backref=db.backref('users', lazy='dynamic')
    )
    auth_history = db.relationship("AuthHistory", backref="user")

@dataclass
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id: uuid
    name: str
    created: datetime.datetime

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.now())


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id: uuid
    user_id: str
    user_agent: str
    host: str
    auth_data: datetime.datetime
    created: datetime.datetime

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('user.id'))
    user_agent = db.Column(db.String(255))
    host = db.Column(db.String(255))
    auth_data = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), default=datetime.datetime.now())


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column('user_id', db.UUID(as_uuid=True), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.UUID(as_uuid=True), db.ForeignKey('role.id'))
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
