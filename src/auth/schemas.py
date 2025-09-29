from pydantic import BaseModel

from auth.models import UserRole


class BaseUser(BaseModel):
    username: str
    full_name: str | None
    role: UserRole


class UserDelete(BaseModel):
    id: int


class User(BaseUser, UserDelete): ...


class Credentials(BaseModel):
    username: str
    password: str


class RegisterData(BaseModel):
    username: str
    password: str


class RefreshData(BaseModel):
    refresh_token: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
