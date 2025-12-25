from aiohttp.web import Application
from aiohttp_apigami import setup_aiohttp_apispec

from src.config.settings import Settings
from src.repository.base import DbAccessor
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

    setup_routes(app)

    db_accessor = DbAccessor(settings.postgres_dsn.unicode_string())
    app["db_accessor"] = db_accessor
    app.on_shutdown.append(db_accessor.close)

    return app
