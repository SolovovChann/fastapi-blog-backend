import bleach
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from auth.models import User
from core.database import Base, Model
from utils import slugify


AVAILABLE_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "a",
    "h1",
    "h2",
    "h3",
    "h4",
    "blockquote",
    "code",
    "pre",
]

AVAILABLE_ATTRIBUTES = [
    "href",
    "title",
    "alt",
]


post_category = Table(
    "post_category",
    Model.metadata,
    Column(
        "post_id",
        Integer,
        ForeignKey("posts.id"),
        primary_key=True,
    ),
    Column(
        "category_slug",
        String,
        ForeignKey("categories.slug"),
        primary_key=True,
    ),
)


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(150))
    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    posts: "Mapped[list[Post]]" = relationship(
        "Post",
        secondary=post_category,
        back_populates="categories",
    )

    def __repr__(self) -> str:
        return f"<Category({self.slug=}, {self.name=})>"

    def __str__(self) -> str:
        return self.name

    @validates("slug")
    def validate_slug(self, key: str, value: str) -> str:
        return slugify(value)


class Post(Model):
    __tablename__ = "posts"

    author_id = Column(Integer, ForeignKey("users.id"))
    author: Mapped[User] = relationship("User", back_populates="posts")
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )
    content: Mapped[str]
    categories: Mapped[list[Category]] = relationship(
        "Category",
        secondary=post_category,
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"<Post({self.id=}, {self.title=}, {self.slug=})>"

    def __str__(self) -> str:
        return self.title

    @validates("content")
    def validate_content(self, key: str, value: str) -> str:
        # NOTE bleach is deprecated since 2023
        return bleach.clean(
            value,
            tags=AVAILABLE_TAGS,
            attributes=AVAILABLE_ATTRIBUTES,
        )
