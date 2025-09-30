from pathlib import Path

from authx import AuthX, AuthXConfig
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str = "<DO NOT USE THIS IN PRODUCTION>"
    DEBUG: bool = False

    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite"


settings = Settings()

auth = AuthX(
    AuthXConfig(
        JWT_ALGORITHM="HS256",
        JWT_SECRET_KEY=settings.SECRET_KEY,
        JWT_TOKEN_LOCATION=["headers"],
    )
)
