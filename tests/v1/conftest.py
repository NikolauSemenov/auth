import pytest
from faker import Faker
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.repository.tables import Users


@pytest.fixture
def get_fake_data_register(get_fake: Faker) -> dict[str, str]:
    return {
        "login": get_fake.user_name(),
        "password": get_fake.password(),
        "email": get_fake.email(),
        "user_name": get_fake.user_name(),
        "last_name": get_fake.last_name(),
    }


@pytest.fixture
async def create_user(
    connection_db: AsyncConnection,
    get_fake_data_register,
    get_security_token,
    get_fake,
):
    return await connection_db.scalar(
        insert(Users)
        .values(
            user_name=get_fake.user_name(),
            last_name=get_fake.last_name(),
            login=get_fake_data_register["login"],
            password=get_security_token.hash_password(
                get_fake_data_register["password"]
            ),
            is_active=False,
            email=get_fake.email(),
        )
        .returning(Users.c.id)
    )


@pytest.fixture
async def create_uniq_user(
    connection_db: AsyncConnection,
    get_security_token,
    get_fake,
):
    result = await connection_db.execute(
        insert(Users)
        .values(
            user_name=get_fake.user_name(),
            last_name=get_fake.last_name(),
            login=get_fake.name(),
            password=get_security_token.hash_password(get_fake.password()),
            email=get_fake.email(),
        )
        .returning(Users)
    )
    return result.fetchone()


@pytest.fixture
async def create_admin(
    connection_db: AsyncConnection, get_fake_data_register, get_security_token, get_fake
):
    result = await connection_db.execute(
        insert(Users)
        .values(
            user_name=get_fake.user_name(),
            last_name=get_fake.last_name(),
            login=get_fake_data_register["login"],
            password=get_security_token.hash_password(
                get_fake_data_register["password"]
            ),
            email=get_fake.email(),
            is_active=True,
            is_admin=True,
        )
        .returning(Users)
    )
    return result.fetchone()


@pytest.fixture
async def creat_token(create_user, get_security_token):
    return get_security_token.create_access_token(create_user)


@pytest.fixture
async def creat_token_admin(create_admin, get_security_token):
    return get_security_token.create_access_token(create_admin.id)
