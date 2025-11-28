from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()

@router.get("/google/login")
async def google_login(
    service: AuthService = Depends(get_auth_service),
) -> RedirectResponse:
    return await service.get_google_login_redirect()


@router.get("/google/callback")
async def google_callback(
    request: Request,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    return await service.handle_google_callback(request)
