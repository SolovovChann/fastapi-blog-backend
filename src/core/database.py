from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
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
