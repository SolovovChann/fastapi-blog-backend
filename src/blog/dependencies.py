from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from blog import services
from blog.models import Post
from core.database import get_scoped_session


async def get_post_by_id(
    post_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_scoped_session),
) -> Post:
    post = await services.get_post_by_id(session, post_id)

    if post is None:
        details = f"Post with ID={post_id} is not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, details)

    return post
