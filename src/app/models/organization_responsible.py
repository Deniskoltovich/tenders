import uuid

from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OrganizationResponsible(Base):
    __tablename__ = 'organization_responsible'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organization.id", ondelete='CASCADE'), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("employee.id", ondelete='CASCADE'), nullable=False
    )
