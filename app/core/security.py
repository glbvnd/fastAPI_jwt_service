
from app.core.config import settings
from passlib.context import CryptContext
from app.models.user import UserModel
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import hashlib
import secrets

class PasswordService(UserModel):
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    # password hashing

    @classmethod
    def hash_password(cls, plain_pass: str) -> str:
        return cls.pwd_context.hash(plain_pass)

    # password verification
    @classmethod
    def verify_password(cls, plain_pass: str, hashed_pass: str) -> bool:
        return cls.pwd_context.verify(plain_pass, hashed_pass)


class TokenService:

    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = "HS256"

    @classmethod
    def generate_access_token(cls, user_id: int) -> str:
        expires = datetime.now(
            timezone(True)) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": expires
        }

        access_token = jwt.encode(
            payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return access_token

    @classmethod
    def generate_refresh_token(cls, user_id: int) -> tuple[str, str]:
        expires = datetime.noe(
            timezone(True)+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        jti = str(uuid4())
        payload = {
            "sub": str(user_id),
            "jti": jti,
            "typ": "refresh",
            "exp": expires
        }
        refresh_token = jwt.encode(payload, cls.SECRET_KEY, cls.ALGORITHM)

        return refresh_token, jti
    
    @classmethod
    def hash_refresh_token(cls, plain_token:str)->str:
        return hashlib.sha256(plain_token.encode("utf-8")).hexdigest()
    
    @classmethod
    def decode_token(cls, token:str)-> dict:
        decoded= jwt.decode(token, cls.SECRET_KEY, cls.ALGORITHM)
        return decoded
        
    @classmethod
    def verify_refresh_token(cls, plain_token:str, hashed_token:str)->bool:
        plain_token_hash = cls.hash_refresh_token(plain_token)
        return secrets.compare_digest(plain_token_hash, hashed_token)
        
            