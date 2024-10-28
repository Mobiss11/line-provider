import pytest

from tests.conftest import TEST_EVENTS
from app.models.events import EventStatus
from app.models.common import StatusEnum


@pytest.mark.asyncio
async def test_create_event(http_client, sample_event):
    event_data = {
        "event_id": sample_event.event_id,
        "coefficient": sample_event.coefficient,
        "deadline": sample_event.deadline,
        "status": sample_event.status.value
    }

    response = await http_client.post("/events", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert data["data"]["event_id"] == sample_event.event_id


@pytest.mark.asyncio
async def test_get_events(http_client, event_service, sample_events):
    # Создаем несколько событий
    for event in sample_events:
        await event_service.create_event(event)

    response = await http_client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert len(data["data"]["events"]) == len(TEST_EVENTS)


@pytest.mark.asyncio
async def test_update_event_status(http_client, event_service, sample_event):
    # Создаем событие
    await event_service.create_event(sample_event)

    # Обновляем статус
    new_status = EventStatus.FIRST_TEAM_WON
    response = await http_client.put(
        f"/events/{sample_event.event_id}/status",
        params={"status": new_status.value}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == StatusEnum.SUCCESS
    assert data["data"]["event_id"] == sample_event.event_id
    assert data["data"]["new_status"] == new_status.value
