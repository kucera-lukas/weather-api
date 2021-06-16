FROM python:3.9-slim

MAINTAINER lukas.kucera.g@protonmail.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN pip install psycopg2-binary \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . /app/

EXPOSE $PORT
CMD gunicorn weather_api.project.wsgi:application --bind 0.0.0.0:$PORT
