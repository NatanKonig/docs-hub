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

    GOOGLE_CLIENT_ID: str = config("GOOGLE_CLIENT_ID", default="")
    GOOGLE_CLIENT_SECRET: str = config("GOOGLE_CLIENT_SECRET", default="")
    GOOGLE_REDIRECT_URI: str = config(
        "GOOGLE_REDIRECT_URI",
        default="http://localhost:8080/auth/google/callback",
    )

    FIRESTORE_CREDENTIALS_PATH: str = config(
        "FIRESTORE_CREDENTIALS_PATH",
        default="",
    )
    FIRESTORE_PROJECT_ID: str = config("FIRESTORE_PROJECT_ID", default="")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
