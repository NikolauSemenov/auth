from datetime import datetime, UTC

from jose import jwt
from passlib.context import CryptContext

from src.config.settings import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int):
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": datetime.now(UTC) + settings.access_token_lifetime,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
