from flask_jwt_extended import JWTManager
from flask_security import SQLAlchemyUserDatastore, Security


from .models import db, User, Role


jwt = JWTManager()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
