from aiohttp.web_exceptions import HTTPConflict, HTTPUnauthorized

from src.repository.cache.base import Cache
from src.repository.base import UserRepository
from src.schemas.auth import (
    RegisterRequestSchema,
    LoginResponseSchema,
    LogoutRequestSchema,
)
from src.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
    get_token_ttl,
)


class MutationUser:
    def __init__(self, user_repository: UserRepository, black_list: Cache):
        self._user_repository = user_repository
        self._black_list = black_list

    async def create_user(self, user: RegisterRequestSchema):
        if await self._user_repository.get_user_by_name(user.name):
            raise HTTPConflict(text="User with that name already exists")
        await self._user_repository.create_user(user.name, hash_password(user.password))

    async def login_user(self, user: RegisterRequestSchema) -> LoginResponseSchema:
        user_db = await self._user_repository.get_user_by_name(user.name)
        if not user_db or not verify_password(user.password, user_db.password):
            raise HTTPUnauthorized()
        return LoginResponseSchema(
            access_token=create_access_token(user_db.id), token_type="bearer"
        )

    async def logout_user(self, data: LogoutRequestSchema):
        token = data.Authorization.split(" ")[1]
        try:
            ttl = get_token_ttl(token)
        except ValueError:
            return
        await self._black_list.add(token, "1", ttl)

    async def verify_user(self, data: LogoutRequestSchema):
        token = data.Authorization.split(" ")[1]
        if await self._black_list.get(token):
            raise HTTPUnauthorized()

        is_verify = verify_access_token(data.Authorization.split(" ")[1])
        if not is_verify:
            raise HTTPUnauthorized()
