import pytest

from app.models.common import StatusEnum


@pytest.mark.asyncio
async def test_register_callback(http_client):
    callback_url = "http://test-callback.com/webhook"
    response = await http_client.post(
        "/callbacks/register",
        json={"url": callback_url}
    )
    assert response.status_code == 200
    assert response.json()["status"] == StatusEnum.SUCCESS