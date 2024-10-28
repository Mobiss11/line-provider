from fastapi import APIRouter

from app.api.endpoints import events, callbacks

api_router = APIRouter()
api_router.include_router(events.router, tags=["events"])
api_router.include_router(callbacks.router, tags=["callbacks"])
