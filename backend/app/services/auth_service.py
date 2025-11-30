from datetime import UTC, datetime, timedelta

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from jose import jwt

from app.core.entities.user import User
from app.core.settings.settings import settings
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import AuthTokenOutput, GoogleUserDataOutput, LoginSuccessOutput


class AuthService:
    def __init__(self, auth_repository: AuthRepository) -> None:
        self.auth_repository = auth_repository
        self.google_sso = GoogleSSO(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            allow_insecure_http=True,
        )

    async def get_google_login_redirect(self) -> RedirectResponse:
        async with self.google_sso:
            return await self.google_sso.get_login_redirect()

    async def handle_google_callback(self, request: Request) -> LoginSuccessOutput:
        async with self.google_sso:
            google_user = await self.google_sso.verify_and_process(request)

        user = self._find_or_create_user(
            email=google_user.email,
            display_name=google_user.display_name,
            picture=google_user.picture,
            provider=google_user.provider,
        )

        token = self._generate_access_token(user.user_id)

        return LoginSuccessOutput(
            user=GoogleUserDataOutput(
                email=user.email,
                display_name=user.display_name,
                picture=user.picture,
                provider=user.provider,
            ),
            token=token,
        )

    def _find_or_create_user(
        self,
        email: str,
        display_name: str,
        picture: str,
        provider: str,
    ) -> User:
        existing_user = self.auth_repository.find_user_by_email(email)

        if existing_user:
            return existing_user

        new_user = User(
            email=email,
            display_name=display_name,
            picture=picture,
            provider=provider,
        )

        return self.auth_repository.create_user(new_user)

    def _generate_access_token(self, user_id: str) -> AuthTokenOutput:
        expires_in_hours = settings.JWT_EXPIRES_IN_HOURS
        expiration_time = datetime.now(UTC) + timedelta(hours=expires_in_hours)

        payload = {
            "sub": user_id,
            "exp": expiration_time,
        }

        access_token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm="HS256",
        )

        return AuthTokenOutput(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in_hours * 3600,
        )
