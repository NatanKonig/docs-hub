from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client

from app.core.settings.settings import settings


@lru_cache
def get_firestore_client() -> Client:
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIRESTORE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(
            cred,
            {"projectId": settings.FIRESTORE_PROJECT_ID},
        )

    return firestore.client()
