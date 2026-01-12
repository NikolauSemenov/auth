import json
import secrets

from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPNotFound,
)

from src.config.settings import Settings
from src.infrastructure.broker.base import BaseProducer
from src.repository.cache.base import Cache
from src.repository.base import UserRepository
from src.schemas.auth import (
    RegisterRequestSchema,
    LoginResponseSchema,
    LogoutRequestSchema,
    GrantTokenRequestSchema,
    LoginEmailRequestSchema,
    VerifyEmailRequestSchema,
    LoginRequestSchema,
    VerifyResponseSchema,
)
from src.utils.security.base import SecurityToken
from src.utils.security.hash_code import encrypt_code, decrypt_code


class User:
    __slots__ = ("_user_repository", "_user_cache", "_security", "_broker", "_settings")

    def __init__(
        self,
        user_repository: UserRepository,
        user_cache: Cache,
        security: SecurityToken,
        broker: BaseProducer,
        settings: Settings,
    ):
        self._user_repository = user_repository
        self._user_cache = user_cache
        self._security = security
        self._broker = broker
        self._settings = settings

    async def create_user(self, user: RegisterRequestSchema) -> None:
        if await self._user_repository.get_user_by_login(user.login):
            raise HTTPConflict(text="User with that name already exists")
        if await self._user_repository.get_user_by_email(user.email):
            raise HTTPConflict(text="User with that email already exists")
        await self._user_repository.create_user(
            dict(
                login=user.login,
                user_name=user.user_name,
                last_name=user.last_name,
                password=self._security.hash_password(user.password),
                email=user.email,
            )
        )
        await self._broker.send(
            topic=self._settings.topic_create_user,
            value=dict(login=user.login, email=user.email),
        )

    async def login_user(self, user: LoginRequestSchema) -> LoginResponseSchema:
        user_db = await self._user_repository.get_user_by_login(user.login)
        if not user_db:
            raise HTTPNotFound(text="User not found")
        if not user_db.is_active or not self._security.verify_password(
            user.password, user_db.password
        ):
            raise HTTPUnauthorized()
        return LoginResponseSchema(
            access_token=self._security.create_access_token(user_db.id),
            token_type="Bearer",
            user_name=user_db.user_name,
            last_name=user_db.last_name,
        )

    async def logout_user(self, data: LogoutRequestSchema):
        token = data.Authorization.split(" ")[1]
        try:
            ttl = self._security.get_token_ttl(token)
        except ValueError:
            return
        await self._user_cache.add(f"black-token:{token}", "1", ttl)

    async def verify_user(self, data: LogoutRequestSchema) -> VerifyResponseSchema:
        token = data.Authorization.split(" ")[1]
        if await self._user_cache.get(f"black-token:{token}"):
            raise HTTPUnauthorized()

        verify_data = self._security.verify_access_token(
            data.Authorization.split(" ")[1]
        )
        if not verify_data:
            raise HTTPUnauthorized()
        return VerifyResponseSchema(user_id=verify_data)

    async def grant_token_permission(
        self, data: GrantTokenRequestSchema, headers: LogoutRequestSchema
    ):
        token = headers.Authorization.split(" ")[1]

        current_user_id = self._security.decode_token(token)
        if current_user_id is None:
            raise HTTPUnauthorized(text="Invalid or expired token")

        current_user = await self._user_repository.get_user_by_id(current_user_id)
        if not current_user or not current_user.is_admin:
            raise HTTPForbidden(text="Only admins can grant token permissions")

        target_user = await self._user_repository.get_user_by_id(data.user_id)
        if not target_user:
            raise HTTPNotFound(text="Target user not found")

        await self._user_repository.set_token_permission(data.user_id)

    async def send_email_code(self, data: LoginEmailRequestSchema):
        user = await self._user_repository.get_user_by_email(data.email)

        if not user:
            raise HTTPNotFound(text="User not found")
        if not user.is_active:
            raise HTTPUnauthorized(text="User is not active")

        hash_code = encrypt_code("".join(secrets.choice("0123456789") for _ in range(12)))
        await self._user_cache.add(
            f"auth:code:{data.email}",
            json.dumps({"hash_code": hash_code, "try": 0}),
            int(self._settings.ttl_email_code_life.total_seconds()),
        )

        await self._broker.send(
            topic=self._settings.topic_verify_email,
            value=dict(login=user.login, email=user.email, code=hash_code),
        )

    async def verify_email_code(
        self, data: VerifyEmailRequestSchema
    ) -> LoginResponseSchema:
        byte_data = await self._user_cache.get(f"auth:code:{data.email}")
        if not byte_data:
            raise HTTPUnauthorized(text="Invalid or expired token")

        cache_data = json.loads(byte_data.decode())

        if cache_data["try"] >= 3:
            raise HTTPForbidden(text="Try again later")

        code = decrypt_code(cache_data["hash_code"])
        if code != data.code:
            cache_data["try"] += 1
            await self._user_cache.add(
                f"auth:code:{data.email}",
                json.dumps(cache_data),
                int(self._settings.ttl_email_code_life.total_seconds()),
            )
            raise HTTPUnauthorized(text="Invalid code")

        user = await self._user_repository.get_user_by_email(data.email)
        if not user:
            raise HTTPNotFound(text="User not found")
        return LoginResponseSchema(
            access_token=self._security.create_access_token(user.id),
            token_type="Bearer",
            last_name=user.last_name,
            user_name=user.user_name,
        )
