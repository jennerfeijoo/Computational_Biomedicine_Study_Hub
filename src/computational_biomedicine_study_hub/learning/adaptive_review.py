"""Adaptive, objective-scoped review sessions built from authored activities."""

from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from functools import lru_cache
from typing import Any, TypeAlias
from uuid import uuid4

from ..content.dm847 import LOCALIZED_BUNDLES as DM847_LOCALIZED_BUNDLES
from ..content.dm857 import LOCALIZED_BUNDLES as DM857_LOCALIZED_BUNDLES
from ..content.models import AssessmentItem, LearningModule, PracticeExercise
from ..content.python_challenges import PythonChallenge, python_challenge_for
from ..i18n.locales import AppLocale
from .objective_assessment import ObjectiveSessionQuestion
from .progress import MasteryState, ReviewItem

ReviewObjectiveKey = tuple[str, str, str]


class ReviewActivityKind(StrEnum):
    """Supported deterministic activity families in one review session."""

    QUESTION = "question"
    PROGRAMMING = "programming"


ReviewActivityKey = tuple[ReviewActivityKind, str, str, str]
_SNAPSHOT_VERSION = 1


class AdaptiveReviewSnapshotError(ValueError):
    """Raised when an active review snapshot cannot be trusted or restored."""


@dataclass(frozen=True, slots=True)
class ReviewQuestionCandidate:
    """One authored bank item explicitly linked to a learning objective."""

    course_code: str
    module_id: str
    objective_ids: tuple[str, ...]
    item: AssessmentItem

    def __post_init__(self) -> None:
        if not self.course_code.strip() or not self.module_id.strip():
            raise ValueError("Review candidates require course and module identifiers.")
        if not self.objective_ids:
            raise ValueError("Review candidates require explicit objective links.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError("Review candidates cannot contain duplicate objective links.")

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.QUESTION

    @property
    def item_id(self) -> str:
        return self.item.item_id

    @property
    def activity_key(self) -> ReviewActivityKey:
        return (self.kind, self.course_code, self.module_id, self.item_id)


@dataclass(frozen=True, slots=True)
class ReviewProgrammingCandidate:
    """One executable practice exercise with explicit objective-linked tests."""

    learning_module: LearningModule
    exercise: PracticeExercise
    challenge: PythonChallenge

    def __post_init__(self) -> None:
        if self.challenge.course_code != self.learning_module.course_code:
            raise ValueError("Programming review candidates must match their course.")
        if self.challenge.module_id != self.learning_module.module_id:
            raise ValueError("Programming review candidates must match their module.")
        if self.challenge.exercise_id != self.exercise.exercise_id:
            raise ValueError("Programming review candidates must match their exercise.")
        if self.challenge.starter_code != self.exercise.starter_code:
            raise ValueError("Programming review candidates require identical starter code.")
        authored_objectives = {
            objective.objective_id for objective in self.learning_module.objectives
        }
        if not set(self.challenge.objective_ids).issubset(authored_objectives):
            raise ValueError("Programming review candidates cannot reference unknown objectives.")
        required_context = (
            self.exercise.prompt,
            self.exercise.solution,
            self.exercise.explanation,
        )
        if any(not value.strip() for value in required_context):
            raise ValueError(
                "Programming review candidates require complete authored feedback context."
            )

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.PROGRAMMING

    @property
    def course_code(self) -> str:
        return self.challenge.course_code

    @property
    def module_id(self) -> str:
        return self.challenge.module_id

    @property
    def objective_ids(self) -> tuple[str, ...]:
        return self.challenge.objective_ids

    @property
    def item_id(self) -> str:
        return self.challenge.exercise_id

    @property
    def activity_key(self) -> ReviewActivityKey:
        return (self.kind, self.course_code, self.module_id, self.item_id)


ReviewActivityCandidate: TypeAlias = ReviewQuestionCandidate | ReviewProgrammingCandidate


@dataclass(frozen=True, slots=True)
class AdaptiveReviewQuestion:
    """One selected objective question with stable randomized display options."""

    primary_key: ReviewObjectiveKey
    candidate: ReviewQuestionCandidate
    question: ObjectiveSessionQuestion

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.QUESTION

    @property
    def activity_key(self) -> ReviewActivityKey:
        return self.candidate.activity_key

    @property
    def item_id(self) -> str:
        return self.candidate.item_id

    @property
    def course_code(self) -> str:
        return self.candidate.course_code

    @property
    def module_id(self) -> str:
        return self.candidate.module_id

    @property
    def objective_ids(self) -> tuple[str, ...]:
        return self.candidate.objective_ids


@dataclass(frozen=True, slots=True)
class AdaptiveReviewProgramming:
    """One selected executable challenge for an objective-scoped review step."""

    primary_key: ReviewObjectiveKey
    candidate: ReviewProgrammingCandidate

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.PROGRAMMING

    @property
    def activity_key(self) -> ReviewActivityKey:
        return self.candidate.activity_key

    @property
    def item_id(self) -> str:
        return self.candidate.item_id

    @property
    def course_code(self) -> str:
        return self.candidate.course_code

    @property
    def module_id(self) -> str:
        return self.candidate.module_id

    @property
    def objective_ids(self) -> tuple[str, ...]:
        return self.candidate.objective_ids


AdaptiveReviewActivity: TypeAlias = AdaptiveReviewQuestion | AdaptiveReviewProgramming


@dataclass(frozen=True, slots=True)
class AdaptiveReviewSummary:
    """Immutable result summary for one completed or exhausted session."""

    answered: int
    correct: int
    target: int
    reviewed_objectives: tuple[ReviewObjectiveKey, ...]
    exhausted: bool
    question_activities: int
    programming_activities: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.answered if self.answered else 0.0


@dataclass(frozen=True, slots=True)
class AdaptiveReviewResultSnapshot:
    """Stable identity and outcome for one accepted session activity."""

    primary_key: ReviewObjectiveKey
    activity_key: ReviewActivityKey
    is_correct: bool


@dataclass(frozen=True, slots=True)
class AdaptiveReviewSessionSnapshot:
    """Serializable, catalog-bound state for one resumable review session."""

    session_id: str
    target_questions: int
    due_items: tuple[ReviewItem, ...]
    results: tuple[AdaptiveReviewResultSnapshot, ...]
    current_primary_key: ReviewObjectiveKey | None
    current_activity_key: ReviewActivityKey | None
    current_option_ids: tuple[str, ...]
    exhausted: bool
    catalog_fingerprint: str
    created_at: datetime
    updated_at: datetime
    draft_source: str | None = None
    pending_programming_result: bool | None = None
    pending_programming_source: str | None = None
    snapshot_version: int = _SNAPSHOT_VERSION

    def __post_init__(self) -> None:
        if self.snapshot_version != _SNAPSHOT_VERSION:
            raise AdaptiveReviewSnapshotError(
                f"Unsupported adaptive review snapshot version {self.snapshot_version}."
            )
        if not self.session_id.strip() or self.session_id != self.session_id.strip():
            raise AdaptiveReviewSnapshotError(
                "Adaptive review snapshots require a stable session ID."
            )
        if self.target_questions < 1:
            raise AdaptiveReviewSnapshotError(
                "Adaptive review snapshots require a positive target."
            )
        due_keys = tuple(item.key for item in self.due_items)
        if not due_keys or len(due_keys) != len(set(due_keys)):
            raise AdaptiveReviewSnapshotError(
                "Adaptive review snapshots require unique due objectives."
            )
        result_keys = tuple(result.activity_key for result in self.results)
        if len(result_keys) != len(set(result_keys)):
            raise AdaptiveReviewSnapshotError(
                "Adaptive review snapshots cannot repeat accepted activities."
            )
        if len(self.results) > self.target_questions:
            raise AdaptiveReviewSnapshotError("Snapshot results cannot exceed the session target.")
        if (self.current_primary_key is None) != (self.current_activity_key is None):
            raise AdaptiveReviewSnapshotError(
                "Current objective and activity identities must be present together."
            )
        if self.current_primary_key is not None and self.current_primary_key not in due_keys:
            raise AdaptiveReviewSnapshotError("The current objective is not part of the session.")
        if self.current_activity_key is not None and self.current_activity_key in result_keys:
            raise AdaptiveReviewSnapshotError("The current activity was already accepted.")
        if self.current_activity_key is None and self.current_option_ids:
            raise AdaptiveReviewSnapshotError("Completed snapshots cannot retain question options.")
        if self.current_activity_key is not None:
            kind = self.current_activity_key[0]
            if kind is ReviewActivityKind.QUESTION and not self.current_option_ids:
                raise AdaptiveReviewSnapshotError(
                    "Current question snapshots require their display option order."
                )
            if kind is ReviewActivityKind.PROGRAMMING and self.current_option_ids:
                raise AdaptiveReviewSnapshotError(
                    "Programming snapshots cannot contain question option IDs."
                )
        if len(self.results) >= self.target_questions and self.current_activity_key is not None:
            raise AdaptiveReviewSnapshotError("A reached session target cannot retain an activity.")
        if len(self.catalog_fingerprint) != 64:
            raise AdaptiveReviewSnapshotError("Invalid adaptive review catalog fingerprint.")
        for name, value in (("created_at", self.created_at), ("updated_at", self.updated_at)):
            if value.tzinfo is None or value.utcoffset() is None:
                raise AdaptiveReviewSnapshotError(f"{name} must be timezone-aware.")
        if self.updated_at < self.created_at:
            raise AdaptiveReviewSnapshotError("Snapshot update time cannot precede creation time.")
        if self.pending_programming_result is not None:
            if self.current_activity_key is None or (
                self.current_activity_key[0] is not ReviewActivityKind.PROGRAMMING
            ):
                raise AdaptiveReviewSnapshotError(
                    "Only a current programming activity may retain a pending result."
                )
            if not self.pending_programming_source:
                raise AdaptiveReviewSnapshotError(
                    "A pending programming result requires its submitted source."
                )
            if self.draft_source != self.pending_programming_source:
                raise AdaptiveReviewSnapshotError(
                    "A pending result must match the currently restored source."
                )
        elif self.pending_programming_source is not None:
            raise AdaptiveReviewSnapshotError(
                "A submitted source cannot be stored without a pending result."
            )

    def to_json(self) -> str:
        """Serialize the snapshot to a deterministic JSON document."""

        payload = {
            "snapshot_version": self.snapshot_version,
            "session_id": self.session_id,
            "target_questions": self.target_questions,
            "due_items": [_review_item_to_payload(item) for item in self.due_items],
            "results": [
                {
                    "primary_key": list(result.primary_key),
                    "activity_key": _activity_key_to_payload(result.activity_key),
                    "is_correct": result.is_correct,
                }
                for result in self.results
            ],
            "current_primary_key": (
                list(self.current_primary_key) if self.current_primary_key is not None else None
            ),
            "current_activity_key": (
                _activity_key_to_payload(self.current_activity_key)
                if self.current_activity_key is not None
                else None
            ),
            "current_option_ids": list(self.current_option_ids),
            "exhausted": self.exhausted,
            "catalog_fingerprint": self.catalog_fingerprint,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "draft_source": self.draft_source,
            "pending_programming_result": self.pending_programming_result,
            "pending_programming_source": self.pending_programming_source,
        }
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    @classmethod
    def from_json(cls, document: str) -> AdaptiveReviewSessionSnapshot:
        """Parse and validate one persisted JSON snapshot."""

        try:
            payload = json.loads(document)
            if not isinstance(payload, dict):
                raise TypeError("Snapshot root must be an object.")
            results_payload = _require_list(payload, "results")
            results = tuple(
                AdaptiveReviewResultSnapshot(
                    primary_key=_objective_key_from_payload(item["primary_key"]),
                    activity_key=_activity_key_from_payload(item["activity_key"]),
                    is_correct=_require_bool(item, "is_correct"),
                )
                for item in results_payload
                if isinstance(item, dict)
            )
            if len(results) != len(results_payload):
                raise TypeError("Every result snapshot must be an object.")
            current_primary_payload = payload.get("current_primary_key")
            current_activity_payload = payload.get("current_activity_key")
            return cls(
                snapshot_version=_require_int(payload, "snapshot_version"),
                session_id=_require_str(payload, "session_id"),
                target_questions=_require_int(payload, "target_questions"),
                due_items=tuple(
                    _review_item_from_payload(item) for item in _require_list(payload, "due_items")
                ),
                results=results,
                current_primary_key=(
                    _objective_key_from_payload(current_primary_payload)
                    if current_primary_payload is not None
                    else None
                ),
                current_activity_key=(
                    _activity_key_from_payload(current_activity_payload)
                    if current_activity_payload is not None
                    else None
                ),
                current_option_ids=tuple(_require_string_list(payload, "current_option_ids")),
                exhausted=_require_bool(payload, "exhausted"),
                catalog_fingerprint=_require_str(payload, "catalog_fingerprint"),
                created_at=datetime.fromisoformat(_require_str(payload, "created_at")),
                updated_at=datetime.fromisoformat(_require_str(payload, "updated_at")),
                draft_source=_optional_str(payload, "draft_source"),
                pending_programming_result=_optional_bool(payload, "pending_programming_result"),
                pending_programming_source=_optional_str(payload, "pending_programming_source"),
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            if isinstance(exc, AdaptiveReviewSnapshotError):
                raise
            raise AdaptiveReviewSnapshotError("Invalid adaptive review snapshot payload.") from exc


@lru_cache(maxsize=len(AppLocale))
def authored_review_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewQuestionCandidate, ...]]:
    """Index authored objective-bank questions by explicit objective identity."""

    indexed: dict[ReviewObjectiveKey, list[ReviewQuestionCandidate]] = {}
    for localized_bundle in (*DM847_LOCALIZED_BUNDLES, *DM857_LOCALIZED_BUNDLES):
        bundle = localized_bundle.materialize(locale)
        links = bundle.objective_links
        if links is None:
            continue
        for item in bundle.objective_question_bank:
            objective_ids = links.objectives_for(item.item_id)
            if not objective_ids:
                continue
            candidate = ReviewQuestionCandidate(
                course_code=bundle.module.course_code,
                module_id=bundle.module.module_id,
                objective_ids=objective_ids,
                item=item,
            )
            for objective_id in objective_ids:
                key = (bundle.module.course_code, bundle.module.module_id, objective_id)
                indexed.setdefault(key, []).append(candidate)

    return {key: tuple(candidates) for key, candidates in indexed.items()}


