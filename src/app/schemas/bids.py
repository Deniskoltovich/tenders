import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models import BidStatus


class CreateBidsSchema(BaseModel):
    name: str
    description: str
    status: BidStatus = BidStatus.CREATED.value
    tender_id: uuid.UUID = Field(
        ..., alias="tenderId", serialization_alias="TenderId"
    )
    organization_id: uuid.UUID = Field(
        ..., alias="organizationId", serialization_alias="OrganizationId"
    )
    creator_username: str = Field(
        ..., alias="creatorUsername", serialization_alias="CreatorUsername"
    )


class BidsOutSchema(BaseModel):
    id: uuid.UUID
    name: str
    status: BidStatus
    author_type: str = Field("User", serialization_alias="authorType")
    author_id: uuid.UUID = Field(..., serialization_alias="authorId")
    version: int
    created_at: datetime = Field(..., serialization_alias="createdAt")

    class Config:
        from_attributes = True


class BidUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
