from typing import Dict, Optional, List
from pydantic import BaseModel
from app.models.events import Event, EventStatus
from app.schemas.responses import DataResponse


class EventsList(BaseModel):
    events: List[Event]


class EventsListResponse(DataResponse[EventsList]):
    pass


class EventResponse(DataResponse[Event]):
    pass


class StatusUpdateData(BaseModel):
    event_id: str
    new_status: EventStatus
    event: Event


class StatusUpdateResponse(DataResponse[StatusUpdateData]):
    pass
