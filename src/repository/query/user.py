from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.tables import Users


class CreateUser:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, name: str, password: str) -> None:
        await self._connection.execute(
            insert(Users).values(name=name, password=password)
        )


class GetUserByName:
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, name: str) -> int | None:
        return await self._connection.scalar(
            select(Users.c.id).where(Users.c.name == name)
        )
