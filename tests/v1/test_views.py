from tests.v1.conftest import check_create_user


async def test_register(client, connection_db, get_fake_data_register):
    resp = await client.post("/register", json=get_fake_data_register)
    assert resp.status == 201
    assert await check_create_user(connection_db, get_fake_data_register["name"])


async def test_register_is_user_exists(client, get_fake_data_register, create_user):
    resp = await client.post("/register", json=get_fake_data_register)
    assert resp.status == 409


async def test_login(client, connection_db, get_fake_data_register, create_user):
    resp = await client.post("/login", json=get_fake_data_register)
    assert resp.status == 200
    result = await resp.json()
    assert result["access_token"]
    assert result["token_type"]


async def test_login_is_unauthorized(client, connection_db, get_fake_data_register):
    resp = await client.post("/login", json=get_fake_data_register)
    assert resp.status == 401
