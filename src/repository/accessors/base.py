import abc


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abc.abstractmethod
    async def ping(self):
        raise NotImplementedError()
