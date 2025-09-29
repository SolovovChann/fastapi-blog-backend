from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import auth, settings
from core.database import create_tables
from core.views import router


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(debug=settings.DEBUG, lifespan=fastapi_lifespan)
app.include_router(router)

auth.handle_errors(app)


if __name__ == "__main__":
    uvicorn.run(app)
