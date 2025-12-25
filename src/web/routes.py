from aiohttp.web_app import Application

from src.api.v1.routes import create_v1_routes


def setup_routes(app: Application, path: str):
    create_v1_routes(app, f"{path}/v1")
