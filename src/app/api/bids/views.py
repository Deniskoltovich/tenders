import uuid

from fastapi import APIRouter, HTTPException

from app.models import BidStatus
from app.schemas.bids import (
    BidsOutSchema,
    BidUpdateSchema,
    CreateBidsSchema,
)
from app.services.bid import BidService
from app.services.exceptions import (
    BidNotFoundError,
    TenderNotFoundError,
    UserNotFoundError,
)

router = APIRouter(prefix="/bids")


@router.post(
    "/new", summary="Создание нового предложения", response_model=BidsOutSchema
)
async def create_new_bid(bid: CreateBidsSchema):
    try:
        return await BidService.create_bid(bid)
    except (UserNotFoundError, TenderNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/my",
    summary="Получение списка предложений текущего пользователя.",
    response_model=list[BidsOutSchema],
)
async def my_bids(
    limit: int = 5, offset: int = 0, username: str | None = None
):
    try:
        return await BidService.list_my(
            limit=limit, offset=offset, username=username
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{tenderId}/list",
    summary="Получение предложений, связанных с указанным тендером.",
    response_model=list[BidsOutSchema],
)
async def list_bids_by_tender(
    tenderId: uuid.UUID, username: str, limit: int = 5, offset: int = 0
):
    try:
        return await BidService.list_by_tender(
            limit=limit, offset=offset, username=username, tender_id=tenderId
        )
    except (UserNotFoundError, TenderNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{bidId}/status",
    summary="Получение текущего статуса предложения",
    response_model=str,
)
async def get_bids_status(bidId: uuid.UUID, username: str):
    try:
        return await BidService.get_bid_status(bidId, username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BidNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{bidID}/status",
    summary="Изменение статуса предложения",
    response_model=BidsOutSchema,
)
async def update_bids_status(
    bidID: uuid.UUID, status: BidStatus, username: str
):
    try:
        return await BidService.update_bid_status(
            bidID, username, status.value
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BidNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{bidID}/edit",
    summary="Редактирование параметров предложения",
    response_model=BidsOutSchema,
)
async def update_bids_edit(
    bidID: uuid.UUID, username: str, bid: BidUpdateSchema
):
    try:
        return await BidService.update_bid(bidID, username, bid)
    except UserNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BidNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{bidID}/rollback/{version}",
    summary="Откат версии предложения",
    response_model=BidsOutSchema,
)
async def rollback_bid(bidID: uuid.UUID, version: int, username: str):
    try:
        return await BidService.rollback(bidID, version, username)
    except UserNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BidNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
