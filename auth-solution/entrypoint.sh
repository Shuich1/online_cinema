flask --app src.wsgi:app commands create $FLASK_ADMIN_MAIL $FLASK_ADMIN_PASS
gunicorn src.wsgi:app --bind $FLASK_HOST:$FLASK_PORT --workers $FLASK_WORKERS --worker-class gevent