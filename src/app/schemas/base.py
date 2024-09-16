from pydantic import BaseModel, Field


class LimitOffsetSchema(BaseModel):
    limit: int = Field(gt=0, default=5)
    offset: int = Field(ge=0, default=0)
