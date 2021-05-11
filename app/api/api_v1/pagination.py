from __future__ import annotations

from typing import Generic, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination import add_pagination, paginate
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from pydantic import BaseModel, conint

from app.core.config import settings

T = TypeVar("T")


class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(
        settings.API_V1_DEFAULT_PAGINATION_SIZE,
        ge=1,
        le=100,
        description="Page size",
    )

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    results: Sequence[T]
    total: conint(ge=0)  # type: ignore
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore

    __params_type__ = Params  # type: ignore

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            results=items, total=total, page=params.page, size=params.size
        )


__all__ = ["add_pagination", "paginate", "AbstractPage", "Page"]
