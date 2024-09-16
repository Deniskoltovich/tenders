from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.repositories.bid import BidRepository
from app.repositories.organizations import OrganizationsRepository
from app.repositories.tender import TenderRepository
from app.repositories.users import UserRepository


class Uow:
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> 'Uow':
        self._session = self._session_factory()

        self.tenders = TenderRepository(self._session)
        self.users = UserRepository(self._session)
        self.organizations = OrganizationsRepository(self._session)
        self.bids = BidRepository(self._session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def shutdown(self) -> None:
        await self._session.close()
