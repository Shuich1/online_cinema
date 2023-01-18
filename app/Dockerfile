# Укажите необходимую версию python
FROM python:3.10

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /opt/app

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

# Скопируйте в контейнер файлы, которые редко меняются
COPY requirements.txt requirements.txt
COPY ./uwsgi/uwsgi.ini uwsgi.ini

# Установите зависимости
RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/movies/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt \
     && apt-get update  \
     && apt-get install -y netcat

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . .

# Укажите порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]