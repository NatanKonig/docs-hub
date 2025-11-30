from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.core.dependencies import AuthServiceDependency
from app.schemas.auth import LoginSuccessOutput

router = APIRouter()


@router.get("/google/login")
async def google_login(
    auth_service: AuthServiceDependency,
) -> RedirectResponse:
    return await auth_service.get_google_login_redirect()


@router.get("/google/callback")
async def google_callback(
    request: Request,
    auth_service: AuthServiceDependency,
) -> LoginSuccessOutput:
    return await auth_service.handle_google_callback(request)
