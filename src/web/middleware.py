from typing import Callable, Awaitable

from aiohttp.abc import Request, StreamResponse
from aiohttp.web_middlewares import middleware
from aiohttp_apigami import validation_middleware


class Middleware:
    @middleware
    async def _transaction_middleware(
        self,
        request: Request,
        handler: Callable[[Request], Awaitable[StreamResponse]],
    ) -> StreamResponse:
        if request.method in ["GET", "OPTION", "HEAD"]:
            async with request.app["db_accessor"].get_connection() as conn:
                request["conn"] = conn
                return await handler(request)
        else:
            async with request.app["db_accessor"].get_transaction() as conn_tx:
                request["conn"] = conn_tx
                return await handler(request)

    def get_middlewares(self):
        return [validation_middleware, self._transaction_middleware]
