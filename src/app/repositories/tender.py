import uuid

from sqlalchemy import and_, select

from app.models.tenders import ServiceType, TenderHistory, Tenders
from app.repositories.base import BaseRepository


class TenderRepository(BaseRepository):
    async def list(
        self, limit: int, offset: int, service_types: list[ServiceType]
    ):
        stmt = (
            select(Tenders)
            .where(Tenders.service_type.in_(service_types))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: dict):
        tender_obj = Tenders(**data | {"id": uuid.uuid4()})
        tender = await super().create(tender_obj)
        tender_history_obj = TenderHistory(
            **data | {"tender_id": tender.id, "id": uuid.uuid4()}
        )

        await super().create(tender_history_obj)
        return tender

    async def list_by_user(self, limit: int, offset: int, user_id: str):
        stmt = (
            select(Tenders)
            .where(Tenders.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # async def get_by_id(self, id: int):
    #     stmt = select(Tenders).where(Tenders.id == id)
    #     result = await self.session.execute(stmt)
    #     return result.scalars().first()
    #
    # async def get_by_status(self, status: str):
    #     stmt = select(Tenders).where(Tenders.status == status)
    #     result = await self.session.execute(stmt)
    #     return result.scalars().all()

    async def get_by_filters(self, filters: dict):
        stmt = select(Tenders).where(
            and_(*[getattr(Tenders, k) == v for k, v in filters.items()])
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, id: int, values: dict):
        tender = await super().update(Tenders, id, values)
        tender_data = {**tender.__dict__}
        del tender_data['_sa_instance_state']
        tender_history_obj = TenderHistory(
            **tender_data | {"tender_id": tender.id, "id": uuid.uuid4()}
        )
        await super().create(tender_history_obj)
        return tender

    async def get_history_by_filters(self, filters: dict):
        stmt = select(TenderHistory).where(
            and_(*[getattr(TenderHistory, k) == v for k, v in filters.items()])
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, id: int):
        await super().delete(Tenders, id)
