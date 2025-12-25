from aiohttp.web_app import Application

from src.api.v1 import views


def create_v1_routes(app: Application, prefix: str):
    app.router.add_view(rf"{prefix}/register", views.RegisterView)
    app.router.add_view(rf"{prefix}/login", views.LoginView)
    app.router.add_view(rf"{prefix}/logout", views.LogoutView)
    app.router.add_view(rf"{prefix}/verify", views.VerifyUserView)
    app.router.add_view(rf"{prefix}/grand-token", views.GrantTokenView)
