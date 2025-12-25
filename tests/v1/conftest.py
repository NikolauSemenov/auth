import pytest
from faker import Faker
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.tables import Users


async def check_create_user(connection_db: AsyncConnection, name: str):
    return await connection_db.scalar(select(Users).where(Users.c.name == name))


@pytest.fixture
def get_fake_data_register(get_fake: Faker) -> dict[str, str]:
    return {"name": get_fake.user_name(), "password": get_fake.password()}


@pytest.fixture
async def create_user(
    connection_db: AsyncConnection, get_fake_data_register, get_security_token
):
    return await connection_db.scalar(
        insert(Users)
        .values(
            name=get_fake_data_register["name"],
            password=get_security_token.hash_password(
                get_fake_data_register["password"]
            ),
            is_active=True,
        )
        .returning(Users.c.id)
    )


@pytest.fixture
async def create_admin(
    connection_db: AsyncConnection, get_fake_data_register, get_security_token
):
    return await connection_db.scalar(
        insert(Users)
        .values(
            name=get_fake_data_register["name"],
            password=get_security_token.hash_password(
                get_fake_data_register["password"]
            ),
            is_active=True,
            is_admin=True,
        )
        .returning(Users.c.id)
    )


@pytest.fixture
async def creat_token(create_user, get_security_token):
    return get_security_token.create_access_token(create_user)


@pytest.fixture
async def creat_token_admin(create_admin, get_security_token):
    return get_security_token.create_access_token(create_admin)
