import redis

from flask_jwt_extended import JWTManager
from flask_security import SQLAlchemyUserDatastore, Security


from .models import db, User, Role


jwt = JWTManager()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

jwt_redis_refresh_tokens = redis.StrictRedis(
    host="localhost", port=6379, db=1, decode_responses=True
)
