from aiohttp.web_exceptions import HTTPConflict, HTTPUnauthorized

from src.repository.cache.base import Cache
from src.repository.base import UserRepository
from src.schemas.auth import (
    RegisterRequestSchema,
    LoginResponseSchema,
    LogoutRequestSchema,
)
from src.utils.security.base import SecurityToken


class MutationUser:
    __slots__ = ("_user_repository", "_black_list", "_security")

    def __init__(
        self,
        user_repository: UserRepository,
        black_list: Cache,
        security: SecurityToken,
    ):
        self._user_repository = user_repository
        self._black_list = black_list
        self._security = security

    async def create_user(self, user: RegisterRequestSchema):
        if await self._user_repository.get_user_by_name(user.name):
            raise HTTPConflict(text="User with that name already exists")
        await self._user_repository.create_user(
            user.name, self._security.hash_password(user.password)
        )

    async def login_user(self, user: RegisterRequestSchema) -> LoginResponseSchema:
        user_db = await self._user_repository.get_user_by_name(user.name)
        if not user_db or not self._security.verify_password(
            user.password, user_db.password
        ):
            raise HTTPUnauthorized()
        return LoginResponseSchema(
            access_token=self._security.create_access_token(user_db.id),
            token_type="bearer",
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
