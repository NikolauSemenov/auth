from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response

from src.repository.cache.black_token import BlackToken
from src.repository.repository import SqlAlchemyUserRepository
from src.schemas.auth import BaseSchema
from src.services.mutation_user import MutationUser


class BaseViews(web.View):
    def __init__(self, request: Request):
        super().__init__(request)
        self._service = MutationUser(
            SqlAlchemyUserRepository(request["conn"]),
            BlackToken(request.app["state_repository"].cache),
        )

    @staticmethod
    def response(_schema: BaseSchema) -> Response:
        return web.json_response(_schema.Schema().dump(_schema))
