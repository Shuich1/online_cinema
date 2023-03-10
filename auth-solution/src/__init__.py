from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from sqlalchemy import text
from werkzeug.exceptions import HTTPException

from .api.v1 import auth, roles
from .core.config import settings, db_config
from .services.database import db
from .utils.commands import commands
from .utils.error_handler import handle_exception
from .utils.extensions import migrate, security
from .utils.trace_functions import traced
from .services.redis import jwt_redis_blocklist


def create_app():
    app = Flask(__name__)

    @app.route("/healthcheck")
    def healthcheck():
        return jsonify("Service healthy"), HTTPStatus.OK

    # App configuration
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = settings.SECURITY_TOKEN_AUTHENTICATION_HEADER
    app.config['SECURITY_PASSWORD_SALT'] = settings.SECURITY_PASSWORD_SALT
    app.config['HOST_MOVIES_API'] = settings.host_fast_api
    app.config['OAUTH_CREDENTIALS'] = {
        'yandex': {
            'id': settings.yandex_id,
            'secret': settings.yandex_secret,
        },
        'vk': {
            'id': settings.vk_id,
            'secret': settings.vk_secret,
        }
    }

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    @traced()
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)

        return token_in_redis is not None

    app.register_blueprint(auth.bp)
    app.register_blueprint(roles.bp)
    app.register_blueprint(commands)

    app.register_error_handler(HTTPException, handle_exception)

    # Tracer configuration
    if settings.tracer.TRACER_ENABLED:
        FlaskInstrumentor().instrument_app(app, excluded_urls="healthcheck")

        @app.before_request
        def before_request():
            request_id = request.headers.get('X-Request-Id')

            if not request_id:
                raise RuntimeError('request id is required')

            if request_id != "healthcheck":
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span('request-id-checking') as span:
                    span.set_attribute('http.request_id', request_id)

    # Database initialisation
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.session.execute(text(f'CREATE SCHEMA IF NOT EXISTS {db_config.db};'))
        db.session.commit()
        app.logger.info('initialised database.')
        security.init_app(app)
        jwt.init_app(app)

    return app
