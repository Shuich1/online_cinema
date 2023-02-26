FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT [ "sh", "entrypoint.sh" ]