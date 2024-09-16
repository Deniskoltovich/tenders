import enum
import uuid

from sqlalchemy import UUID, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.mixins import CreatedUpdatedMixin


class TenderStatus(enum.StrEnum):
    CREATED = 'Created'
    PUBLISHED = 'Published'
    CLOSED = 'Closed'


class ServiceType(enum.StrEnum):
    CONSTRUCTION = 'Construction'
    DELIVERY = 'Delivery'
    MANUFACTURE = 'Manufacture'


class TenderBaseFields:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TenderStatus] = mapped_column(
        nullable=False, default=TenderStatus.CREATED.value
    )
    service_type: Mapped[ServiceType] = mapped_column(nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organization.id"), nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employee.id"), nullable=False
    )


class Tenders(Base, TenderBaseFields, CreatedUpdatedMixin):
    __tablename__ = 'tenders'


class TenderHistory(Base, TenderBaseFields, CreatedUpdatedMixin):
    __tablename__ = 'tender_history'

    id: Mapped[uuid] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    tender_id: Mapped[uuid] = mapped_column(UUID, nullable=False)
