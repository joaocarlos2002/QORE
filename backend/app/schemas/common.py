from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


ItemT = TypeVar("ItemT")


class Page(BaseModel, Generic[ItemT]):
    model_config = ConfigDict(from_attributes=True)

    items: list[ItemT]
    total: int = Field(ge=0)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=100)


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, object] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail
