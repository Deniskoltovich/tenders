from sqlalchemy import select

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_by_id(self, user_id):
        return await super().get_by_id(User, user_id)

    async def get_by_username(self, username: str):
        query = select(User).filter(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()
