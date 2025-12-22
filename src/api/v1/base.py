from aiohttp import web
from aiohttp.abc import Request

from src.repository.repository import UserRepository
from src.services.mutation_user import MutationUser


class BaseViews(web.View):
    def __init__(self, request: Request):
        super().__init__(request)
        self._service = MutationUser(UserRepository(request["conn"]))