@lru_cache(maxsize=len(AppLocale))
def authored_review_programming_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewProgrammingCandidate, ...]]:
    """Index executable DM857 challenges by their explicit objective mappings."""

    indexed: dict[ReviewObjectiveKey, list[ReviewProgrammingCandidate]] = {}
    for localized_bundle in DM857_LOCALIZED_BUNDLES:
        bundle = localized_bundle.materialize(locale)
        module = bundle.module
        for exercise in module.practice_exercises:
            if not exercise.starter_code.strip():
                continue
            challenge = python_challenge_for(
                exercise.exercise_id,
                exercise.starter_code,
                locale,
            )
            if challenge is None:
                continue
            candidate = ReviewProgrammingCandidate(
                learning_module=module,
                exercise=exercise,
                challenge=challenge,
            )
            for objective_id in candidate.objective_ids:
                key = (candidate.course_code, candidate.module_id, objective_id)
                indexed.setdefault(key, []).append(candidate)

    return {key: tuple(candidates) for key, candidates in indexed.items()}


@lru_cache(maxsize=len(AppLocale))
def authored_review_activity_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewActivityCandidate, ...]]:
    """Merge explicitly linked questions and programming challenges."""

    merged: dict[ReviewObjectiveKey, list[ReviewActivityCandidate]] = {}
    question_catalog = authored_review_candidates(locale)
    programming_catalog = authored_review_programming_candidates(locale)
    for key, question_candidates in question_catalog.items():
        merged.setdefault(key, []).extend(question_candidates)
    for key, programming_candidates in programming_catalog.items():
        merged.setdefault(key, []).extend(programming_candidates)

    result: dict[ReviewObjectiveKey, tuple[ReviewActivityCandidate, ...]] = {}
    for key, activity_candidates in merged.items():
        activity_keys = tuple(candidate.activity_key for candidate in activity_candidates)
        if len(activity_keys) != len(set(activity_keys)):
            raise ValueError(f"Duplicate adaptive review activities are registered for {key!r}.")
        result[key] = tuple(activity_candidates)
    return result


