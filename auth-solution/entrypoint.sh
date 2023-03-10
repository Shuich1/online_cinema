flask --app src.wsgi:app db migrate
flask --app src.wsgi:app db upgrade
flask --app src.wsgi:app commands createsuperuser $FLASK_ADMIN_MAIL $FLASK_ADMIN_PASS
gunicorn src.wsgi:app --bind $FLASK_HOST:$FLASK_PORT --workers $FLASK_WORKERS --worker-class gevent