import uuid
from datetime import datetime

from src.services.database import db


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column('user_id', db.UUID(as_uuid=True), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.UUID(as_uuid=True), db.ForeignKey('role.id'))
    created = db.Column(db.DateTime(), default=datetime.datetime.now())
    updated = db.Column(db.DateTime(), default=datetime.datetime.now())