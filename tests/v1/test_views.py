from tests.v1.conftest import check_create_user


async def test_register(client, get_prefix_v1, connection_db, get_fake_data_register):
    resp = await client.post(f"{get_prefix_v1}/register", json=get_fake_data_register)
    assert resp.status == 201
    assert await check_create_user(connection_db, get_fake_data_register["name"])


async def test_register_is_user_exists(
    client, get_prefix_v1, get_fake_data_register, create_user
):
    resp = await client.post(f"{get_prefix_v1}/register", json=get_fake_data_register)
    assert resp.status == 409


async def test_login(
    client, get_prefix_v1, get_fake_data_register, create_user
):
    resp = await client.post(f"{get_prefix_v1}/login", json=get_fake_data_register)
    assert resp.status == 200
    result = await resp.json()
    assert result["access_token"]
    assert result["token_type"]


async def test_login_is_unauthorized(
    client, get_prefix_v1, get_fake_data_register
):
    resp = await client.post(f"{get_prefix_v1}/login", json=get_fake_data_register)
    assert resp.status == 401


async def test_verify(client, get_prefix_v1, creat_token):
    resp = await client.get(
        f"{get_prefix_v1}/verify", headers={"Authorization": f"Bearer {creat_token}"}
    )
    assert resp.status == 200


async def test_verify_unauthorized(client, get_prefix_v1, get_fake):
    resp = await client.get(
        f"{get_prefix_v1}/verify",
        headers={"Authorization": f"Bearer {get_fake.cryptocurrency_code()}"},
    )
    assert resp.status == 401


async def test_logout(client, get_prefix_v1, creat_token):
    resp = await client.delete(
        f"{get_prefix_v1}/logout", headers={"Authorization": f"Bearer {creat_token}"}
    )
    assert resp.status == 204



async def test_grand_token(client, get_prefix_v1, creat_token_admin, create_admin):
    resp = await client.put(
        f"{get_prefix_v1}/grand-token", headers={"Authorization": f"Bearer {creat_token_admin}"}, json={"user_id": create_admin}
    )
    assert resp.status == 200


async def test_grand_token_is_forbidden(client, get_prefix_v1, creat_token, create_user):
    resp = await client.put(
        f"{get_prefix_v1}/grand-token", headers={"Authorization": f"Bearer {creat_token}"}, json={"user_id": create_user}
    )
    assert resp.status == 403


async def test_grand_token_is_unauthorized(client, get_prefix_v1, get_fake, create_user):
    resp = await client.put(
        f"{get_prefix_v1}/grand-token", headers={"Authorization": f"Bearer {get_fake.cryptocurrency_code()}"}, json={"user_id": create_user}
    )
    assert resp.status == 401
