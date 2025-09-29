from fastapi import APIRouter

from auth.views import router as auth_router
from blog.views import categories_router, posts_router


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(posts_router)
router.include_router(categories_router)
