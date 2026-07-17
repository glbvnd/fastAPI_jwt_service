from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, exists
from app.models.user import UserModel
from sqlalchemy.exc import SQLAlchemyError


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self, email: str, hashed_password: str, user_name: str | None, role: str
    ) -> UserModel:
        try:
            user = UserModel(
                email=email,
                user_name=user_name,
                hashed_password=hashed_password,
                role=role,
            )

            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete_account(self, user_id:int) -> bool:
        try:
            stmt = delete(UserModel).where(UserModel.id == user_id)
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_public_id(self, public_id: str) -> UserModel | None:

        result = await self.db.execute(
            select(UserModel).where(UserModel.public_id == public_id)
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        stmt = select(exists().where(UserModel.email == email))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_password(self, public_id: str, new_hashed_password: str):
        try:
            stmt = (
                update(UserModel)
                .where(UserModel.public_id == public_id)
                .values(hashed_password=new_hashed_password)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def update_username(self, public_id: str, new_username: str) -> bool:
        try:
            stmt = (
                update(UserModel)
                .where(UserModel.public_id == public_id)
                .values(user_name=new_username)
            )
            result = await self.db.execute(stmt)
            return result.rowcount > 0

        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def set_user_activate(self, user_id: int, bool: bool):
        try:
            stmt = (
                update(UserModel).where(UserModel.id == user_id).values(is_active=bool)
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            return f"user activetion is :{bool}"
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def check_activation(self, public_id: str):
        user = await self.db.execute(
            select(UserModel).where(UserModel.public_id == public_id)
        )
        result = user.scalar_one_or_none()
        if result:
            return result.is_active
        raise "user not found"
