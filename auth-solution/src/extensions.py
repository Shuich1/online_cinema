from flask import Flask
from flask_jwt_extended import JWTManager
from flask_security import SQLAlchemySessionUserDatastore, Security
# import redis

from db import db_session
from models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)

# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )


def init_security(app: Flask):
    Security(app, user_datastore)


def init_jwt_manager(app: Flask):
    JWTManager(app)
