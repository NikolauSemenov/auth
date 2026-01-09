from aiohttp.web_exceptions import HTTPNoContent, HTTPOk, HTTPCreated
from aiohttp_apigami import docs, json_schema, response_schema, headers_schema

from src.api.v1.base import BaseViews
from src.schemas import auth as schemas


class RegisterView(BaseViews):
    @docs(
        tags=["Auth"],
        summary="Регистрация",
        responses={
            201: {"description": "OK"},
            409: {"description": "Exists"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.RegisterRequestSchema.Schema())
    async def post(self):
        await self._service.create_user(self.request["json"])
        return HTTPCreated()


class LoginView(BaseViews):
    @docs(
        tags=["Authentication"],
        summary="Аутентификация по логину и паролю",
        responses={
            401: {"description": "Unauthorized"},
            404: {"description": "Not found"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.LoginRequestSchema.Schema())
    @response_schema(schemas.LoginResponseSchema.Schema, 200)
    async def post(self):
        return self.response(await self._service.login_user(self.request["json"]))


class LoginEmailView(BaseViews):
    @docs(
        tags=["Authentication"],
        summary="Отправка кода на email",
        responses={
            200: {"description": "OK"},
            401: {"description": "Unauthorized"},
            404: {"description": "Not found"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.LoginEmailRequestSchema.Schema())
    async def post(self):
        await self._service.send_email_code(self.request["json"])
        return HTTPOk()


class VerifyEmailView(BaseViews):
    @docs(
        tags=["Authentication"],
        summary="Аутентификация по email",
        responses={
            404: {"description": "Not found"},
            422: {"description": "Unprocessable Entity"},
            503: {"description": "Service Unavailable"},
        },
    )
    @json_schema(schemas.VerifyEmailRequestSchema.Schema())
    @response_schema(schemas.LoginResponseSchema.Schema, 200)
    async def put(self):
        return self.response(
            await self._service.verify_email_code(self.request["json"])
        )


class VerifyUserView(BaseViews):
    @docs(
        tags=["Authentication"],
        summary="Проверка токена",
        responses={
            200: {"description": "Token valid"},
            401: {"description": "Unauthorized"},
        },
    )
    @headers_schema(schemas.LogoutRequestSchema.Schema())
    @response_schema(schemas.VerifyResponseSchema.Schema, 200)
    async def get(self):
        return self.response(await self._service.verify_user(self.request["headers"]))


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
