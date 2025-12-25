from aiohttp import web

from src.config.settings import settings
from src.web.app import make_app


def start_app():
    return make_app(settings)


if __name__ == "__main__":
    web.run_app(start_app(), host=settings.host, port=settings.port)
