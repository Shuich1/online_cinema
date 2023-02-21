import datetime
from dataclasses import dataclass
import uuid

from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # TODO: при использовании Postgres
    # db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
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

    id: str
    name: str
    created: datetime.datetime

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime(), default=datetime.datetime.now())


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id: str
    user_id: str
    user_agent: str
    host: str
    auth_data: datetime.datetime
    created: datetime.datetime

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    user_agent = db.Column(db.String(255))
    host = db.Column(db.String(255))
    auth_data = db.Column(db.DateTime())
    created = db.Column(db.DateTime(), default=datetime.datetime.now())


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = db.Column('user_id', db.String(36), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.String(36), db.ForeignKey('role.id'))
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
