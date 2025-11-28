import logging
import os

from app.api.routers import api_router
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination

from app.core.settings.settings import settings


def _setup_logging() -> None:
    level = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    fmt = os.getenv("APP_LOG_FORMAT", "%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))

    app_logger = logging.getLogger("app.request")
    app_logger.setLevel(level)
    app_logger.handlers = [handler]
    app_logger.propagate = False


def create_app() -> FastAPI:
    _setup_logging()

    fast_api = FastAPI(
        title="Docs Hub API",
        description="Docs Hub API documentation",
        version="1.0.0",
        docs_url="/docs" if not settings.PRODUCTION else None,
        openapi_url="/openapi.json" if not settings.PRODUCTION else None,
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
        },
    )

    fast_api.openapi_schema = None

    def custom_openapi() -> dict:
        if fast_api.openapi_schema:
            return fast_api.openapi_schema

        openapi_schema = get_openapi(
            title=fast_api.title,
            version=fast_api.version,
            description=fast_api.description,
            routes=fast_api.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Insira apenas o token JWT (sem Bearer)",
            },
        }

        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                if method.lower() != "options":
                    openapi_schema["paths"][path][method]["security"] = [
                        {"BearerAuth": []},
                    ]

        fast_api.openapi_schema = openapi_schema
        return fast_api.openapi_schema

    fast_api.openapi = custom_openapi

    fast_api.include_router(
        api_router,
        prefix=settings.PREFIX,
    )

    add_pagination(fast_api)

    return fast_api
