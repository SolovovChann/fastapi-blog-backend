from pydantic import BaseModel, EmailStr

from auth.models import UserRole


class BaseUser(BaseModel):
    email: EmailStr
    full_name: str | None
    role: UserRole


class UserDelete(BaseModel):
    id: int


class User(BaseUser, UserDelete): ...


class Credentials(BaseModel):
    email: EmailStr
    password: str


class RegisterData(BaseModel):
    email: EmailStr
    password: str


class RefreshData(BaseModel):
    refresh_token: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class SetRole(BaseModel):
    user_email: EmailStr
    role: UserRole
