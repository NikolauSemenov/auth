from aiohttp.web import Application
from aiohttp_apigami import setup_aiohttp_apispec

from src.config.settings import Settings
from src.repository.state.state import AppStateRepository
from src.web.middleware import Middleware
from src.web.routes import setup_routes


def make_app(settings: Settings):
    app = Application(middlewares=Middleware().get_middlewares())
    setup_aiohttp_apispec(
        app=app,
        title="Auth Service",
        version="1.0.0",
        url="/docs/swagger.json",
        swagger_path="/docs",
    )

    setup_routes(app, settings.api_prefix)

    state = AppStateRepository(settings)
    app["state_repository"] = state
    app.cleanup_ctx.append(state.lifespan)

    return app
