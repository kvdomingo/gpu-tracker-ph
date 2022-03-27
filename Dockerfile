FROM python:3.9-bullseye as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /backend

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

FROM base as dev

WORKDIR /backend

ENTRYPOINT gunicorn wsgi -b 0.0.0.0:5000 -w 4 --log-file - --capture-output --reload
