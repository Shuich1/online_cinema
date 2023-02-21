from gevent import monkey
from src import create_app


monkey.patch_all()
app = create_app()