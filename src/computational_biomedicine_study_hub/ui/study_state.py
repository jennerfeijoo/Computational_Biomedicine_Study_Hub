"""Serializable language-independent study location."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any


def _integer(value: object, default: int = 0) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


@dataclass(slots=True)
class StudyLocation:
    route: str = ""
    course_code: str = ""
    module_id: str = ""
    tab_index: int = 0
    activity_id: str = ""
    card_id: str = ""
    filters: dict[str, str] = field(default_factory=dict)
    drafts: dict[str, str] = field(default_factory=dict)
    logical_position: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> StudyLocation:
        filters = value.get("filters")
        drafts = value.get("drafts")
        return cls(
            route=str(value.get("route", "")),
            course_code=str(value.get("course_code", "")),
            module_id=str(value.get("module_id", "")),
            tab_index=_integer(value.get("tab_index", 0)),
            activity_id=str(value.get("activity_id", "")),
            card_id=str(value.get("card_id", "")),
            filters=(
                {str(key): str(item) for key, item in filters.items()}
                if isinstance(filters, Mapping)
                else {}
            ),
            drafts=(
                {str(key): str(item) for key, item in drafts.items()}
                if isinstance(drafts, Mapping)
                else {}
            ),
            logical_position=_integer(value.get("logical_position", 0)),
        )


__all__ = ["StudyLocation"]
