import logging
from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.abc import Request, StreamResponse
from aiohttp.web_middlewares import middleware
from aiohttp_apigami import validation_middleware

from src.web.state_app import StateApp


class Middleware:
    @middleware
    async def _transaction_middleware(
        self,
        request: Request,
        handler: Callable[[Request], Awaitable[StreamResponse]],
    ) -> StreamResponse:
        state: StateApp = request.app.get("state_app")
        if state is None:
            logging.error("StateApp missing in Middleware")
            raise web.HTTPServiceUnavailable(text="Service not available")
        if request.method in ["GET", "OPTION", "HEAD"]:
            async with state.state_repo.db.get_connection() as conn:
                request["conn"] = conn
                return await handler(request)
        else:
            async with state.state_repo.db.get_transaction() as conn_tx:
                request["conn"] = conn_tx
                return await handler(request)

    def get_middlewares(self):
        return [validation_middleware, self._transaction_middleware]
