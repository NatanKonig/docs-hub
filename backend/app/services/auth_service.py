from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO

from app.core.settings.settings import settings
from app.schemas.auth import GoogleUserDataOutput


class AuthService:
    def __init__(self) -> None:
        self.google_sso = GoogleSSO(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            allow_insecure_http=True,
        )

    async def get_google_login_redirect(self) -> RedirectResponse:
        async with self.google_sso:
            return await self.google_sso.get_login_redirect()

    async def handle_google_callback(self, request: Request) -> GoogleUserDataOutput:
        async with self.google_sso:
            user = await self.google_sso.verify_and_process(request)

        # 1. Verificar se o usuário existe no banco
        # 2. Criar se não existir
        # 3. Gerar um token JWT da sua aplicação

        return GoogleUserDataOutput(
            email=user.email,
            display_name=user.display_name,
            picture=user.picture,
            provider=user.provider,
        )
