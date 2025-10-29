FROM python:3.13-slim AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_VERSION=0.9.5
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

WORKDIR /app

FROM base AS build

WORKDIR /tmp

COPY pyproject.toml uv.lock ./

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

# hadolint ignore=DL4006
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl

ADD https://astral.sh/uv/${UV_VERSION}/install.sh install-uv.sh

SHELL [ "/bin/sh", "-eu", "-c" ]
RUN chmod +x /tmp/install-uv.sh && \
    /tmp/install-uv.sh && \
    uv export --format requirements-txt --no-dev --output-file requirements.txt

WORKDIR /app

ENTRYPOINT [ "/bin/bash", "-euxo", "pipefail", "-c" ]
RUN python -m venv .venv && \
    ./.venv/bin/pip install -r /tmp/requirements.txt

FROM oven/bun:1-alpine AS web-build

WORKDIR /tmp

COPY ./ui/ ./

SHELL [ "/bin/sh", "-eu", "-c" ]
# hadolint ignore=DL4006
RUN bun install && bun run build

FROM base AS prod

WORKDIR /app

SHELL [ "/bin/bash", "-euxo", "pipefail", "-c" ]

COPY ./api ./
COPY --from=build /app/.venv ./.venv/
COPY --from=web-build /tmp/build ./static/

ENTRYPOINT [ "/app/.venv/bin/fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--app", "app", "app/app.py" ]
