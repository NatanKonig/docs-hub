# syntax=docker/dockerfile:1

FROM python:3.13-alpine AS builder

ENV TZ=America/Sao_Paulo
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

WORKDIR /code

RUN apk update && \
    apk add --no-cache \
    musl-dev \
    libffi-dev \
    build-base \
    libressl-dev \
    tzdata \
    curl && \
    rm -rf /var/cache/apk/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock* /code/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Estágio de Desenvolvimento ----
FROM python:3.13-alpine AS development

ENV TZ=America/Sao_Paulo
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/code

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

WORKDIR /code

RUN apk update && \
    apk add --no-cache \
    musl-dev \
    libffi-dev \
    libressl-dev \
    curl && \
    rm -rf /var/cache/apk/*

COPY --from=builder /code/.venv /code/.venv

COPY . /code

EXPOSE 8080

CMD ["uvicorn", "app.main:application", "--reload", "--host", "0.0.0.0", "--port", "8080"]

# ---- Estágio de Produção ----
FROM python:3.13-alpine AS production

ENV TZ=America/Sao_Paulo
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

WORKDIR /code

RUN apk update && \
    apk add --no-cache \
    libffi \
    libressl && \
    rm -rf /var/cache/apk/*

COPY --from=builder /code/.venv /code/.venv

COPY . /code

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app app && \
    chown -R app:app /code

USER app

EXPOSE 8080

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]