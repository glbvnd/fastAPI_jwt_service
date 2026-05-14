from sqlalchemy import DateTime, Column, String, INTEGER, BIGINT, Integer, ForeignKey, Text, Boolean, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from enum import Enum
from uuid import uuid4
from datetime import datetime

class RefreshTokenModel(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id :Mapped[int]=mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(nullable=False)
    jti: Mapped[str] = mapped_column(default=lambda: str(
        uuid4()), nullable=False, unique=True, index=True)
    parent_jti: Mapped[str] = mapped_column(index=True, nullable=True)
    family_id: Mapped[str] = mapped_column(index=True)
    user_agent: Mapped[str]
    ip_address: Mapped[str]
    revoke: Mapped[bool] = mapped_column(default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user =relationship("UserModel", back_populates="refresh_token")