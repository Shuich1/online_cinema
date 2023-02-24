from flask import Flask
from werkzeug.exceptions import HTTPException

from .api.v1 import auth, roles
from .core.config import settings
from .services.database import db
from .utils.extensions import jwt, security, migrate
from .utils.super_user import bp
from .utils.error_handler import handle_exception


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = settings.SECURITY_TOKEN_AUTHENTICATION_HEADER
    app.config['SECURITY_PASSWORD_SALT'] = settings.SECURITY_PASSWORD_SALT

    app.register_blueprint(auth.bp)
    app.register_blueprint(roles.bp)
    app.register_blueprint(bp)

    app.register_error_handler(HTTPException, handle_exception)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.logger.info('initialised database.')
        db.create_all()
        security.init_app(app)
        jwt.init_app(app)

    return app
