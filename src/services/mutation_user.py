from aiohttp.web_exceptions import HTTPConflict

from src.schemas.auth import RegisterRequestSchema
from src.utils.security import hash_password


class MutationUser:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    async def create_user(self, user: RegisterRequestSchema):
        if await self._user_repository.get_user_by_name(user.name):
            raise HTTPConflict(text="User with that name already exists")
        await self._user_repository.create_user(user.name, hash_password(user.password))
