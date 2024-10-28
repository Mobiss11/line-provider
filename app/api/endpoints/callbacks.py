from fastapi import APIRouter, HTTPException, Depends

from app.services.callbacks import CallbackService
from app.schemas.callbacks import (
    CallbackResponse,
    CallbackRegistration,
    CallbackHealthResponse,
    CallbackListResponse
)
from app.storage.redis import RedisStorage
from app.models.common import StatusEnum

router = APIRouter()


def get_callback_service():
    return CallbackService(RedisStorage())


@router.post("/callbacks/register", response_model=CallbackResponse)
async def register_callback(
        callback: CallbackRegistration,
        service: CallbackService = Depends(get_callback_service)
):
    try:
        await service.register_callback(str(callback.url))
        return CallbackResponse(
            status=StatusEnum.SUCCESS,
            message="Callback успешно зарегистрирован",
            data=callback
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callbacks/health", response_model=CallbackHealthResponse)
async def check_callbacks_health(
        service: CallbackService = Depends(get_callback_service)
):
    """Проверка состояния всех callbacks"""
    try:
        health_status = await service.check_callbacks_health()
        return CallbackHealthResponse(
            status=StatusEnum.SUCCESS,
            message="Проверка здоровья выполнена",
            data=health_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/callbacks/cleanup", response_model=CallbackListResponse)
async def remove_inactive_callbacks(
        service: CallbackService = Depends(get_callback_service)
):
    """Удаление неактивных callbacks"""
    try:
        removed = await service.remove_inactive_callbacks()
        return CallbackListResponse(
            status=StatusEnum.SUCCESS,
            message="Неактивные callbacks удалены",
            data={"removed_callbacks": removed}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callbacks", response_model=CallbackHealthResponse)
async def get_callbacks(
        service: CallbackService = Depends(get_callback_service)
):
    """Получение списка всех зарегистрированных callbacks"""
    try:
        callbacks = await service.get_callbacks()
        return CallbackHealthResponse(
            status=StatusEnum.SUCCESS,
            message="Список callbacks получен",
            data=callbacks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
