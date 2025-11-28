# syntax=docker/dockerfile:1

# ---- Base comum para todos os estágios ----
FROM python:3.13-alpine AS base

ENV TZ=America/Sao_Paulo \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTEbackend=1 \
    PYTHONPATH=/backend

WORKDIR /backend

# ---- Builder: instala dependências ----
FROM base AS builder

ENV UV_COMPILE_BYTEbackend=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/venv"

RUN apk add --no-cache \
    musl-dev \
    libffi-dev \
    build-base \
    libressl-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock* ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---- Desenvolvimento: com hot-reload ----
FROM base AS development

RUN apk add --no-cache \
    libffi \
    libressl

# Copia o ambiente virtual para /venv (fora de /backend para não ser sobrescrito pelo volume)
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copia o código fonte (fallback se não houver volume)
COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:application", "--reload", "--host", "0.0.0.0", "--port", "8080"]

# ---- Produção: otimizada e segura ----
FROM base AS production

RUN apk add --no-cache \
    libffi \
    libressl && \
    addgroup -g 1000 app && \
    adduser -D -u 1000 -G app app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . .

RUN chown -R app:app /backend && \
    chown -R app:app /venv

USER app

EXPOSE 8080

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]