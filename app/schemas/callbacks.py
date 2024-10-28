# app/schemas/callbacks.py
from typing import Dict, List
from pydantic import BaseModel, HttpUrl
from app.schemas.responses import DataResponse


class CallbackRegistration(BaseModel):
    url: HttpUrl


class CallbackResponse(DataResponse[CallbackRegistration]):
    pass


class CallbackHealth(BaseModel):
    url: str
    last_active: str
    status: str


class CallbackHealthResponse(DataResponse[Dict[str, dict]]):
    pass


class CallbackListData(BaseModel):
    removed_callbacks: List[str]


class CallbackListResponse(DataResponse[CallbackListData]):
    pass
