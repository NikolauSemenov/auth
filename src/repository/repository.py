from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.query.user import CreateUser, GetUserByName


class UserRepository:
    def __init__(self, connection: AsyncConnection):
        self.create_user = CreateUser(connection)
        self.get_user_by_name = GetUserByName(connection)
