from sqlalchemy import (
    DateTime,
    Column,
    String,
    INTEGER,
    BIGINT,
    Integer,
    ForeignKey,
    Text,
    Boolean,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from enum import Enum
from uuid import uuid4
from datetime import datetime


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserModel(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(
        default=lambda: str(uuid4()), unique=True, nullable=False, index=True
    )
    user_name: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    refresh_tokens = relationship(
        "RefreshTokenModel", back_populates="user", cascade="all, delete-orphan"
    )
