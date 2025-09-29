from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str = "<DO NOT USE THIS IN PRODUCTION>"
    # TODO Now debug is True by default. Change to FALSE on commit
    DEBUG: bool = True

    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite"


settings = Settings()
