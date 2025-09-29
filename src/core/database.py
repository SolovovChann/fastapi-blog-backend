from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings


engine = create_async_engine(settings.DB_URL, echo=settings.DEBUG)

session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)
