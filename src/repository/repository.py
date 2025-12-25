from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.base import UserRepository
from src.repository.query.user import (
    CreateUser,
    GetUserByName,
    GetUserById,
    UpdateUserActive,
)


class SqlAlchemyUserRepository(UserRepository):
    __slots__ = ("_create_user", "_get_user_by_name")

    def __init__(self, connection: AsyncConnection):
        self._create_user = CreateUser(connection)
        self._get_user_by_name = GetUserByName(connection)
        self._get_user_by_id = GetUserById(connection)
        self._set_token_permission = UpdateUserActive(connection)

    @property
    def create_user(self) -> CreateUser:
        return self._create_user

    @property
    def get_user_by_name(self) -> GetUserByName:
        return self._get_user_by_name

    @property
    def get_user_by_id(self) -> GetUserById:
        return self._get_user_by_id

    @property
    def set_token_permission(self) -> UpdateUserActive:
        return self._set_token_permission
