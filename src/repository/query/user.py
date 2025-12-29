from typing import Any
from sqlalchemy import insert, select, Row, update

from src.repository.query.base import UserBase
from src.repository.tables import Users


class CreateUser(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, name: str, password: str) -> int | None:
        return await self._connection.scalar(
            insert(Users).values(name=name, password=password).returning(Users.c.id)
        )


class GetUserByName(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, name: str) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.name == name)
        )
        return result.fetchone()


class GetUserById(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, user_id: int) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.id == user_id)
        )
        return result.fetchone()


class UpdateUserActive(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, user_id: int) -> None:
        await self._connection.execute(
            update(Users).where(Users.c.id == user_id).values(is_active=True)
        )
