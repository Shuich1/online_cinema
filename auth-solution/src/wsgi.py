from gevent import monkey

monkey.patch_all()
from src import create_app
from src.core.config import settings
from src.services.tracer import configure_tracer

app = create_app()

# Prevents unexpected behavior (failure of CLI commands) when configuring tracer inside a create app function
if settings.tracer.TRACER_ENABLED:
    configure_tracer()
