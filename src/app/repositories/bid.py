import uuid

from sqlalchemy import and_, select

from app.models import Bids, BidsHistory
from app.repositories.base import BaseRepository


class BidRepository(BaseRepository):
    async def create(self, data: dict):
        bid_obj = Bids(**data | {"id": uuid.uuid4()})
        bid = await super().create(bid_obj)
        bid_history_obj = BidsHistory(
            **data | {"bid_id": bid.id, "id": uuid.uuid4()}
        )

        await super().create(bid_history_obj)
        return bid

    async def list_by_user(self, limit: int, offset: int, user_id: str):
        stmt = (
            select(Bids)
            .where(Bids.author_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # async def get_by_id(self, id: int):
    #     stmt = select(Bids).where(Bids.id == id)
    #     result = await self.session.execute(stmt)
    #     return result.scalars().first()
    #
    # async def get_by_status(self, status: str):
    #     stmt = select(Bids).where(Bids.status == status)
    #     result = await self.session.execute(stmt)
    #     return result.scalars().all()

    async def get_by_filters(
        self,
        filters: dict,
        limit: int | None = None,
        offset: int | None = None,
    ):
        stmt = select(Bids).where(
            and_(*[getattr(Bids, k) == v for k, v in filters.items()])
        )
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, id: int, values: dict):
        bid = await super().update(Bids, id, values)
        bid_data = {**bid.__dict__}
        del bid_data['_sa_instance_state']
        del bid_data['id']
        bid_history_obj = BidsHistory(
            **bid_data | {"bid_id": bid.id, "id": uuid.uuid4()}
        )
        print(bid_history_obj.__dict__)
        await super().create(bid_history_obj)
        return bid

    async def get_history_by_filters(self, filters: dict):
        stmt = select(BidsHistory).where(
            and_(*[getattr(BidsHistory, k) == v for k, v in filters.items()])
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, id: int):
        await super().delete(Bids, id)
