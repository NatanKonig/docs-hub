from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema


class GoogleUserDataOutput(BaseSchema):
    email: EmailStr = Field(description="Email do usuário autenticado pelo Google")
    display_name: str = Field(description="Nome completo do usuário")
    picture: str = Field(description="URL da foto de perfil do usuário")
    provider: str = Field(description="Provedor de autenticação (google)")


class AuthTokenOutput(BaseSchema):
    access_token: str = Field(description="Token JWT para autenticação nas requisições")
    token_type: str = Field(
        default="bearer",
        description="Tipo do token (sempre 'bearer')",
    )
    expires_in: int = Field(description="Tempo de expiração do token em segundos")


class LoginSuccessOutput(BaseSchema):
    user: GoogleUserDataOutput = Field(description="Dados do usuário autenticado")
    token: AuthTokenOutput = Field(description="Token de acesso gerado")
