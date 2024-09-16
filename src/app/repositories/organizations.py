from app.models import Organization
from app.repositories.base import BaseRepository


class OrganizationsRepository(BaseRepository):
    async def get_by_id(self, organization_id):
        return await super().get_by_id(Organization, organization_id)
