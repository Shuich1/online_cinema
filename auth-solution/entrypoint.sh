flask --app src.wsgi:app commands create $FLASK_ADMIN_MAIL $FLASK_ADMIN_PASS
flask --app src.wsgi:app db init
flask --app src.wsgi:app db migrate
flask --app src.wsgi:app db upgrade
gunicorn src.wsgi:app --bind $FLASK_HOST:$FLASK_PORT --workers $FLASK_WORKERS --worker-class gevent