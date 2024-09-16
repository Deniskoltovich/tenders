import uuid
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.models.tenders import ServiceType, TenderStatus
from app.schemas.tenders import (
    CreateTenderSchema,
    TenderOutSchema,
    UpdateTenderSchema,
)
from app.services.exceptions import (
    TenderNotFoundError,
    UserNotFoundError,
)
from app.services.tender import TenderService

router = APIRouter(prefix="/tenders")


@router.get(
    "/",
    summary="Получение списка тендеров",
    response_model=list[TenderOutSchema],
)
async def list_tenders(
    limit: int = 5,
    offset: int = 0,
    service_type: list[ServiceType] = Query([v.value for v in ServiceType]),
):
    return await TenderService.list_tenders(limit, offset, service_type)


@router.post(
    '/new', summary="Создание нового тендера", response_model=TenderOutSchema
)
async def create_tender(tender: CreateTenderSchema):
    try:
        return await TenderService.create_tender(tender)
    except UserNotFoundError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get(
    "/my",
    summary="Получить тендеры пользователя",
    response_model=list[TenderOutSchema],
)
async def list_tenders_my(username: str, limit: int = 5, offset: int = 0):
    try:
        return await TenderService.list_my_tenders(limit, offset, username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get(
    "/{tenderId}/status",
    summary="Получение статуса тендера",
    response_model=str,
)
async def get_tender_status(tenderId: uuid.UUID, username: str | None = None):
    try:
        tender = await TenderService.get_by_id(tenderId, username)
    except TenderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tender.status


@router.put(
    "/{tenderId}/status",
    summary="Изменить статус тендера по его идентификатору.",
    response_model=TenderOutSchema,
)
async def update_tender_status(
    tenderId: uuid.UUID, status: TenderStatus, username: str | None = None
):
    try:
        tender = await TenderService.update_tender(
            tenderId, {"status": status}, username
        )
    except (TenderNotFoundError, UserNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tender


@router.put(
    "/{tenderId}/edit",
    summary="Изменение параметров существующего тендера.",
    response_model=TenderOutSchema,
)
async def update_tender(
    tenderId: uuid.UUID, username: str, data: UpdateTenderSchema
):
    try:
        tender = await TenderService.update_tender(
            tenderId, UpdateTenderSchema.model_dump(data), username
        )
    except (TenderNotFoundError, UserNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tender


@router.put(
    "/{tenderId}/rollback/{version}",
    summary="Откат версии тендера",
    response_model=TenderOutSchema,
)
async def rollback_tender_version(
    tenderId: uuid.UUID, version: int, username: str
):

    try:
        tender = await TenderService.rollback(tenderId, version, username)
    except (TenderNotFoundError, UserNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return tender
