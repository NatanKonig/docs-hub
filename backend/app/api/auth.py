from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.schemas.auth import GoogleUserDataOutput
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.get("/google/login")
async def google_login(
    service: AuthServiceDep,
) -> RedirectResponse:
    return await service.get_google_login_redirect()


@router.get("/google/callback")
async def google_callback(
    request: Request,
    service: AuthServiceDep,
) -> GoogleUserDataOutput:
    return await service.handle_google_callback(request)
