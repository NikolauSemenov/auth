from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.base import UserRepository
from src.repository.query.user import CreateUser, GetUserByName


class SqlAlchemyUserRepository(UserRepository):
    __slots__ = ("_create_user", "_get_user_by_name")

    def __init__(self, connection: AsyncConnection):
        self._create_user = CreateUser(connection)
        self._get_user_by_name = GetUserByName(connection)

    @property
    def create_user(self) -> CreateUser:
        return self._create_user

    @property
    def get_user_by_name(self) -> GetUserByName:
        return self._get_user_by_name