def review_catalog_fingerprint(
    catalog: Mapping[ReviewObjectiveKey, tuple[ReviewActivityCandidate, ...]],
    objective_keys: tuple[ReviewObjectiveKey, ...],
) -> str:
    """Hash the academic contracts relevant to one session, independent of locale prose."""

    payload: list[dict[str, Any]] = []
    for objective_key in sorted(set(objective_keys)):
        candidates = catalog.get(objective_key, ())
        candidate_payloads: list[dict[str, Any]] = []
        for candidate in sorted(candidates, key=lambda item: item.activity_key):
            base: dict[str, Any] = {
                "kind": candidate.kind.value,
                "course_code": candidate.course_code,
                "module_id": candidate.module_id,
                "item_id": candidate.item_id,
                "objective_ids": list(candidate.objective_ids),
            }
            if isinstance(candidate, ReviewQuestionCandidate):
                base.update(
                    {
                        "activity_type": candidate.item.activity_type.value,
                        "option_ids": [
                            option.option_id for option in candidate.item.option_objects
                        ],
                        "correct_option_ids": list(candidate.item.correct_option_ids),
                    }
                )
            else:
                challenge = candidate.challenge
                base.update(
                    {
                        "starter_code": challenge.starter_code,
                        "timeout_seconds": challenge.timeout_seconds,
                        "visible_cases": [
                            [case.case_id, case.assertion] for case in challenge.visible_cases
                        ],
                        "hidden_cases": [
                            [case.case_id, case.assertion] for case in challenge.hidden_cases
                        ],
                    }
                )
            candidate_payloads.append(base)
        payload.append(
            {
                "objective_key": list(objective_key),
                "candidates": candidate_payloads,
            }
        )
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class AdaptiveReviewSession:
    """Select authored activities from weakness, outcomes and spacing constraints."""

    def __init__(
        self,
        due_items: tuple[ReviewItem, ...],
        *,
        locale: AppLocale,
        target_questions: int = 6,
        rng: random.Random | None = None,
        candidate_catalog: Mapping[
            ReviewObjectiveKey,
            tuple[ReviewActivityCandidate, ...],
        ]
        | None = None,
    ) -> None:
        if target_questions < 1:
            raise ValueError("Adaptive review sessions require at least one target activity.")
        keys = tuple(item.key for item in due_items)
        if len(keys) != len(set(keys)):
            raise ValueError("Adaptive review sessions cannot contain duplicate due objectives.")

        self._due_items = due_items
        self._target_questions = target_questions
        self._rng = rng or random.Random()
        source_catalog = (
            candidate_catalog
            if candidate_catalog is not None
            else authored_review_activity_candidates(locale)
        )
        self._catalog = {key: tuple(candidates) for key, candidates in source_catalog.items()}
        self._validate_catalog()
        self._eligible_items = tuple(item for item in due_items if self._catalog.get(item.key))
        self._unsupported_keys = tuple(
            item.key for item in due_items if not self._catalog.get(item.key)
        )
        self._asked_activity_keys: set[ReviewActivityKey] = set()
        self._results: list[tuple[AdaptiveReviewActivity, bool]] = []
        self._objective_correct: dict[ReviewObjectiveKey, int] = {}
        self._objective_incorrect: dict[ReviewObjectiveKey, int] = {}
        self._current: AdaptiveReviewActivity | None = self._select_next()
        self._exhausted = self._current is None and bool(self._eligible_items)
        self._session_id = uuid4().hex
        self._created_at = datetime.now(UTC)
        self._catalog_fingerprint = review_catalog_fingerprint(self._catalog, keys)

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def catalog_fingerprint(self) -> str:
        return self._catalog_fingerprint

    @property
    def target_questions(self) -> int:
        return self._target_questions

    @property
    def eligible_objective_count(self) -> int:
        return len(self._eligible_items)

    @property
    def unsupported_keys(self) -> tuple[ReviewObjectiveKey, ...]:
        return self._unsupported_keys

    @property
    def current_activity(self) -> AdaptiveReviewActivity | None:
        return self._current

    @property
    def current_question(self) -> AdaptiveReviewQuestion | None:
        current = self._current
        return current if isinstance(current, AdaptiveReviewQuestion) else None

    @property
    def current_programming_activity(self) -> AdaptiveReviewProgramming | None:
        current = self._current
        return current if isinstance(current, AdaptiveReviewProgramming) else None

    @property
    def answered_count(self) -> int:
        return len(self._results)

    @property
    def correct_count(self) -> int:
        return sum(is_correct for _, is_correct in self._results)

    @property
    def is_complete(self) -> bool:
        return self._current is None

    @property
    def can_start(self) -> bool:
        return self._current is not None

    @property
    def summary(self) -> AdaptiveReviewSummary:
        reviewed: list[ReviewObjectiveKey] = []
        for activity, _ in self._results:
            if activity.primary_key not in reviewed:
                reviewed.append(activity.primary_key)
        return AdaptiveReviewSummary(
            answered=self.answered_count,
            correct=self.correct_count,
            target=self._target_questions,
            reviewed_objectives=tuple(reviewed),
            exhausted=self._exhausted,
            question_activities=sum(
                activity.kind is ReviewActivityKind.QUESTION for activity, _ in self._results
            ),
            programming_activities=sum(
                activity.kind is ReviewActivityKind.PROGRAMMING for activity, _ in self._results
            ),
        )

    def record_result(self, item_id: str, is_correct: bool) -> None:
        """Advance after accepting the deterministic result for the current activity."""

        current = self._current
        if current is None:
            raise RuntimeError("The adaptive review session is already complete.")
        if item_id != current.item_id:
            raise ValueError("Review results must match the current authored item.")

        self._results.append((current, is_correct))
        counter = self._objective_correct if is_correct else self._objective_incorrect
        counter[current.primary_key] = counter.get(current.primary_key, 0) + 1
        self._asked_activity_keys.add(current.activity_key)

        if self.answered_count >= self._target_questions:
            self._current = None
            return

        self._current = self._select_next()
        if self._current is None:
            self._exhausted = True

    def to_snapshot(
        self,
        *,
        updated_at: datetime | None = None,
        draft_source: str | None = None,
        pending_programming_result: bool | None = None,
        pending_programming_source: str | None = None,
    ) -> AdaptiveReviewSessionSnapshot:
        """Capture the active session without serializing authored content or tutor dialogue."""

        current_primary_key: ReviewObjectiveKey | None = None
        current_activity_key: ReviewActivityKey | None = None
        current_option_ids: tuple[str, ...] = ()
        if self._current is not None:
            current_primary_key = self._current.primary_key
            current_activity_key = self._current.activity_key
            if isinstance(self._current, AdaptiveReviewQuestion):
                current_option_ids = tuple(
                    option.option_id for option in self._current.question.display_options
                )
            elif draft_source is None:
                draft_source = self._current.candidate.challenge.starter_code

        captured_at = updated_at or datetime.now(UTC)
        return AdaptiveReviewSessionSnapshot(
            session_id=self._session_id,
            target_questions=self._target_questions,
            due_items=self._due_items,
            results=tuple(
                AdaptiveReviewResultSnapshot(
                    primary_key=activity.primary_key,
                    activity_key=activity.activity_key,
                    is_correct=is_correct,
                )
                for activity, is_correct in self._results
            ),
            current_primary_key=current_primary_key,
            current_activity_key=current_activity_key,
            current_option_ids=current_option_ids,
            exhausted=self._exhausted,
            catalog_fingerprint=self._catalog_fingerprint,
            created_at=self._created_at,
            updated_at=captured_at,
            draft_source=draft_source,
            pending_programming_result=pending_programming_result,
            pending_programming_source=pending_programming_source,
        )

    @classmethod
    def from_snapshot(
        cls,
        snapshot: AdaptiveReviewSessionSnapshot,
        *,
        locale: AppLocale,
        rng: random.Random | None = None,
        candidate_catalog: Mapping[
            ReviewObjectiveKey,
            tuple[ReviewActivityCandidate, ...],
        ]
        | None = None,
    ) -> AdaptiveReviewSession:
        """Restore a session only when all referenced academic contracts still match."""

        source_catalog = (
            candidate_catalog
            if candidate_catalog is not None
            else authored_review_activity_candidates(locale)
        )
        catalog = {key: tuple(candidates) for key, candidates in source_catalog.items()}
        fingerprint = review_catalog_fingerprint(
            catalog,
            tuple(item.key for item in snapshot.due_items),
        )
        if fingerprint != snapshot.catalog_fingerprint:
            raise AdaptiveReviewSnapshotError(
                "The authored review catalog changed after this session was saved."
            )

        session = cls.__new__(cls)
        session._due_items = snapshot.due_items
        session._target_questions = snapshot.target_questions
        session._rng = rng or random.Random()
        session._catalog = catalog
        session._validate_catalog()
        session._eligible_items = tuple(
            item for item in snapshot.due_items if session._catalog.get(item.key)
        )
        session._unsupported_keys = tuple(
            item.key for item in snapshot.due_items if not session._catalog.get(item.key)
        )
        session._asked_activity_keys = set()
        session._results = []
        session._objective_correct = {}
        session._objective_incorrect = {}
        session._session_id = snapshot.session_id
        session._created_at = snapshot.created_at
        session._catalog_fingerprint = fingerprint

        for result in snapshot.results:
            activity = session._activity_from_identity(
                result.primary_key,
                result.activity_key,
                (),
            )
            session._results.append((activity, result.is_correct))
            session._asked_activity_keys.add(activity.activity_key)
            counter = (
                session._objective_correct if result.is_correct else session._objective_incorrect
            )
            counter[activity.primary_key] = counter.get(activity.primary_key, 0) + 1

        if snapshot.current_activity_key is None:
            session._current = None
        else:
            assert snapshot.current_primary_key is not None
            session._current = session._activity_from_identity(
                snapshot.current_primary_key,
                snapshot.current_activity_key,
                snapshot.current_option_ids,
            )
        session._exhausted = snapshot.exhausted

        if session._current is None and len(session._results) < session._target_questions:
            if not session._exhausted:
                raise AdaptiveReviewSnapshotError(
                    "An unfinished restored session requires a current activity."
                )
        if session._current is not None:
            available = session._available_candidates(
                next(
                    item
                    for item in session._eligible_items
                    if item.key == session._current.primary_key
                )
            )
            if session._current.activity_key not in {
                candidate.activity_key for candidate in available
            }:
                raise AdaptiveReviewSnapshotError(
                    "The restored current activity is no longer available."
                )
        return session

    def _activity_from_identity(
        self,
        primary_key: ReviewObjectiveKey,
        activity_key: ReviewActivityKey,
        option_ids: tuple[str, ...],
    ) -> AdaptiveReviewActivity:
        candidates = self._catalog.get(primary_key, ())
        candidate = next(
            (item for item in candidates if item.activity_key == activity_key),
            None,
        )
        if candidate is None:
            raise AdaptiveReviewSnapshotError(
                f"Snapshot activity {activity_key!r} is not authorized for {primary_key!r}."
            )
        if isinstance(candidate, ReviewProgrammingCandidate):
            if option_ids:
                raise AdaptiveReviewSnapshotError(
                    "Programming activities cannot restore question option order."
                )
            return AdaptiveReviewProgramming(primary_key=primary_key, candidate=candidate)

        options_by_id = {option.option_id: option for option in candidate.item.option_objects}
        resolved_ids = option_ids or tuple(options_by_id)
        if set(resolved_ids) != set(options_by_id) or len(resolved_ids) != len(options_by_id):
            raise AdaptiveReviewSnapshotError(
                "The restored question option contract no longer matches the catalog."
            )
        return AdaptiveReviewQuestion(
            primary_key=primary_key,
            candidate=candidate,
            question=ObjectiveSessionQuestion(
                item=candidate.item,
                display_options=tuple(options_by_id[option_id] for option_id in resolved_ids),
            ),
        )

    def _select_next(self) -> AdaptiveReviewActivity | None:
        available = tuple(item for item in self._eligible_items if self._available_candidates(item))
        if not available:
            return None

        previous_key = self._results[-1][0].primary_key if self._results else None
        alternatives = tuple(item for item in available if item.key != previous_key)
        selectable = alternatives or available
        selected_item = max(
            selectable,
            key=lambda item: (
                self._priority_score(item),
                -self._due_items.index(item),
            ),
        )
        candidates = self._available_candidates(selected_item)
        scores = {
            candidate.activity_key: self._candidate_score(candidate, selected_item)
            for candidate in candidates
        }
        best_score = max(scores.values())
        preferred = [
            candidate for candidate in candidates if scores[candidate.activity_key] == best_score
        ]
        candidate = self._rng.choice(preferred)
        if isinstance(candidate, ReviewProgrammingCandidate):
            return AdaptiveReviewProgramming(
                primary_key=selected_item.key,
                candidate=candidate,
            )

        options = list(candidate.item.option_objects)
        self._rng.shuffle(options)
        return AdaptiveReviewQuestion(
            primary_key=selected_item.key,
            candidate=candidate,
            question=ObjectiveSessionQuestion(
                item=candidate.item,
                display_options=tuple(options),
            ),
        )

    def _available_candidates(
        self,
        item: ReviewItem,
    ) -> tuple[ReviewActivityCandidate, ...]:
        return tuple(
            candidate
            for candidate in self._catalog[item.key]
            if candidate.activity_key not in self._asked_activity_keys
        )

    def _priority_score(self, item: ReviewItem) -> float:
        key = item.key
        state = item.state
        weakness = (1.0 - state.mastery_score) * 4.0
        lapses = min(state.lapse_count, 5) * 0.25
        incorrect_bonus = self._objective_incorrect.get(key, 0) * 1.5
        correct_penalty = self._objective_correct.get(key, 0) * 0.65
        return weakness + lapses + incorrect_bonus - correct_penalty

    def _candidate_score(
        self,
        candidate: ReviewActivityCandidate,
        item: ReviewItem,
    ) -> float:
        key = item.key
        correct = self._objective_correct.get(key, 0)
        incorrect = self._objective_incorrect.get(key, 0)
        previous_kind = self._results[-1][0].kind if self._results else None
        interleaving_bonus = (
            0.35 if previous_kind is not None and candidate.kind is not previous_kind else 0.0
        )

        if candidate.kind is ReviewActivityKind.PROGRAMMING:
            return (
                item.state.mastery_score * 0.8
                + correct * 1.25
                - incorrect * 0.9
                + interleaving_bonus
            )
        return (
            (1.0 - item.state.mastery_score) * 0.8 + incorrect - correct * 0.25 + interleaving_bonus
        )

    def _validate_catalog(self) -> None:
        for key, candidates in self._catalog.items():
            activity_keys = tuple(candidate.activity_key for candidate in candidates)
            if len(activity_keys) != len(set(activity_keys)):
                raise ValueError(f"Adaptive review catalog {key!r} contains duplicate activities.")
            for candidate in candidates:
                identity = (candidate.course_code, candidate.module_id)
                if identity != key[:2] or key[2] not in candidate.objective_ids:
                    raise ValueError(
                        "Adaptive review candidates must be indexed only by explicit "
                        "objective links."
                    )


