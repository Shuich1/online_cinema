from flask import Flask, request
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from werkzeug.exceptions import HTTPException

from .api.v1 import auth, roles
from .core.config import settings
from .services.database import db
from .services.tracer import configure_tracer
from .utils.commands import commands
from .utils.error_handler import handle_exception
from .utils.extensions import jwt, migrate, security

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = settings.SECURITY_TOKEN_AUTHENTICATION_HEADER
app.config['SECURITY_PASSWORD_SALT'] = settings.SECURITY_PASSWORD_SALT

app.register_blueprint(auth.bp)
app.register_blueprint(roles.bp)
app.register_blueprint(commands)

app.register_error_handler(HTTPException, handle_exception)

# Tracer configuration
if settings.tracer.TRACER_ENABLED:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)

    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('request id is required')
        tracer = trace.get_tracer(__name__)
        span = tracer.start_span('auth')
        span.set_attribute('http.request_id', request_id)
        span.end()

# Database initialisation
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    app.logger.info('initialised database.')
    db.create_all()
    security.init_app(app)
    jwt.init_app(app)
