"""Extensible ``ActivityType -> ActivityRenderer`` registry."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from PySide6.QtWidgets import QWidget

from ...content.models import AssessmentItem
from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.activity_types import ActivityType
from .widgets import (
    ActivityWidget,
    ClozeChoiceActivityWidget,
    FillBlankActivityWidget,
    MatchingActivityWidget,
    MultipleChoiceActivityWidget,
    OpenResponseActivityWidget,
    OrderingActivityWidget,
)


class ActivityRenderer(Protocol):
    """Callable that constructs one interactive widget for an authored item."""

    def __call__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale,
        parent: QWidget | None,
    ) -> ActivityWidget:
        """Render one assessment item."""


class ActivityRendererRegistry:
    """Validated registry with no course-specific or text-specific dispatch."""

    def __init__(self) -> None:
        self._renderers: dict[ActivityType, ActivityRenderer] = {}

    def register(self, activity_type: ActivityType, renderer: ActivityRenderer) -> None:
        if activity_type in self._renderers:
            raise ValueError(f"Renderer already registered for {activity_type.value!r}.")
        self._renderers[activity_type] = renderer

    def render(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> ActivityWidget:
        try:
            renderer = self._renderers[item.activity_type]
        except KeyError as exc:
            raise KeyError(f"No renderer registered for {item.activity_type.value!r}.") from exc
        return renderer(item, locale=locale, parent=parent)

    def supports(self, activity_type: ActivityType) -> bool:
        return activity_type in self._renderers

    def __iter__(self) -> Iterator[ActivityType]:
        return iter(self._renderers)


def _widget_renderer(
    widget_type: type[ActivityWidget],
    **fixed_arguments: object,
) -> ActivityRenderer:
    def render(
        item: AssessmentItem,
        *,
        locale: AppLocale,
        parent: QWidget | None,
    ) -> ActivityWidget:
        return widget_type(
            item,
            locale=locale,
            parent=parent,
            **fixed_arguments,
        )

    return render


def create_default_activity_registry() -> ActivityRendererRegistry:
    """Register every current activity family explicitly."""
    registry = ActivityRendererRegistry()
    registry.register(
        ActivityType.MULTIPLE_CHOICE,
        _widget_renderer(MultipleChoiceActivityWidget),
    )
    registry.register(
        ActivityType.MULTIPLE_SELECT,
        _widget_renderer(MultipleChoiceActivityWidget, multiple=True),
    )
    registry.register(
        ActivityType.TRUE_FALSE,
        _widget_renderer(MultipleChoiceActivityWidget),
    )
    registry.register(
        ActivityType.FILL_IN_THE_BLANK,
        _widget_renderer(FillBlankActivityWidget),
    )
    registry.register(
        ActivityType.CLOZE_CHOICE,
        _widget_renderer(ClozeChoiceActivityWidget),
    )
    registry.register(ActivityType.MATCHING, _widget_renderer(MatchingActivityWidget))
    registry.register(ActivityType.ORDERING, _widget_renderer(OrderingActivityWidget))

    open_response_types = (
        ActivityType.WORKED_EXAMPLE,
        ActivityType.FLASHCARD,
        ActivityType.CODE_COMPLETION,
        ActivityType.CODE_TRACING,
        ActivityType.DEBUGGING,
        ActivityType.SHORT_ANSWER,
        ActivityType.ORAL_EXPLANATION,
        ActivityType.DATA_INTERPRETATION,
        ActivityType.PIPELINE_DESIGN,
    )
    open_renderer = _widget_renderer(OpenResponseActivityWidget)
    for activity_type in open_response_types:
        registry.register(activity_type, open_renderer)
    return registry


__all__ = [
    "ActivityRenderer",
    "ActivityRendererRegistry",
    "create_default_activity_registry",
]
