from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings


engine = create_async_engine(settings.DB_URL, echo=settings.DEBUG)

session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for all ORM model classes"""

    pass


class Model(Base):
    """
    Abstract base class for all models.
    Provides autoincrement integer as ID
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def delete_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


def get_scoped_session():
    return async_scoped_session(
        session_factory=session_maker,
        scopefunc=current_task,
    )


@asynccontextmanager
async def session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
        await session.close()


@asynccontextmanager
async def scoped_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    session = get_scoped_session()
    yield session
    await session.close()
