from flask import Flask

from . import auth
from . import roles
from .extensions import security, jwt
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '45b99b19b1e840b79bff2d3227d3915d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
    app.config['SECURITY_PASSWORD_SALT'] = 'asasdasd'

    app.register_blueprint(auth.bp)
    app.register_blueprint(roles.bp)

    db.init_app(app)
    with app.app_context():
        app.logger.info('initialised database.')
        db.create_all()

    security.init_app(app)
    jwt.init_app(app)

    return app
