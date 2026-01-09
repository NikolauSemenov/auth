from typing import Any
from sqlalchemy import insert, select, Row, update

from src.repository.query.base import UserBase
from src.repository.tables import Users


class CreateUser(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, user_data: dict[str, str]) -> int | None:
        return await self._connection.scalar(
            insert(Users).values(user_data).returning(Users.c.id)
        )


class GetUserByLogin(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, login: str) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.login == login)
        )
        return result.fetchone()


class GetUserByEmail(UserBase):
    __slots__ = ("_connection",)

    async def __call__(self, email: str) -> Row[Any] | None:
        result = await self._connection.execute(
            select(Users).where(Users.c.email == email)
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