def _activity_key_to_payload(key: ReviewActivityKey) -> list[str]:
    return [key[0].value, key[1], key[2], key[3]]


def _activity_key_from_payload(value: object) -> ReviewActivityKey:
    items = _string_sequence(value, expected_length=4)
    return ReviewActivityKind(items[0]), items[1], items[2], items[3]


def _objective_key_from_payload(value: object) -> ReviewObjectiveKey:
    items = _string_sequence(value, expected_length=3)
    return items[0], items[1], items[2]


def _review_item_to_payload(item: ReviewItem) -> dict[str, object]:
    state = item.state
    return {
        "course_code": item.course_code,
        "module_id": item.module_id,
        "state": {
            "objective_id": state.objective_id,
            "mastery_score": state.mastery_score,
            "attempts": state.attempts,
            "consecutive_correct": state.consecutive_correct,
            "lapse_count": state.lapse_count,
            "last_attempt_at": state.last_attempt_at.isoformat(),
            "next_review_at": state.next_review_at.isoformat(),
        },
    }


def _review_item_from_payload(value: object) -> ReviewItem:
    if not isinstance(value, dict):
        raise TypeError("Review item snapshots must be objects.")
    state = value.get("state")
    if not isinstance(state, dict):
        raise TypeError("Review item mastery snapshots must be objects.")
    return ReviewItem(
        course_code=_require_str(value, "course_code"),
        module_id=_require_str(value, "module_id"),
        state=MasteryState(
            objective_id=_require_str(state, "objective_id"),
            mastery_score=_require_float(state, "mastery_score"),
            attempts=_require_int(state, "attempts"),
            consecutive_correct=_require_int(state, "consecutive_correct"),
            lapse_count=_require_int(state, "lapse_count"),
            last_attempt_at=datetime.fromisoformat(_require_str(state, "last_attempt_at")),
            next_review_at=datetime.fromisoformat(_require_str(state, "next_review_at")),
        ),
    )


