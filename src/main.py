import uvicorn
from fastapi import FastAPI

from core.config import auth, settings
from core.views import router


app = FastAPI(debug=settings.DEBUG)
app.include_router(router)

auth.handle_errors(app)


if __name__ == "__main__":
    uvicorn.run(app)
