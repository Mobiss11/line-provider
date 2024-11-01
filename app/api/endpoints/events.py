from fastapi import APIRouter, HTTPException, Depends
from app.models.events import Event, EventStatus
from app.schemas.events import EventsListResponse, EventResponse, StatusUpdateResponse
from app.services.events import EventService
from app.storage.redis import RedisStorage
from app.models.common import StatusEnum

router = APIRouter()


def get_event_service():
    return EventService(RedisStorage())


@router.get("/events", response_model=EventsListResponse)
async def get_events(
        service: EventService = Depends(get_event_service)
):
    try:
        events = await service.get_all_events()
        return EventsListResponse(
            status=StatusEnum.SUCCESS,
            message="События успешно получены",
            data={"events": events}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/{event_id}", response_model=EventResponse)
async def get_events(
        event_id: str,
        service: EventService = Depends(get_event_service),
):
    try:
        event = await service.get_event(event_id)
        return EventResponse(
            status=StatusEnum.SUCCESS,
            message="Событие успешно получено",
            data=event
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/events", response_model=EventResponse)
async def create_event(
        event: Event,
        service: EventService = Depends(get_event_service)
):
    try:
        created_event = await service.create_event(event)
        return EventResponse(
            status=StatusEnum.SUCCESS,
            message="Событие успешно создано",
            data=created_event
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/events/{event_id}/status", response_model=StatusUpdateResponse)
async def update_event_status(
        event_id: str,
        status: EventStatus,
        service: EventService = Depends(get_event_service)
):
    try:
        updated_event = await service.update_event_status(event_id, status)
        if not updated_event:
            raise HTTPException(
                status_code=404,
                detail=f"Событие с ID {event_id} не найдено"
            )
        return StatusUpdateResponse(
            status=StatusEnum.SUCCESS,
            message="Статус события успешно обновлен",
            data={
                "event_id": event_id,
                "new_status": status,
                "event": updated_event
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
