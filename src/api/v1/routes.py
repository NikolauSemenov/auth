from aiohttp.web_app import Application

from src.api.v1 import views


def create_v1_routes(app: Application):
    app.router.add_view("/register", views.RegisterView)
    app.router.add_view("/login", views.LoginView)
    app.router.add_view("/logout", views.LogoutView)
    app.router.add_view("/verify", views.VerifyUserView)
