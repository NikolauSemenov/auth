from datetime import datetime, UTC

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from src.config.settings import Settings
from src.utils.security.base import SecurityToken


class JwtSecurity(SecurityToken):
    __slots__ = ("_settings", "_ph")

    def __init__(self, settings: Settings):
        self._settings = settings
        self._ph = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._ph.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            self._ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.now(UTC) + self._settings.access_token_lifetime
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": int(expire.timestamp()),
        }
        return jwt.encode(
            payload,
            self._settings.secret_key,
            algorithm=self._settings.algorithm,
        )

    def verify_access_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.algorithm],
            )
            return payload.get("type") == "access"
        except JWTError:
            return False

    def get_token_ttl(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.algorithm],
            )
        except (JWTError, ExpiredSignatureError, JWTClaimsError):
            raise ValueError

        exp = payload.get("exp")
        if exp is None:
            return 0

        now = int(datetime.now(UTC).timestamp())
        return max(0, exp - now)
