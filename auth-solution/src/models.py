from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    # auth_id = Column(String(255), ForeignKey("auth_history.id"))
    # auth = relationship("AuthHistory", back_populates="user")


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    created = db.Column(db.DateTime())


# class AuthHistory(Base):
#     __tablename__ = 'auth_history'
#     id = Column(String(255), primary_key=True)
#     user_id = relationship('User', back_populates='auth_history')
#     user_agent = Column(String(255))
#     auth_data = Column(DateTime())
#     created = Column(DateTime())


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
