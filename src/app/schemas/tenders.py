import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.tenders import ServiceType, TenderStatus


class CreateTenderSchema(BaseModel):
    name: str
    description: str
    service_type: ServiceType = Field(
        ..., alias="serviceType", serialization_alias="serviceType"
    )
    status: TenderStatus = TenderStatus.CREATED.value
    organization_id: uuid.UUID = Field(
        ..., alias="organizationId", serialization_alias="organizationId"
    )
    creator_username: str = Field(
        ..., alias="creatorUsername", serialization_alias="creatorUsername"
    )


class TenderOutSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    service_type: ServiceType = Field(..., serialization_alias="serviceType")
    status: TenderStatus = TenderStatus.CREATED.value
    version: int
    created_at: datetime = Field(..., serialization_alias="createdAt")

    class Config:
        from_attributes = True


class UpdateTenderSchema(BaseModel):
    name: str | None
    description: str | None
    service_type: ServiceType | None = Field(
        None, alias="serviceType", serialization_alias="serviceType"
    )
