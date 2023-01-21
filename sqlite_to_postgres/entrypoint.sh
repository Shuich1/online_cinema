while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
      echo "Waiting for database..."
done
python3 main.py