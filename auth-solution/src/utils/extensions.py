from flask_jwt_extended import JWTManager
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.role import Role
from src.models.user import User
from src.services.database import db

jwt = JWTManager()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
