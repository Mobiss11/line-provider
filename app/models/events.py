# app/models/events.py
from enum import Enum
from pydantic import BaseModel, Field


class EventStatus(str, Enum):
    NEW = "new"
    FIRST_TEAM_WON = "first_team_won"
    SECOND_TEAM_WON = "second_team_won"


class Event(BaseModel):
    event_id: str
    coefficient: float
    deadline: str = Field(description="Формат даты: YYYY-MM-DDTHH:MM:SS, пример: 2024-03-25T12:00:00")
    status: EventStatus = EventStatus.NEW
