import datetime
import uuid

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import CreatedUpdatedMixin


class User(Base, CreatedUpdatedMixin):
    __tablename__ = 'employee'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4()
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    organizations = relationship(
        "Organization",
        back_populates="users",
        secondary="organization_responsible",
    )
