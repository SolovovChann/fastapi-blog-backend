from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_user_by_JWT_token
from auth.models import User
from auth.services import is_admin_or_raise_401
from blog import dependencies, services
from blog.models import Category, Post
from blog.schemas import Category as CategorySchema
from blog.schemas import CategoryCreate, CategoryUpdate, CategoryUpdatePartial
from blog.schemas import Post as PostSchema
from blog.schemas import PostCreate, PostUpdate, PostUpdatePartial
from core.database import get_scoped_session


posts_router = APIRouter(prefix="/posts", tags=["Posts"])
categories_router = APIRouter(
    prefix="/categories",
    tags=["Posts", "Categories"],
)

DEFAULT_ACCESS_RESTRICTED_MESSAGE: str = "Only author of a post can edit it"


def is_author_or_raise_401(
    user: User,
    post: Post,
    detail: str = DEFAULT_ACCESS_RESTRICTED_MESSAGE,
) -> None:
    if post.author != user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail)


async def _post_to_schema(post: Post) -> PostSchema:
    return PostSchema(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        categories=[
            _category_to_schema(category)
            for category in await post.awaitable_attrs.categories
        ],
        author=(await post.awaitable_attrs.author).email,
    )


def _category_to_schema(category: Category) -> CategorySchema:
    return CategorySchema(name=category.name, slug=category.slug)


@categories_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    user: User = Depends(get_user_by_JWT_token),
    session: AsyncSession = Depends(get_scoped_session),
) -> CategorySchema:
    is_admin_or_raise_401(user)
    return _category_to_schema(await services.create_category(session, data))


@posts_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostCreate,
    user: User = Depends(get_user_by_JWT_token),
    session: AsyncSession = Depends(get_scoped_session),
) -> PostSchema:
    is_admin_or_raise_401(user)
    return await _post_to_schema(
        await services.create_post(session, user, data)
    )


@categories_router.delete(
    "/{category_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    user: User = Depends(get_user_by_JWT_token),
    category: Category = Depends(dependencies.get_category_by_slug),
    session: AsyncSession = Depends(get_scoped_session),
):
    is_admin_or_raise_401(user)
    await services.delete_category(session, category)


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    user: User = Depends(get_user_by_JWT_token),
    post: Post = Depends(dependencies.get_post_by_id),
    session: AsyncSession = Depends(get_scoped_session),
):
    is_admin_or_raise_401(user)
    is_author_or_raise_401(user, post)

    await services.delete_post(session, post)


@categories_router.get("/")
async def get_all_categories(
    session: AsyncSession = Depends(get_scoped_session),
) -> list[CategorySchema]:
    return [
        _category_to_schema(category)
        for category in await services.get_all_categories(session)
    ]


@posts_router.get("/")
async def get_all_posts(
    session: AsyncSession = Depends(get_scoped_session),
) -> list[PostSchema]:
    return [
        await _post_to_schema(post)
        for post in await services.get_all_posts(session)
    ]


@categories_router.get("/{category_slug}")
async def get_category_by_slug(
    category: Category = Depends(dependencies.get_category_by_slug),
) -> CategorySchema:
    return _category_to_schema(category)


@posts_router.get("/{post_id}")
async def get_post_by_id(
    post: Post = Depends(dependencies.get_post_by_id),
) -> PostSchema:
    return await _post_to_schema(post)


@categories_router.patch("/{category_slug}")
async def partial_update_category(
    data: CategoryUpdatePartial,
    user: User = Depends(get_user_by_JWT_token),
    category: Category = Depends(dependencies.get_category_by_slug),
    session: AsyncSession = Depends(get_scoped_session),
) -> CategorySchema:
    is_admin_or_raise_401(user)
    return _category_to_schema(
        await services.update_category(
            session,
            category,
            data,
            partial=True,
        )
    )


@posts_router.patch("/{post_id}")
async def partial_update_post(
    data: PostUpdatePartial,
    user: User = Depends(get_user_by_JWT_token),
    post: Post = Depends(dependencies.get_post_by_id),
    session: AsyncSession = Depends(get_scoped_session),
):
    is_admin_or_raise_401(user)
    is_author_or_raise_401(user, post)

    return await _post_to_schema(
        await services.update_post(session, post, data, partial=True)
    )


@categories_router.put("/{category_slug}")
async def update_category(
    data: CategoryUpdate,
    user: User = Depends(get_user_by_JWT_token),
    category: Category = Depends(dependencies.get_category_by_slug),
    session: AsyncSession = Depends(get_scoped_session),
):
    is_admin_or_raise_401(user)
    return _category_to_schema(
        await services.update_category(session, category, data)
    )


@posts_router.put("/{post_id}")
async def update_post(
    data: PostUpdate,
    user: User = Depends(get_user_by_JWT_token),
    post: Post = Depends(dependencies.get_post_by_id),
    session: AsyncSession = Depends(get_scoped_session),
):
    is_admin_or_raise_401(user)
    is_author_or_raise_401(user, post)

    return await _post_to_schema(
        await services.update_post(session, post, data)
    )
