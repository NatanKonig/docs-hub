from functools import lru_cache

from decouple import config


class Settings:
    PRODUCTION: bool = config("PRODUCTION", default=False, cast=bool)
    JWT_SECRET: str = config("JWT_SECRET")
    JWT_EXPIRES_IN_HOURS: int = config(
        "JWT_EXPIRES_IN_HOURS",
        default=12,
        cast=int,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
