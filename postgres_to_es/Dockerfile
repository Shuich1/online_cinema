FROM python:3.10

WORKDIR /opt/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY .. .

RUN ["chmod", "+x", "/opt/etl/run_etl.sh"]