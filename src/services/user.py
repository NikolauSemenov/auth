from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPNotFound,
)

from src.infrastructure.broker.base import BaseProducer
from src.repository.cache.base import Cache
from src.repository.base import UserRepository
from src.schemas.auth import (
    RegisterRequestSchema,
    LoginResponseSchema,
    LogoutRequestSchema,
    GrantTokenRequestSchema,
)
from src.utils.security.base import SecurityToken


class User:
    __slots__ = ("_user_repository", "_black_list", "_security", "_broker")

    def __init__(
        self,
        user_repository: UserRepository,
        black_list: Cache,
        security: SecurityToken,
        broker: BaseProducer,
    ):
        self._user_repository = user_repository
        self._black_list = black_list
        self._security = security
        self._broker = broker

    async def create_user(self, user: RegisterRequestSchema) -> None:
        if await self._user_repository.get_user_by_name(user.name):
            raise HTTPConflict(text="User with that name already exists")
        await self._broker.send(
            value={
                "name": user.name,
                "password": self._security.hash_password(user.password),
            }
        )

    async def login_user(self, user: RegisterRequestSchema) -> LoginResponseSchema:
        user_db = await self._user_repository.get_user_by_name(user.name)
        if not user_db:
            raise HTTPNotFound(text="User not found")
        if not user_db.is_active or not self._security.verify_password(
            user.password, user_db.password
        ):
            raise HTTPUnauthorized()
        return LoginResponseSchema(
            access_token=self._security.create_access_token(user_db.id),
            token_type="Bearer",
        )

    async def logout_user(self, data: LogoutRequestSchema):
        token = data.Authorization.split(" ")[1]
        try:
            ttl = self._security.get_token_ttl(token)
        except ValueError:
            return
        await self._black_list.add(token, "1", ttl)

    async def verify_user(self, data: LogoutRequestSchema):
        token = data.Authorization.split(" ")[1]
        if await self._black_list.get(token):
            raise HTTPUnauthorized()

        is_verify = self._security.verify_access_token(data.Authorization.split(" ")[1])
        if not is_verify:
            raise HTTPUnauthorized()

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
