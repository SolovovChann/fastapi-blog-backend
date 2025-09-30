import bcrypt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import RegisterData


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def password_is_valid(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    statement = select(User).filter(User.email == email)
    result: Result = await session.execute(statement)
    user = result.scalars().first()

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def register_new_user(session: AsyncSession, data: RegisterData) -> User:
    data_as_dict = data.model_dump()
    password: str = data_as_dict.pop("password")

    user = User(**data_as_dict, password=hash_password(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
