import uvicorn
from fastapi import FastAPI

from core.config import settings


app = FastAPI(debug=settings.DEBUG)


if __name__ == "__main__":
    uvicorn.run(app)
