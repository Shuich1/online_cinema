from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(String(255), primary_key=True)
    login = Column(String(255), unique=True)
    password = Column(String(255))
    created = Column(DateTime())
    updated = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    auth_id = Column(String(255), ForeignKey("auth_history.id"))
    auth = relationship("AuthHistory", back_populates="user")


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(String(255), primary_key=True)
    name = Column(String(80), unique=True)
    created = Column(DateTime())


class AuthHistory(Base):
    __tablename__ = 'auth_history'
    id = Column(String(255), primary_key=True)
    user_id = relationship('User', back_populates='auth_history')
    user_agent = Column(String(255))
    auth_data = Column(DateTime())
    created = Column(DateTime())


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(String(255), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))
    created = Column(DateTime())
    updated = Column(DateTime())
