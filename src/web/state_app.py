from typing import AsyncIterator

from aiohttp import web

from src.config.settings import Settings
from src.infrastructure.base import StateInfrastructure
from src.infrastructure.state import AppStateInfrastructure
from src.repository.state.base import StateRepository
from src.repository.state.state import AppStateRepository


class StateApp:
    def __init__(self, settings: Settings):
        self._state_repo: StateRepository = AppStateRepository(settings)
        self._state_infra: StateInfrastructure = AppStateInfrastructure(settings)

    async def lifespan(self, app: web.Application) -> AsyncIterator[None]:
        async with self._state_repo, self._state_infra:
            yield

    @property
    def state_repo(self) -> StateRepository:
        return self._state_repo

    @property
    def state_infra(self):
        return self._state_infra
