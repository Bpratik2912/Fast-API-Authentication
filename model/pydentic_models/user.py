from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """ to validate a user details. """

    user_name: str
    email: EmailStr
    password: str = Field(max_length=10)
    is_active: bool = True

    def validate(cls, value: Any) -> Self:
        pass


class UserToken(BaseModel):
    """ To map accesstoken for a validated user."""

    access_token: str
    refresh_token: str
    token_type: str


class UserPassword(User):
    """ to show a user details with password."""

    password: str
