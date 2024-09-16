from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, model, id: int):
        query = select(model).filter(model.id == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self, model, limit: int = 10, offset: int = 0):
        query = select(model).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, obj):
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, model, id: int, values: dict):
        query = (
            update(model)
            .where(model.id == id)
            .values(**values)
            .execution_options(synchronize_session="fetch")
            .returning(model)
        )
        res = await self.session.execute(query)
        await self.session.flush()
        return res.scalars().first()

    async def delete(self, model, id: int):
        query = (
            delete(model)
            .where(model.id == id)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(query)
        await self.session.flush()
