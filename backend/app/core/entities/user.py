from typing import Any

from pydantic import Field
from app.schemas.base import BaseSchema


class User(BaseSchema):
    email: str
    display_name: str
    picture: str
    provider: str
    user_id: str
