FROM python:3.9-bullseye as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /backend

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

FROM base as dev

WORKDIR /backend

RUN poetry install --no-interaction --no-ansi

ENTRYPOINT gunicorn wsgi -b 0.0.0.0:5000 -w 4 --log-file - --capture-output --reload

FROM node:16-alpine as build

WORKDIR /web

COPY ./web/app/package.json ./web/app/yarn.lock ./

RUN yarn install --prod

COPY ./web/app ./

RUN yarn build

FROM base as prod

WORKDIR /backend

RUN poetry install --no-interaction --no-ansi --no-dev

COPY ./gpu_tracker_ph/ ./gpu_tracker_ph/
COPY ./*.py ./
COPY --from=build /web/build ./web/app

EXPOSE $PORT

ENTRYPOINT gunicorn wsgi -b 0.0.0.0:$PORT -w 2 --log-file -
