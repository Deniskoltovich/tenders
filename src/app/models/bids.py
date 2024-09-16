import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class BidStatus(StrEnum):
    CREATED = 'Created'
    PUBLISHED = 'Published'
    CANCELLED = 'Cancelled'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'


class BidsBaseFields:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[BidStatus] = mapped_column(
        nullable=False, default=BidStatus.CREATED.value
    )
    author_type: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("employee.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id"), nullable=False
    )
    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organization.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Bids(Base, BidsBaseFields):
    __tablename__ = 'bids'


class BidsHistory(Base, BidsBaseFields):
    __tablename__ = 'BidsHistory'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    bid_id: Mapped[int] = Column(ForeignKey('bids.id'), nullable=False)
