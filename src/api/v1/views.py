from aiohttp.web_exceptions import HTTPNoContent, HTTPOk
from aiohttp_apigami import docs, json_schema, response_schema, headers_schema

from src.api.v1.base import BaseViews
from src.schemas import auth as schemas


class RegisterView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Регистрация",
        responses={
            409: {"description": "Exists"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.RegisterRequestSchema.Schema())
    @response_schema(schemas.RegisterResponseSchema.Schema, 201)
    async def post(self):
        return self.response(await self._service.create_user(self.request["json"]), 201)


class LoginView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Аутентификация",
        responses={
            401: {"description": "Unauthorized"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.RegisterRequestSchema.Schema())
    @response_schema(schemas.LoginResponseSchema.Schema, 200)
    async def post(self):
        return self.response(await self._service.login_user(self.request["json"]))


class VerifyUserView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Проверка токена",
        responses={
            200: {"description": "Token valid"},
            401: {"description": "Unauthorized"},
        },
    )
    @headers_schema(schemas.LogoutRequestSchema.Schema())
    async def get(self):
        await self._service.verify_user(self.request["headers"])
        return HTTPOk()


class LogoutView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Выход",
        responses={
            204: {"description": "No content"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @headers_schema(schemas.LogoutRequestSchema.Schema())
    async def delete(self):
        await self._service.logout_user(self.request["headers"])
        return HTTPNoContent()


class GrantTokenView(BaseViews):
    @docs(
        tags=["Admin"],
        summary="Выдача разрешения на использование токена",
        responses={
            200: {"description": "Permission granted"},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.GrantTokenRequestSchema.Schema())
    @headers_schema(schemas.LogoutRequestSchema.Schema())
    async def put(self):
        await self._service.grant_token_permission(
            self.request["json"], self.request["headers"]
        )
        return HTTPOk()
