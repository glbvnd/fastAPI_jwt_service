from sqlalchemy import DateTime, Column, String, INTEGER, BIGINT, Integer, ForeignKey, Text, Boolean, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum
from uuid import uuid4


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    public_id = Column(String, default=lambda: str(uuid4()),
                       unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    refresh_token = relationship("ًRefreshTokenModel", back_populates="user",
                                 cascade="all, delete-orphan")
