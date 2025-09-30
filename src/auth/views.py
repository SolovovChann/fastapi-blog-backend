from authx import RequestToken
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.models import User
from auth.schemas import (
    BaseUser,
    Credentials,
    RefreshData,
    RegisterData,
    SetRole,
    Tokens,
)
from core.config import auth
from core.database import get_scoped_session


router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/login")
async def login(
    credentials: Credentials,
    session: AsyncSession = Depends(get_scoped_session),
) -> Tokens:
    user = await services.get_user_by_email(session, credentials.email)

    if user is None:
        detail = f"User with email '{credentials.email}' is not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail)

    if not services.password_is_valid(
        credentials.password,
        user.password.encode(),
    ):
        detail = "Invalid email or password"
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail)

    access_token = auth.create_access_token(str(user.id))
    refresh_token = auth.create_refresh_token(str(user.id))

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/register")
async def register(
    data: RegisterData,
    session: AsyncSession = Depends(get_scoped_session),
):
    existing_user = await services.get_user_by_email(
        session,
        data.email,
    )

    if existing_user is not None:
        detail = f"User with email '{data.email}' already exists"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail)

    user = await services.register_new_user(session, data)
    access_token = auth.create_access_token(str(user.id))
    refresh_token = auth.create_refresh_token(str(user.id))

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh_token(request: Request, data: RefreshData) -> Tokens:
    try:
        try:
            refresh_payload = await auth.refresh_token_required(request)
        except Exception as exc:
            if not data or not data.refresh_token:
                raise exc

            request_token = RequestToken(
                token=data.refresh_token,
                type="refresh",
                location=auth.config.JWT_TOKEN_LOCATION[0],
            )
            refresh_payload = auth.verify_token(
                request_token,
                verify_type=True,
            )

        access_token = auth.create_access_token(refresh_payload.sub)
        refresh_token = auth.create_refresh_token(refresh_payload.sub)

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    except Exception as exc:
        detail = {"error": str(exc), "type": type(exc).__name__}
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail)


@auth.set_subject_getter
async def _get_user_from_uid(uid: str, whatever=None) -> User:
    # NOTE auth.set_subject_getter does not support async functions.
    # You should use it with await

    try:
        user_id = int(uid)
    except ValueError as exc:
        detail = "Invalid token, please login again"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail) from exc

    session_maker = get_scoped_session()
    user = await services.get_user_by_id(session_maker(), user_id)

    if user is None:
        detail = f"User with ID '{user_id}' is not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail)

    return user


@router.get("/me")
async def get_authenticated_user_profile(
    user: User = Depends(auth.get_current_subject),
) -> BaseUser:
    user = await user
    return BaseUser(
        email=user.email,
        full_name=user.full_name,
        role=user.role,
    )


@router.post("/set-role")
async def set_user_role(
    data: SetRole,
    user: User = Depends(auth.get_current_subject),
    session: AsyncSession = Depends(get_scoped_session),
) -> None:
    services.is_admin_or_raise_401(await user)

    target = await services.get_user_by_email(session, data.user_email)

    if target is None:
        detail = f"User with email '{data.user_email}' is not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail)

    await services.set_user_role(session, target, data.role)
