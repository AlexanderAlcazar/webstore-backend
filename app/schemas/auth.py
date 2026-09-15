from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

Email = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    ),
]
Password = Annotated[str, StringConstraints(min_length=1, max_length=255)]


class RegisterRequest(BaseModel):
    email: Email
    password: Password


class LoginRequest(BaseModel):
    email: Email
    password: Password


class AuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
