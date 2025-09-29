from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, validates

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

    @validates("slug")
    def validate_slug(self, key: str, value: str) -> str:
        return slugify(value)
