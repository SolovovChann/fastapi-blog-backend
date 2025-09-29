import uvicorn
from fastapi import FastAPI

from core.config import auth, settings


app = FastAPI(debug=settings.DEBUG)

auth.handle_errors(app)


if __name__ == "__main__":
    uvicorn.run(app)
