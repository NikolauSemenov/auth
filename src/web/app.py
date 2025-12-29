from aiohttp.web import Application
from aiohttp_apigami import setup_aiohttp_apispec

from src.config.settings import Settings
from src.web.middleware import Middleware
from src.web.routes import setup_routes
from src.web.state_app import StateApp


def make_app(settings: Settings):
    app = Application(middlewares=Middleware().get_middlewares())
    setup_aiohttp_apispec(
        app=app,
        title="Auth Service",
        version="1.0.0",
        url="/docs/swagger.json",
        swagger_path=f"{settings.api_prefix}/v1/docs",
    )

    setup_routes(app, settings.api_prefix)

    state = StateApp(settings)
    app["state_app"] = state
    app.cleanup_ctx.append(state.lifespan)

    return app
