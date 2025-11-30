from typing import Annotated

from fastapi import Depends
from google.cloud.firestore_v1 import Client

from app.core.database import get_firestore_client
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def get_auth_repository(
    firestore_client: Annotated[Client, Depends(get_firestore_client)],
) -> AuthRepository:
    return AuthRepository(firestore_client)


def get_auth_service(
    auth_repository: Annotated[AuthRepository, Depends(get_auth_repository)],
) -> AuthService:
    return AuthService(auth_repository)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
