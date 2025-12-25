from sqlalchemy.ext.asyncio import AsyncConnection


class UserBase:
    __slots__ = ("_connection",)

    def __init__(self, connection: AsyncConnection):
        self._connection = connection
