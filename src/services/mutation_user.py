from aiohttp.web_exceptions import HTTPConflict, HTTPUnauthorized

from src.schemas.auth import RegisterRequestSchema, LoginResponseSchema
from src.utils.security import hash_password, verify_password, create_access_token


class MutationUser:
    def __init__(self, user_repository):
        self._user_repository = user_repository

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