def _string_sequence(value: object, *, expected_length: int) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) != expected_length:
        raise TypeError(f"Expected a {expected_length}-item string list.")
    if any(not isinstance(item, str) or not item for item in value):
        raise TypeError("Snapshot identity lists require non-empty strings.")
    return tuple(value)


def _require_list(payload: Mapping[str, object], key: str) -> list[object]:
    value = payload[key]
    if not isinstance(value, list):
        raise TypeError(f"Snapshot field {key!r} must be a list.")
    return value


def _require_string_list(payload: Mapping[str, object], key: str) -> list[str]:
    values = _require_list(payload, key)
    if any(not isinstance(value, str) or not value for value in values):
        raise TypeError(f"Snapshot field {key!r} must contain non-empty strings.")
    return [str(value) for value in values]


def _require_str(payload: Mapping[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str) or not value:
        raise TypeError(f"Snapshot field {key!r} must be a non-empty string.")
    return value


def _optional_str(payload: Mapping[str, object], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"Snapshot field {key!r} must be a string or null.")
    return value


def _require_bool(payload: Mapping[str, object], key: str) -> bool:
    value = payload[key]
    if not isinstance(value, bool):
        raise TypeError(f"Snapshot field {key!r} must be boolean.")
    return value


def _optional_bool(payload: Mapping[str, object], key: str) -> bool | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise TypeError(f"Snapshot field {key!r} must be boolean or null.")
    return value


def _require_int(payload: Mapping[str, object], key: str) -> int:
    value = payload[key]
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Snapshot field {key!r} must be an integer.")
    return value


def _require_float(payload: Mapping[str, object], key: str) -> float:
    value = payload[key]
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"Snapshot field {key!r} must be numeric.")
    return float(value)


__all__ = [
    "AdaptiveReviewActivity",
    "AdaptiveReviewProgramming",
    "AdaptiveReviewQuestion",
    "AdaptiveReviewResultSnapshot",
    "AdaptiveReviewSession",
    "AdaptiveReviewSessionSnapshot",
    "AdaptiveReviewSnapshotError",
    "AdaptiveReviewSummary",
    "ReviewActivityCandidate",
    "ReviewActivityKey",
    "ReviewActivityKind",
    "ReviewObjectiveKey",
    "ReviewProgrammingCandidate",
    "ReviewQuestionCandidate",
    "authored_review_activity_candidates",
    "authored_review_candidates",
    "authored_review_programming_candidates",
    "review_catalog_fingerprint",
]
