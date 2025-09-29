from fastapi import FastAPI

from core.config import settings


app = FastAPI(debug=settings.DEBUG)
