import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import CreatedUpdatedMixin


class OrganizationType(enum.StrEnum):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'


class Organization(Base, CreatedUpdatedMixin):
    __tablename__ = 'organization'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[OrganizationType] = mapped_column(
        Enum(OrganizationType, name="organization_type", create_type=True),
        nullable=False,
    )

    users = relationship(
        "User",
        secondary="organization_responsible",
        back_populates="organizations",
    )
