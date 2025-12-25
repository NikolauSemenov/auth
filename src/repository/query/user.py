# query/user.py
from typing import Any
from sqlalchemy import insert, select, Row, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.repository.tables import Users


class CreateUser:
    __slots__ = ("_connection",)

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, name: str, password: str) -> int:
        user_id = await self._connection.scalar(
            insert(Users).values(name=name, password=password).returning(Users.c.id)
        )
        if user_id is None:
            raise ValueError("Failed to create user")
        return int(user_id)  # возвращаем int


class GetUserByName:
    __slots__ = ("_connection",)

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, name: str) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.name == name)
        )
        return result.fetchone()


class GetUserById:
    __slots__ = ("_connection",)

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, user_id: int) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.id == user_id)
        )
        return result.fetchone()


class UpdateUserActive:
    __slots__ = ("_connection",)

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def __call__(self, user_id: int) -> None:
        await self._connection.execute(
            update(Users).where(Users.c.id == user_id).values(is_active=True)
        )
