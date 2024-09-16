import uuid
from datetime import datetime

from app.repositories.unit_of_work import Uow
from app.schemas.bids import (
    BidsOutSchema,
    BidUpdateSchema,
    CreateBidsSchema,
)
from app.services.exceptions import (
    BidNotFoundError,
    TenderNotFoundError,
    UserNotFoundError,
)
from settings.db import async_session


class BidService:
    @staticmethod
    async def create_bid(bid: CreateBidsSchema) -> BidsOutSchema:
        bid_data = bid.model_dump()
        bid_data['created_at'] = datetime.now()
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(
                bid_data.pop('creator_username')
            )
            if not related_user:
                raise UserNotFoundError("User not found")
            related_tender = await uow.tenders.get_by_filters(
                {"id": bid.tender_id}
            )
            if not related_tender:
                raise TenderNotFoundError("Tender not found")

            bid_obj = await uow.bids.create(
                bid_data
                | {"author_id": related_user.id, "author_type": "User"}
            )
            await uow.commit()

            return BidsOutSchema.model_validate(bid_obj)

    @staticmethod
    async def list_my(
        limit: int, offset: int, username: str | None
    ) -> list[BidsOutSchema]:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")
            bids = await uow.bids.list_by_user(limit, offset, related_user.id)
            return [BidsOutSchema.model_validate(obj) for obj in bids]

    @staticmethod
    async def list_by_tender(
        limit: int, offset: int, username: str, tender_id: uuid.UUID
    ) -> list[BidsOutSchema]:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")
            related_tender = await uow.tenders.get_by_filters(
                {"id": tender_id, "user_id": related_user.id}
            )
            if not related_tender:
                raise TenderNotFoundError("Tender not found")

            bids = await uow.bids.get_by_filters(
                limit=limit,
                offset=offset,
                filters={"tender_id": tender_id, "author_id": related_user.id},
            )

            return [BidsOutSchema.model_validate(obj) for obj in bids]

    @staticmethod
    async def get_bid_status(bid_id: uuid.UUID, username: str) -> str:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")
            bid = await uow.bids.get_by_filters(
                {"id": bid_id, "author_id": related_user.id}
            )
            if not bid:
                raise BidNotFoundError("Bid not found")
            return bid[0].status

    @staticmethod
    async def update_bid_status(
        bid_id: uuid.UUID, username: str, status: str
    ) -> BidsOutSchema:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")

            bid = await uow.bids.get_by_filters(
                {"id": bid_id, "author_id": related_user.id}
            )
            if not bid:
                raise BidNotFoundError("Bid not found")

            updated_bid = await uow.bids.update(
                bid[0].id, {"status": status, "version": bid[0].version + 1}
            )
            await uow.commit()
            return BidsOutSchema.model_validate(updated_bid)

    @staticmethod
    async def update_bid(
        bid_id: uuid.UUID, username: str, bid_schema: BidUpdateSchema
    ) -> BidsOutSchema:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")

            bid = await uow.bids.get_by_filters(
                {"id": bid_id, "author_id": related_user.id}
            )
            if not bid:
                raise BidNotFoundError("Bid not found")

            values = {
                k: v
                for k, v in bid_schema.model_dump().items()
                if v is not None
            }
            if not any(values.values()):
                return BidsOutSchema.model_validate(bid)
            updated_bid = await uow.bids.update(
                bid[0].id, values | {"version": bid[0].version + 1}
            )
            await uow.commit()
            return BidsOutSchema.model_validate(updated_bid)

    @staticmethod
    async def rollback(
        bid_id: uuid.UUID, version: int, username: str
    ) -> BidsOutSchema:
        async with Uow(async_session) as uow:
            related_user = await uow.users.get_by_username(username)
            if not related_user:
                raise UserNotFoundError("User not found")

            bid = await uow.bids.get_history_by_filters(
                {
                    'bid_id': bid_id,
                    'author_id': related_user.id,
                    "version": version,
                }
            )
            if not bid:
                raise BidNotFoundError(
                    f"Big with version {version} does not exist"
                )

            bid_data = bid[0].__dict__
            del bid_data['_sa_instance_state']
            del bid_data['id']
            bid_id = bid_data.pop('bid_id')
            rollbacked_bid = await uow.bids.update(bid_id, bid_data)
            await uow.commit()
            return BidsOutSchema.model_validate(rollbacked_bid)
