from app.repository.user_repository import UserRepository
from app.repository.token_repository import TokenRepository
from app.core.security import PasswordService, JwtHandeler
import uuid
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.models.user import UserModel
from jose import ExpiredSignatureError


class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register(
        self,
        email: str,
        plain_password: str,
        role: str = "user",
        username: str = "new_user",
    ):
        # check email:
        if await self.user_repo.email_exists(email=email):
            raise ValueError("Email already exists")

        hashed_password = PasswordService.hash_password(
            plain_pass=plain_password)

        user = await self.user_repo.create_user(
            email=email, hashed_password=hashed_password, role=role, user_name=username
        )

        return user

    async def login(
        self, email: str, plain_password: str, user_agent: str, ip_address: str
    ) -> dict:
        """return a dict that its containd access and refresh tokens"""
        # get user
        user = await self.user_repo.get_by_email(email=email)
        # check user in db
        if not user:
            raise ValueError("Invalid credentials : email not found")
        # verify password
        if not PasswordService.verify_password(
            plain_pass=plain_password, hashed_pass=user.hashed_password
        ):
            raise ValueError("Invalid credentials : passwords not match")

        # set active user:
        await self.user_repo.set_user_activate(user_id=user.id, bool=True)
        # Generate Tokens
        access_token = JwtHandeler.generate_access_token(
            user_public_id=user.public_id)
        refresh_token, expire_dt, payload = JwtHandeler.generate_refresh_token(
            user_public_id=user.public_id
        )
        hashed_refresh_token = JwtHandeler.hash_refresh_token(refresh_token)
        family_id = str(uuid.uuid4())
        parent_jti = None
        # store Refresh Token in db

        await self.token_repo.store_token(
            user_id=user.id,
            jti=payload["jti"],
            token_hash=hashed_refresh_token,
            parent_jti=parent_jti,
            family_id=family_id,
            expires_at=expire_dt,
            user_agent=user_agent,
            ip_address=ip_address,
        )

        return {
            "email": user.email,
            "user_public_id": user.public_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

    async def refresh_endpoint(self, plain_refresh_token: str, user_agent: str, ip_address: str) -> str:
        try:
            decode = JwtHandeler.decode_token(plain_refresh_token)
            user_public_id = decode.get("sub")
            jti = decode.get("jti")

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token has expired, please login again")

        user = await self.user_repo.get_by_public_id(user_public_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        db_token = await self.token_repo.get_by_jti(jti=jti)
        if not db_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="invalid Refresh Token(jti)")

        family_id = db_token.family_id

        if db_token.revoked:
            await self.token_repo.revoke_family_id(family_id)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token reuse detected")

        # check Hash
        if not JwtHandeler.verify_refresh_token(
                plain_token=plain_refresh_token, hashed_token=db_token.token_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid refresh token(empty db)")
        # check expiration
        if db_token.expires_at < datetime.utcnow():
            raise HTTPException(401, "Refresh token expired")

        # Rotation
        await self.token_repo.revoked_token(db_token)
        # new RT
        new_refresh_token, exp, payload = JwtHandeler.generate_refresh_token(
            user_public_id=user_public_id
        )
        hashed_token = JwtHandeler.hash_refresh_token(new_refresh_token)

        await self.token_repo.store_token(user_id=user.id,
                                          token_hash=hashed_token,
                                          jti=payload["jti"],
                                          family_id=family_id,
                                          parent_jti=jti,
                                          expires_at=exp,
                                          user_agent=user_agent,
                                          ip_address=ip_address)

        # generate access token
        access_token = JwtHandeler.generate_access_token(user.public_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }

    async def logout(self, plain_refresh_token: str):
        try:
            decode = JwtHandeler.decode_token(plain_refresh_token)
            jti = decode.get("jti")
            db_token = await self.token_repo.get_by_jti(jti)

            await self.token_repo.revoked_token(db_token)

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid Token")

    async def logout_all_session(self, access_token: str):

        try:
            decoded = JwtHandeler.decode_token(access_token)
            user_public_id = decoded.get("sub")
            user = await self.user_repo.get_by_public_id(user_public_id)
            await self.token_repo.revoke_all_sessions(user_id=user.id)

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid Token")

    async def delete_account(self, plain_password: str, plain_refresh_token: str):

        decode = JwtHandeler.decode_token(plain_refresh_token)
        public_id = decode.get("sub")
        if not public_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user = await self.user_repo.get_by_public_id(public_id=public_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )

        valid = PasswordService.verify_password(
            plain_pass=plain_password, hashed_pass=user.hashed_password
        )

        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
            )

        await self.user_repo.delete_account(user_id=user.id)

        return {"detail": "DELETED USER ACCOUNT"}
