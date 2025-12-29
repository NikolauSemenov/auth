from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response

from src.config.settings import settings
from src.repository.cache.user import UserCache
from src.repository.repository import SqlAlchemyUserRepository
from src.schemas.auth import BaseSchema
from src.services.user import User
from src.utils.security.jwt import JwtSecurity
from src.web.state_app import StateApp


class BaseViews(web.View):
    def __init__(self, request: Request):
        super().__init__(request)
        state: StateApp = request.app.get("state_app")
        if not state:
            raise RuntimeError("StateApp missing in BaseViews")
        self._service = User(
            SqlAlchemyUserRepository(request["conn"]),
            UserCache(state.state_repo.cache),
            JwtSecurity(settings),
            state.state_infra.producer,
            settings,
        )

    @staticmethod
    def response(_schema: BaseSchema, status: int = 200) -> Response:
        return web.json_response(_schema.Schema().dump(_schema), status=status)
