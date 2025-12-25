import asyncio
from typing import AsyncIterator

import pytest
from alembic import command
from aiohttp.web import Application
from alembic.config import Config as AlembicConfig
from faker import Faker
from pydantic import PostgresDsn
from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy_utils import database_exists, drop_database, create_database

from src.config.settings import Settings
from src.web.app import make_app

faker = Faker()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    settings = Settings()

    url = make_url(settings.postgres_dsn.unicode_string()).set(database="auth-test")
    settings.postgres_dsn = PostgresDsn(url.render_as_string(hide_password=False))
    return settings


@pytest.fixture(scope="session")
def pg_url(test_settings: Settings) -> str:
    return test_settings.postgres_dsn.unicode_string()


@pytest.fixture(scope="session", autouse=True)
def create_db(pg_url):
    sync_url = (
        make_url(pg_url)
        .set(drivername="postgresql")
        .render_as_string(hide_password=False)
    )

    if database_exists(sync_url):
        drop_database(sync_url)
    create_database(sync_url)

    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture
async def get_async_engine(pg_url) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(pg_url, isolation_level="AUTOCOMMIT")
    yield engine
    await engine.dispose()


@pytest.fixture
async def connection_db(get_async_engine) -> AsyncIterator[AsyncConnection]:
    async with get_async_engine.begin() as conn:
        yield conn


@pytest.fixture
def test_app(test_settings: Settings, pg_url) -> Application:
    return make_app(test_settings)


@pytest.fixture
async def client(aiohttp_client, test_app):
    http_client = await aiohttp_client(test_app)
    async with http_client as client:
        yield client


@pytest.fixture
def get_fake() -> Faker:
    return faker
