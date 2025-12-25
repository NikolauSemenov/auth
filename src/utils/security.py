from datetime import datetime, UTC

from jose import jwt, JWTError, ExpiredSignatureError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose.exceptions import JWTClaimsError

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
    expire = datetime.now(UTC) + settings.access_token_lifetime
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_access_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("type") != "access":
            return False
    except JWTError:
        return False
    return True


def get_token_ttl(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except (JWTError, ExpiredSignatureError, JWTClaimsError):
        raise ValueError

    exp = payload.get("exp")
    if exp is None:
        return 0

    now = int(datetime.now(UTC).timestamp())
    return max(0, exp - now)
