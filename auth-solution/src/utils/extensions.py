import redis
from flask_jwt_extended import JWTManager
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.models import Role, User
from src.services.database import db

jwt = JWTManager()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
