from aiohttp.web_exceptions import HTTPCreated
from aiohttp_apigami import docs, json_schema

from src.api.v1.base import BaseViews
from src.schemas import auth as schemas


class RegisterView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Регистрация",
        responses={
            201: {"description": "Created"},
            409: {"description": "Exists"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.RegisterRequestSchema.Schema())
    async def post(self):
        await self._service.create_user(self.request["json"])
        return HTTPCreated()
