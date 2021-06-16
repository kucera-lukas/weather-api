FROM python:latest

MAINTAINER lukas.kucera.g@protonmail.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE $PORT
CMD gunicorn weather_api.project.wsgi:application --bind 0.0.0.0:$PORT
