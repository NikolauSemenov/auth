import pytest
from faker import Faker
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.tables import Users
from src.utils.security import hash_password


async def check_create_user(connection_db: AsyncConnection, name: str):
    return await connection_db.scalar(select(Users).where(Users.c.name == name))


@pytest.fixture
def get_fake_data_register(get_fake: Faker) -> dict[str, str]:
    return {"name": get_fake.user_name(), "password": get_fake.password()}


@pytest.fixture
async def create_user(connection_db: AsyncConnection, get_fake_data_register):
    await connection_db.execute(
        insert(Users).values(
            name=get_fake_data_register["name"],
            password=hash_password(get_fake_data_register["password"]),
        )
    )
