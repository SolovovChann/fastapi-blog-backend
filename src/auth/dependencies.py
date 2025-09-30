from authx import TokenPayload
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.models import User
from core.config import auth
from core.database import get_scoped_session


async def get_user_by_JWT_token(
    request: Request,
    session: AsyncSession = Depends(get_scoped_session),
) -> User:
    """
    Due `AuthX.set_subject_getter` as the recommended way
    to get a user by JWT token works synchronously,
    use this workaround to call the user in asynchronous functions
    """

    try:
        token: TokenPayload = await auth._auth_required(request=request)
        user_id = int(token.sub)
    except ValueError as exc:
        detail = "Invalid token, please login again"
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail) from exc

    user = await services.get_user_by_id(session, user_id)

    if user is None:
        detail = f"User with ID '{user_id}' is not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail)

    return user
