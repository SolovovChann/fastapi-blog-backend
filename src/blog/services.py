from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from blog.models import Category, Post
from blog.schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryUpdatePartial,
    PostCreate,
    PostUpdate,
    PostUpdatePartial,
)


async def create_category(
    session: AsyncSession,
    data: CategoryCreate,
) -> Category:
    category = Category(**data.model_dump())

    session.add(category)
    await session.commit()
    await session.refresh(category)

    return category


async def create_post(
    session: AsyncSession,
    author: User,
    data: PostCreate,
) -> Post:
    data_as_dict = data.model_dump()
    categories = data_as_dict.pop("categories")
    post = Post(**data_as_dict, author=author)

    for slug in categories:
        category = await get_category_by_slug(session, slug)

        if category is None:
            # NOTE rasing exception is better approach.
            # Rewrite later
            continue

        session.add(category)
        post.categories.append(category)

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return post


async def delete_category(session: AsyncSession, category: Category) -> None:
    await session.delete(category)


async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)


async def get_all_categories(session: AsyncSession) -> list[Category]:
    statement = select(Category).order_by(Category.slug)
    result: Result = await session.execute(statement)
    categories = result.scalars().all()

    return list(categories)


async def get_all_posts(session: AsyncSession) -> list[Post]:
    statement = select(Post).order_by(Post.id)
    result: Result = await session.execute(statement)
    products = result.scalars().all()

    return list(products)


async def get_category_by_slug(
    session: AsyncSession,
    slug: str,
) -> Category | None:
    return await session.get(Category, slug)


async def get_post_by_id(session: AsyncSession, id: int) -> Post | None:
    return await session.get(Post, id)


async def get_post_by_slug(
    session: AsyncSession,
    slug: str,
) -> Post | None:
    statement = select(Post).filter(Post.slug == slug)
    result: Result = await session.execute(statement)
    user = result.scalars().first()

    return user


async def update_category(
    session: AsyncSession,
    category: Category,
    data: CategoryUpdate | CategoryUpdatePartial,
    partial: bool = False,
) -> Category:
    for key, value in data.model_dump(exclude_none=partial).items():
        setattr(category, key, value)

    await session.commit()

    return category


async def update_post(
    session: AsyncSession,
    post: Post,
    data: PostUpdate | PostUpdatePartial,
    partial: bool = False,
) -> Post:
    for key, value in data.model_dump(exclude_none=partial).items():
        setattr(post, key, value)

    await session.commit()

    return post
