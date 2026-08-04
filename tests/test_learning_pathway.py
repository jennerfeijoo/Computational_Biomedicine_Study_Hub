"""Regression tests for deterministic evidence-driven learning-path decisions."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from computational_biomedicine_study_hub.learning.activity_types import StudyCycleStage
from computational_biomedicine_study_hub.learning.pathway import (
    CourseModulePlan,
    LearningDestinationKind,
    LearningPathEngine,
    LearningPathRecommendation,
    RecommendationReason,
)
from computational_biomedicine_study_hub.learning.progress import (
    MasteryState,
    ReviewItem,
)

NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)
PLAN = CourseModulePlan(
    course_code="TEST",
    module_id="test.m01",
    ordinal=1,
    objective_ids=("o1", "o2"),
)


def _state(
    objective_id: str,
    score: float,
    *,
    attempts: int = 2,
    due: bool = False,
) -> MasteryState:
    return MasteryState(
        objective_id=objective_id,
        mastery_score=score,
        attempts=attempts,
        consecutive_correct=min(attempts, 1),
        lapse_count=0,
        last_attempt_at=NOW - timedelta(days=1),
        next_review_at=NOW - timedelta(minutes=1) if due else NOW + timedelta(days=2),
    )


class FakeProgress:
    def __init__(
        self,
        states: dict[tuple[str, str, str], MasteryState] | None = None,
        due: tuple[ReviewItem, ...] = (),
    ) -> None:
        self._states = states or {}
        self._due = due

    def get_mastery(
        self,
        objective_id: str,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> MasteryState | None:
        assert course_code is not None
        assert module_id is not None
        return self._states.get((course_code, module_id, objective_id))

    def due_reviews(
        self,
        as_of: datetime,
        *,
        limit: int | None = None,
    ) -> tuple[ReviewItem, ...]:
        assert as_of == NOW
        return self._due if limit is None else self._due[:limit]


def _recommendation(
    progress: FakeProgress | None,
    assessment_ids: tuple[str, ...] = (),
) -> LearningPathRecommendation:
    engine = LearningPathEngine((PLAN,))
    return engine.snapshot(
        progress,
        as_of=NOW,
        assessment_ids=assessment_ids,
    ).course_recommendations[0]


def test_no_objective_evidence_starts_with_authored_concepts() -> None:
    recommendation = _recommendation(None)

    assert recommendation.stage is StudyCycleStage.CONCEPT
    assert recommendation.reason is RecommendationReason.NO_EVIDENCE
    assert recommendation.destination.kind is LearningDestinationKind.COURSE_SECTION
    assert recommendation.destination.section_index == 0


def test_partial_evidence_returns_to_worked_examples() -> None:
    progress = FakeProgress({("TEST", "test.m01", "o1"): _state("o1", 0.8)})

    recommendation = _recommendation(progress)

    assert recommendation.stage is StudyCycleStage.WORKED_EXAMPLE
    assert recommendation.objective_ids == ("o2",)
    assert recommendation.destination.section_index == 2


def test_weak_mastery_prioritizes_guided_practice() -> None:
    progress = FakeProgress(
        {
            ("TEST", "test.m01", "o1"): _state("o1", 0.4),
            ("TEST", "test.m01", "o2"): _state("o2", 0.8),
        }
    )

    recommendation = _recommendation(progress)

    assert recommendation.stage is StudyCycleStage.GUIDED_PRACTICE
    assert recommendation.objective_ids == ("o1",)
    assert recommendation.destination.section_index == 3


def test_fragile_mastery_prioritizes_retrieval() -> None:
    progress = FakeProgress(
        {
            ("TEST", "test.m01", "o1"): _state("o1", 0.7, attempts=1),
            ("TEST", "test.m01", "o2"): _state("o2", 0.8),
        }
    )

    recommendation = _recommendation(progress)

    assert recommendation.stage is StudyCycleStage.RETRIEVAL
    assert recommendation.objective_ids == ("o1",)
    assert recommendation.destination.section_index == 4


def test_mastered_course_routes_to_registered_assessment() -> None:
    progress = FakeProgress(
        {
            ("TEST", "test.m01", "o1"): _state("o1", 0.9),
            ("TEST", "test.m01", "o2"): _state("o2", 0.85),
        }
    )

    recommendation = _recommendation(progress, ("TEST.exam",))

    assert recommendation.stage is StudyCycleStage.ASSESSMENT
    assert recommendation.destination.kind is LearningDestinationKind.ASSESSMENT
    assert recommendation.destination.assessment_id == "TEST.exam"


def test_due_review_is_exposed_separately_from_course_progression() -> None:
    state = _state("o1", 0.5, due=True)
    progress = FakeProgress(
        {("TEST", "test.m01", "o1"): state},
        (ReviewItem("TEST", "test.m01", state),),
    )
    snapshot = LearningPathEngine((PLAN,)).snapshot(progress, as_of=NOW)

    assert snapshot.due_review is not None
    assert snapshot.due_review.stage is StudyCycleStage.SPACED_REVIEW
    assert snapshot.due_review.destination.kind is LearningDestinationKind.REVIEW


def test_generator_input_preserves_authored_course_order() -> None:
    plans = (
        CourseModulePlan("SECOND", "second.m01", 1, ("o1",)),
        CourseModulePlan("FIRST", "first.m01", 1, ("o1",)),
    )
    engine = LearningPathEngine(plan for plan in plans)

    assert engine.course_codes == ("SECOND", "FIRST")
