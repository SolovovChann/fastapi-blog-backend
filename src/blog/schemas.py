from pydantic import BaseModel, EmailStr


class Category(BaseModel):
    name: str
    slug: str


class CategoryCreate(Category): ...


class CategoryUpdate(Category): ...


class CategoryUpdatePartial(BaseModel):
    name: str | None = None
    slug: str | None = None


class BasePost(BaseModel):
    title: str
    slug: str
    content: str


class PostCreate(BasePost):
    categories: list[str]


class PostDelete(BaseModel):
    id: int


class Post(BasePost, PostDelete):
    author: EmailStr
    categories: list[Category]


class PostUpdate(BaseModel):
    title: str
    content: str
    categories: list[str]


class PostUpdatePartial(BaseModel):
    title: str | None = None
    content: str | None = None
    categories: list[str] | None = None
