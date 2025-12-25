from datetime import datetime, UTC

from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.config.settings import settings

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(user_id: int):
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": datetime.now(UTC) + settings.access_token_lifetime,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
