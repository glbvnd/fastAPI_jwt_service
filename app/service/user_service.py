from app.repository.user_repository import UserRepository
from app.core.security import PasswordService


class AccountService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def change_username(self, public_id, new_username: str):
        if len(new_username) < 5:
            raise ValueError("userName too short!")
        user = await self.user_repo.get_by_public_id(public_id=public_id)
        await self.user_repo.update_username(public_id, new_username)

    async def change_password(
        self, last_pass: str, public_id: str, input_new_password: str
    ):
        user = await self.user_repo.get_by_public_id(public_id=public_id)
        validate = PasswordService.verify_password(last_pass, user.hashed_password)
        if validate:
            new_hashed_password = PasswordService.hash_password(input_new_password)
            user.hashed_password = new_hashed_password
