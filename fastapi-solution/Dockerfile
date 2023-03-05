FROM python:3.9

WORKDIR /opt/fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

COPY . .

ENTRYPOINT [ "sh", "entrypoint.sh" ]