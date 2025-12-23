from typing import Any

from sqlalchemy import insert, select, Row
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

    async def __call__(self, name: str) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.name == name)
        )
        return result.fetchone()
