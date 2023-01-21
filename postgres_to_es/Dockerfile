FROM python:3.10

WORKDIR /opt/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY .. .

ENTRYPOINT ["python", "main_process.py"]