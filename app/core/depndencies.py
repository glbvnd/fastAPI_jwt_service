from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from fastapi import Depends, Cookie, HTTPException, status
from app.repository.user_repository import UserRepository
from app.repository.token_repository import TokenRepository
from app.service.auth_service import AuthService
from app.service.user_service import AccountService
from jose import jwt, JWTError
from .config import settings

# Auth Service


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repo = UserRepository(db=db)
    token_repo = TokenRepository(db=db)
    return AuthService(user_repo=user_repo, token_repo=token_repo)


async def get_account_service(db: AsyncSession = Depends(get_db)) -> AccountService:
    user_repo = UserRepository(db=db)
    return AccountService(user_repo=user_repo)


async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db=db)


async def get_current_user_by_cookie(
    access_token: str = Cookie(None), user_repo: UserRepository = Depends(get_user_repo)
):

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not any token"
        )
    try:
        payload = jwt.decode(
            token=access_token, key=settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )  # ->dict
        user_public_id = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    user = await user_repo.get_by_public_id(user_public_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
