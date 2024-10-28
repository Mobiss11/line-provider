# tests/test_service.py
import pytest
from app.models.events import EventStatus


@pytest.mark.asyncio
async def test_event_service_create(event_service, sample_event):
    created_event = await event_service.create_event(sample_event)
    assert created_event.event_id == sample_event.event_id

    stored_event = await event_service.get_event(sample_event.event_id)
    assert stored_event is not None
    assert stored_event.coefficient == sample_event.coefficient
    assert stored_event.status == sample_event.status


@pytest.mark.asyncio
async def test_event_service_update_status(event_service, sample_event):
    # Создаем событие
    await event_service.create_event(sample_event)

    # Обновляем статус
    new_status = EventStatus.FIRST_TEAM_WON
    updated_event = await event_service.update_event_status(
        sample_event.event_id,
        new_status
    )

    assert updated_event is not None
    assert updated_event.status == new_status

    # Проверяем, что статус сохранился
    stored_event = await event_service.get_event(sample_event.event_id)
    assert stored_event.status == new_status


@pytest.mark.asyncio
async def test_event_service_get_all(event_service, sample_events):
    # Создаем несколько событий
    for event in sample_events:
        await event_service.create_event(event)

    # Получаем все события
    all_events = await event_service.get_all_events()
    assert len(all_events) == len(sample_events)

    # Проверяем, что все события на месте
    event_ids = {event.event_id for event in sample_events}
    stored_ids = set(all_events.keys())
    assert event_ids == stored_ids
