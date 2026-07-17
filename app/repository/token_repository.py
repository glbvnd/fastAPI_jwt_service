from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshTokenModel
from sqlalchemy import select, delete, update
from datetime import datetime, timezone
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.models import RefreshTokenModel


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # create new database record
    async def store_token(
        self,
        *,
        user_id: int,
        token_hash: str,
        jti: str,
        family_id: str,
        parent_jti: str | None,
        user_agent: str,
        ip_address: str,
        expires_at: datetime,
    ) -> RefreshTokenModel:

        token = RefreshTokenModel(
            user_id=user_id,
            token_hash=token_hash,
            jti=jti,
            family_id=family_id,
            parent_jti=parent_jti,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at,
        )
        try:
            self.db.add(token)
            await self.db.commit()
            await self.db.refresh(token)
            return token

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    # get token from DB

    async def get_by_jti(self, jti: str) -> RefreshTokenModel | None:
        query = await self.db.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.jti == jti)
        )
        result = query.scalar_one_or_none()
        return result

    async def get_by_hash(self, hashed_token: str) -> RefreshTokenModel | None:
        query = await self.db.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == hashed_token
            )
        )
        result = query.scalar_one_or_none()
        return result

    async def revoked_token(self, token: RefreshTokenModel):
        try:
            token.revoked = True
            token.revoked_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(token)
            return {"message": " token revoked"}

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_expired_tokens(self):
        try:
            stmt = delete(RefreshTokenModel).where(
                RefreshTokenModel.expires_at < datetime.now(timezone.utc)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.rowcount
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_user_tokens(self, user_public_id: str) -> List[RefreshTokenModel]:
        query = select(RefreshTokenModel).where(
            RefreshTokenModel.user_id == user_public_id
        )
        tokens = await self.db.execute(query)
        return tokens.scalars().all()

    async def revoke_family_id(self, family_id):
        try:
            stmt = (
                update(RefreshTokenModel)
                .where(RefreshTokenModel.family_id == family_id,
                       RefreshTokenModel.revoked == False)
                .values(revoked=True, revoked_at=datetime.now(timezone.utc))
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.rowcount

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def revoke_all_sessions(self, user_id: int):
        try:
            stmt = (
                update(RefreshTokenModel)
                .where(RefreshTokenModel.user_id == user_id,
                       RefreshTokenModel.revoked == False)
                .values(revoked=True,
                        revoked_at=datetime.now(timezone.utc))
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return {"message": f"{result.rowcount} sessions deleted"}

        except SQLAlchemyError:
            await self.db.rollback()
            raise
