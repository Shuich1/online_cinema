from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from src import create_app

app = create_app()
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()