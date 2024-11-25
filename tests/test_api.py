from litestar import status_codes
from tests.factories import UserFactory


async def test_get_users(f_client, f_session) -> None:
    await UserFactory.create_async()

    response = await f_client.get("/users")
    assert response.status_code == status_codes.HTTP_200_OK
    assert len(response.json()) == 1
