"""Deterministic evidence-driven learning-path recommendations.

The path engine reads authored module identities and local objective mastery. It does
not infer mastery from page visits, model feedback, or self-reported completion.
Course-specific assessment workflows remain independently registered by the UI.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from ..content.bmb830 import BUNDLES as BMB830_BUNDLES
from ..content.bmb831 import BUNDLES as BMB831_BUNDLES
from ..content.bundles import ModuleBundle
from ..content.dm847 import BUNDLES as DM847_BUNDLES
from ..content.dm857 import BUNDLES as DM857_BUNDLES
from .progress import MasteryState, ReviewItem


class LearningStage(StrEnum):
    """Evidence-producing phases in one course learning cycle."""

    ORIENT = "orient"
    LEARN = "learn"
    PRACTICE = "practice"
    RETRIEVE = "retrieve"
    TRANSFER = "transfer"
    ASSESS = "assess"
    CONSOLIDATE = "consolidate"


class LearningDestinationKind(StrEnum):
    """Type of application destination for a recommendation."""

    COURSE_SECTION = "course_section"
    REVIEW = "review"
    ASSESSMENT = "assessment"


class RecommendationReason(StrEnum):
    """Stable explanation code for localization and analytics."""

    NO_EVIDENCE = "no_evidence"
    PARTIAL_EVIDENCE = "partial_evidence"
    WEAK_MASTERY = "weak_mastery"
    RETRIEVAL_NEEDED = "retrieval_needed"
    COURSE_READY_FOR_ASSESSMENT = "course_ready_for_assessment"
    TRANSFER_NEEDED = "transfer_needed"
    REVIEW_DUE = "review_due"


class ProgressReader(Protocol):
    """Read-only subset of local progress required by the path engine."""

    def get_mastery(
        self,
        objective_id: str,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> MasteryState | None:
        """Return one objective mastery state."""

    def due_reviews(
        self,
        as_of: datetime,
        *,
        limit: int | None = None,
    ) -> tuple[ReviewItem, ...]:
        """Return objective states currently due for retrieval practice."""


@dataclass(frozen=True, slots=True)
class CourseModulePlan:
    """Stable authored module identity and objective sequence."""

    course_code: str
    module_id: str
    ordinal: int
    objective_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.course_code.strip() or not self.module_id.strip():
            raise ValueError("Learning-path modules require course and module identities.")
        if self.ordinal < 1:
            raise ValueError("Learning-path module ordinals start at one.")
        if not self.objective_ids:
            raise ValueError("Learning-path modules require authored objectives.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError("Learning-path module objectives cannot be duplicated.")


@dataclass(frozen=True, slots=True)
class LearningDestination:
    """Stable route target without importing any UI implementation."""

    kind: LearningDestinationKind
    route: str
    module_id: str | None = None
    section_index: int | None = None
    assessment_id: str | None = None

    def __post_init__(self) -> None:
        if not self.route.strip():
            raise ValueError("Learning destinations require a route.")
        if self.kind is LearningDestinationKind.COURSE_SECTION:
            if self.module_id is None or self.section_index is None:
                raise ValueError("Course destinations require module and section identities.")
            if self.section_index < 0:
                raise ValueError("Course-section indices cannot be negative.")
            if self.assessment_id is not None:
                raise ValueError("Course destinations cannot contain assessment IDs.")
        elif self.kind is LearningDestinationKind.ASSESSMENT:
            if self.assessment_id is None:
                raise ValueError("Assessment destinations require a registered assessment ID.")
            if self.module_id is not None or self.section_index is not None:
                raise ValueError("Assessment destinations cannot contain module locations.")
        elif self.module_id is not None or self.section_index is not None or self.assessment_id is not None:
            raise ValueError("Review destinations use only their application route.")


@dataclass(frozen=True, slots=True)
class LearningPathRecommendation:
    """One deterministic next action and the evidence supporting it."""

    recommendation_id: str
    course_code: str
    stage: LearningStage
    reason: RecommendationReason
    destination: LearningDestination
    module_id: str | None
    objective_ids: tuple[str, ...]
    mastery_ratio: float

    def __post_init__(self) -> None:
        if not self.recommendation_id.strip() or not self.course_code.strip():
            raise ValueError("Learning recommendations require stable identities.")
        if not 0.0 <= self.mastery_ratio <= 1.0:
            raise ValueError("Learning recommendation mastery ratios must be between zero and one.")
        if self.module_id is not None and self.destination.module_id not in {None, self.module_id}:
            raise ValueError("Recommendation and destination module identities must agree.")


@dataclass(frozen=True, slots=True)
class LearningPathSnapshot:
    """Current due-review action plus one recommendation for every course."""

    generated_at: datetime
    due_review: LearningPathRecommendation | None
    course_recommendations: tuple[LearningPathRecommendation, ...]

    def __post_init__(self) -> None:
        if self.generated_at.tzinfo is None or self.generated_at.utcoffset() is None:
            raise ValueError("Learning-path timestamps must be timezone-aware.")
        course_codes = tuple(item.course_code.casefold() for item in self.course_recommendations)
        if len(course_codes) != len(set(course_codes)):
            raise ValueError("Learning-path snapshots require one recommendation per course.")


def _plans_for(course_code: str, bundles: tuple[ModuleBundle, ...]) -> tuple[CourseModulePlan, ...]:
    return tuple(
        CourseModulePlan(
            course_code=course_code,
            module_id=bundle.module.module_id,
            ordinal=ordinal,
            objective_ids=tuple(objective.objective_id for objective in bundle.module.objectives),
        )
        for ordinal, bundle in enumerate(bundles, start=1)
    )


DEFAULT_COURSE_PLANS: tuple[CourseModulePlan, ...] = (
    *_plans_for("DM857", DM857_BUNDLES),
    *_plans_for("DM847", DM847_BUNDLES),
    *_plans_for("BMB830", BMB830_BUNDLES),
    *_plans_for("BMB831", BMB831_BUNDLES),
)


class LearningPathEngine:
    """Recommend authored evidence-producing actions from local objective mastery."""

    def __init__(
        self,
        plans: Iterable[CourseModulePlan] = DEFAULT_COURSE_PLANS,
        *,
        practice_threshold: float = 0.55,
        mastery_threshold: float = 0.75,
    ) -> None:
        if not 0.0 < practice_threshold < mastery_threshold <= 1.0:
            raise ValueError("Learning-path thresholds require 0 < practice < mastery <= 1.")
        ordered = tuple(sorted(plans, key=lambda item: (item.course_code, item.ordinal)))
        if not ordered:
            raise ValueError("Learning-path engines require at least one authored module.")
        module_ids = tuple(item.module_id.casefold() for item in ordered)
        if len(module_ids) != len(set(module_ids)):
            raise ValueError("Learning-path module IDs must be globally unique.")
        per_course: dict[str, list[CourseModulePlan]] = {}
        for item in ordered:
            per_course.setdefault(item.course_code, []).append(item)
        for course_code, course_plans in per_course.items():
            expected = tuple(range(1, len(course_plans) + 1))
            actual = tuple(item.ordinal for item in course_plans)
            if actual != expected:
                raise ValueError(
                    f"Course {course_code!r} learning-path ordinals must be contiguous."
                )
        self._plans = ordered
        self._course_order = tuple(dict.fromkeys(item.course_code for item in plans))
        self._plans_by_course = {
            course_code: tuple(per_course[course_code]) for course_code in self._course_order
        }
        self._practice_threshold = practice_threshold
        self._mastery_threshold = mastery_threshold

    @property
    def course_codes(self) -> tuple[str, ...]:
        """Return courses in the authored display order."""

        return self._course_order

    def snapshot(
        self,
        progress: ProgressReader | None,
        *,
        as_of: datetime,
        assessment_ids: Iterable[str] = (),
    ) -> LearningPathSnapshot:
        """Build current due-review and per-course recommendations."""

        if as_of.tzinfo is None or as_of.utcoffset() is None:
            raise ValueError("Learning-path generation requires a timezone-aware timestamp.")
        available_assessments = frozenset(assessment_ids)
        due = self._due_review(progress, as_of)
        recommendations = tuple(
            self._recommend_course(course_code, progress, available_assessments)
            for course_code in self._course_order
        )
        return LearningPathSnapshot(as_of, due, recommendations)

    def _due_review(
        self,
        progress: ProgressReader | None,
        as_of: datetime,
    ) -> LearningPathRecommendation | None:
        if progress is None:
            return None
        due_items = progress.due_reviews(as_of, limit=1)
        if not due_items:
            return None
        item = due_items[0]
        return LearningPathRecommendation(
            recommendation_id=(
                f"path.review.{item.course_code.casefold()}.{item.module_id}.{item.objective_id}"
            ),
            course_code=item.course_code,
            stage=LearningStage.CONSOLIDATE,
            reason=RecommendationReason.REVIEW_DUE,
            destination=LearningDestination(
                kind=LearningDestinationKind.REVIEW,
                route="review",
            ),
            module_id=item.module_id,
            objective_ids=(item.objective_id,),
            mastery_ratio=item.state.mastery_score,
        )

    def _recommend_course(
        self,
        course_code: str,
        progress: ProgressReader | None,
        assessment_ids: frozenset[str],
    ) -> LearningPathRecommendation:
        plans = self._plans_by_course[course_code]
        for plan in plans:
            states = tuple(
                self._mastery(progress, plan, objective_id)
                for objective_id in plan.objective_ids
            )
            available = tuple(state for state in states if state is not None)
            ratio = self._mastery_ratio(states)
            if not available:
                return self._module_recommendation(
                    plan,
                    LearningStage.ORIENT,
                    RecommendationReason.NO_EVIDENCE,
                    section_index=0,
                    objective_ids=plan.objective_ids,
                    mastery_ratio=0.0,
                )
            missing = tuple(
                objective_id
                for objective_id, state in zip(plan.objective_ids, states, strict=True)
                if state is None
            )
            if missing:
                return self._module_recommendation(
                    plan,
                    LearningStage.LEARN,
                    RecommendationReason.PARTIAL_EVIDENCE,
                    section_index=1,
                    objective_ids=missing,
                    mastery_ratio=ratio,
                )
            weak = tuple(
                objective_id
                for objective_id, state in zip(plan.objective_ids, states, strict=True)
                if state is not None and state.mastery_score < self._practice_threshold
            )
            if weak:
                return self._module_recommendation(
                    plan,
                    LearningStage.PRACTICE,
                    RecommendationReason.WEAK_MASTERY,
                    section_index=3,
                    objective_ids=weak,
                    mastery_ratio=ratio,
                )
            retrieval = tuple(
                objective_id
                for objective_id, state in zip(plan.objective_ids, states, strict=True)
                if state is not None
                and (state.attempts < 2 or state.mastery_score < self._mastery_threshold)
            )
            if retrieval:
                return self._module_recommendation(
                    plan,
                    LearningStage.RETRIEVE,
                    RecommendationReason.RETRIEVAL_NEEDED,
                    section_index=4,
                    objective_ids=retrieval,
                    mastery_ratio=ratio,
                )

        assessment_id = next(
            (
                assessment_id
                for assessment_id in assessment_ids
                if assessment_id.casefold().startswith(f"{course_code.casefold()}.")
            ),
            None,
        )
        if assessment_id is not None:
            return LearningPathRecommendation(
                recommendation_id=f"path.assess.{course_code.casefold()}",
                course_code=course_code,
                stage=LearningStage.ASSESS,
                reason=RecommendationReason.COURSE_READY_FOR_ASSESSMENT,
                destination=LearningDestination(
                    kind=LearningDestinationKind.ASSESSMENT,
                    route="assessments",
                    assessment_id=assessment_id,
                ),
                module_id=None,
                objective_ids=(),
                mastery_ratio=1.0,
            )

        final_plan = plans[-1]
        return self._module_recommendation(
            final_plan,
            LearningStage.TRANSFER,
            RecommendationReason.TRANSFER_NEEDED,
            section_index=3,
            objective_ids=final_plan.objective_ids,
            mastery_ratio=1.0,
        )

    @staticmethod
    def _mastery(
        progress: ProgressReader | None,
        plan: CourseModulePlan,
        objective_id: str,
    ) -> MasteryState | None:
        if progress is None:
            return None
        return progress.get_mastery(
            objective_id,
            course_code=plan.course_code,
            module_id=plan.module_id,
        )

    @staticmethod
    def _mastery_ratio(states: tuple[MasteryState | None, ...]) -> float:
        if not states:
            return 0.0
        return sum(state.mastery_score if state is not None else 0.0 for state in states) / len(
            states
        )

    @staticmethod
    def _module_recommendation(
        plan: CourseModulePlan,
        stage: LearningStage,
        reason: RecommendationReason,
        *,
        section_index: int,
        objective_ids: tuple[str, ...],
        mastery_ratio: float,
    ) -> LearningPathRecommendation:
        return LearningPathRecommendation(
            recommendation_id=(
                f"path.{stage.value}.{plan.course_code.casefold()}.{plan.module_id}"
            ),
            course_code=plan.course_code,
            stage=stage,
            reason=reason,
            destination=LearningDestination(
                kind=LearningDestinationKind.COURSE_SECTION,
                route=f"course/{plan.course_code.casefold()}",
                module_id=plan.module_id,
                section_index=section_index,
            ),
            module_id=plan.module_id,
            objective_ids=objective_ids,
            mastery_ratio=mastery_ratio,
        )


__all__ = [
    "DEFAULT_COURSE_PLANS",
    "CourseModulePlan",
    "LearningDestination",
    "LearningDestinationKind",
    "LearningPathEngine",
    "LearningPathRecommendation",
    "LearningPathSnapshot",
    "LearningStage",
    "ProgressReader",
    "RecommendationReason",
]
