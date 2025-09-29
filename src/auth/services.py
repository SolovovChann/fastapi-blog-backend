import bcrypt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import RegisterData


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def password_is_valid(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    statement = select(User).filter(User.username == username)
    result: Result = await session.execute(statement)
    user = result.scalars().first()

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def register_new_user(session: AsyncSession, data: RegisterData) -> User:
    data_as_dict = data.model_dump()
    password: str = data_as_dict.pop("password")

    user = User(**data_as_dict, password=hash_password(password).decode())

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
