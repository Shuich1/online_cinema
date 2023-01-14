import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
