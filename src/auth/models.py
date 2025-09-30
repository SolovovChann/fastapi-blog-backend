import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Model


class UserRole(enum.Enum):
    USER = 0
    ADMIN = 1


class User(Model):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    password: Mapped[str] = mapped_column(String(1024))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
    )
    posts = relationship("Post", back_populates="author")

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return f"<User({self.id=}, {self.email=}, {self.full_name=}, {self.role.value=})>"
