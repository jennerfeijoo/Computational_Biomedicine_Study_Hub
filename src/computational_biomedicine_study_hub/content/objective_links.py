"""Locale-independent links between learning activities and learning objectives.

The authored text remains localized, while this normalized relation stays stable across
Spanish, English and Danish. Keeping the relation separate avoids duplicating the same
objective identifiers inside every translated activity object.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import AssessmentItem, LearningModule


@dataclass(frozen=True, slots=True)
class ObjectiveLink:
    """Associate one stable activity identifier with one or more objectives."""

    activity_id: str
    objective_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.activity_id.strip():
            raise ValueError("Objective links require a non-empty activity ID.")
        if self.activity_id != self.activity_id.strip():
            raise ValueError("Objective-link activity IDs cannot contain surrounding whitespace.")
        if not self.objective_ids:
            raise ValueError(f"Activity {self.activity_id!r} requires at least one objective.")

        normalized = tuple(objective_id.strip().casefold() for objective_id in self.objective_ids)
        if any(not objective_id for objective_id in normalized):
            raise ValueError(f"Activity {self.activity_id!r} contains an empty objective ID.")
        if any(objective_id != objective_id.strip() for objective_id in self.objective_ids):
            raise ValueError(
                f"Activity {self.activity_id!r} has objective IDs with surrounding whitespace."
            )
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Activity {self.activity_id!r} contains duplicate objective IDs.")


@dataclass(frozen=True, slots=True)
class ObjectiveLinkCatalog:
    """Complete objective mapping for one module's assessable activities."""

    module_id: str
    links: tuple[ObjectiveLink, ...]

    def __post_init__(self) -> None:
        if not self.module_id.strip():
            raise ValueError("Objective-link catalogs require a module ID.")
        if self.module_id != self.module_id.strip():
            raise ValueError("Objective-link module IDs cannot contain surrounding whitespace.")
        if not self.links:
            raise ValueError(f"Module {self.module_id!r} requires objective links.")

        activity_ids = tuple(link.activity_id for link in self.links)
        normalized = tuple(activity_id.casefold() for activity_id in activity_ids)
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Module {self.module_id!r} has duplicate linked activity IDs.")

        local_module_id = self.module_id.rsplit(".", maxsplit=1)[-1]
        valid_prefixes = (f"{self.module_id}.", f"{local_module_id}.")
        out_of_scope = tuple(
            activity_id
            for activity_id in activity_ids
            if not activity_id.startswith(valid_prefixes)
        )
        if out_of_scope:
            raise ValueError(
                f"Module {self.module_id!r} has out-of-scope activity links: "
                + ", ".join(out_of_scope)
            )

    @property
    def activity_ids(self) -> tuple[str, ...]:
        """Return linked activity IDs in authored order."""

        return tuple(link.activity_id for link in self.links)

    def objectives_for(self, activity_id: str) -> tuple[str, ...]:
        """Return the objectives assessed by one activity, or an empty tuple."""

        for link in self.links:
            if link.activity_id == activity_id:
                return link.objective_ids
        return ()

    def validate_against(
        self,
        module: LearningModule,
        objective_question_bank: tuple[AssessmentItem, ...],
    ) -> None:
        """Require exact coverage and valid objective references for a runtime bundle."""

        if module.module_id != self.module_id:
            raise ValueError(
                f"Objective links for {self.module_id!r} cannot validate module "
                f"{module.module_id!r}."
            )

        expected_ids = {
            *(exercise.exercise_id for exercise in module.practice_exercises),
            *(item.item_id for item in module.assessment_items),
            *(item.item_id for item in objective_question_bank),
        }
        actual_ids = set(self.activity_ids)
        missing = sorted(expected_ids - actual_ids)
        unexpected = sorted(actual_ids - expected_ids)
        if missing or unexpected:
            details: list[str] = []
            if missing:
                details.append("missing=" + ", ".join(missing))
            if unexpected:
                details.append("unexpected=" + ", ".join(unexpected))
            raise ValueError(
                f"Objective links for {self.module_id!r} do not exactly cover activities: "
                + "; ".join(details)
            )

        valid_objective_ids = {objective.objective_id for objective in module.objectives}
        invalid_references = sorted(
            {
                objective_id
                for link in self.links
                for objective_id in link.objective_ids
                if objective_id not in valid_objective_ids
            }
        )
        if invalid_references:
            raise ValueError(
                f"Objective links for {self.module_id!r} reference unknown objectives: "
                + ", ".join(invalid_references)
            )


def _link(activity_id: str, *objective_ids: str) -> ObjectiveLink:
    return ObjectiveLink(activity_id=activity_id, objective_ids=tuple(objective_ids))


DM847_M01_OBJECTIVE_LINKS = ObjectiveLinkCatalog(
    module_id="dm847.m01",
    links=(
        # Guided practice
        _link("m01.p01", "m01.o1", "m01.o4"),
        _link("m01.p02", "m01.o2"),
        _link("m01.p03", "m01.o3"),
        _link("m01.p04", "m01.o4", "m01.o6"),
        _link("m01.p05", "m01.o3", "m01.o6"),
        _link("m01.p06", "m01.o4"),
        _link("m01.p07", "m01.o5"),
        _link("m01.p08", "m01.o3"),
        # Complete authored assessment: MCQ 001-005 followed by true/false 011-015.
        _link("dm847.m01.assessment.001", "m01.o3"),
        _link("dm847.m01.assessment.002", "m01.o2"),
        _link("dm847.m01.assessment.003", "m01.o2"),
        _link("dm847.m01.assessment.004", "m01.o3"),
        _link("dm847.m01.assessment.005", "m01.o4"),
        _link("dm847.m01.assessment.006", "m01.o1", "m01.o3"),
        _link("dm847.m01.assessment.007", "m01.o2"),
        _link("dm847.m01.assessment.008", "m01.o3"),
        _link("dm847.m01.assessment.009", "m01.o4"),
        _link("dm847.m01.assessment.010", "m01.o4", "m01.o6"),
        # Randomized objective bank
        _link("dm847.m01.bank.001", "m01.o3"),
        _link("dm847.m01.bank.002", "m01.o2"),
        _link("dm847.m01.bank.003", "m01.o2"),
        _link("dm847.m01.bank.004", "m01.o3"),
        _link("dm847.m01.bank.005", "m01.o4"),
        _link("dm847.m01.bank.006", "m01.o5", "m01.o6"),
        _link("dm847.m01.bank.007", "m01.o5"),
        _link("dm847.m01.bank.008", "m01.o5"),
        _link("dm847.m01.bank.009", "m01.o2", "m01.o6"),
        _link("dm847.m01.bank.010", "m01.o6"),
        _link("dm847.m01.bank.011", "m01.o1", "m01.o3"),
        _link("dm847.m01.bank.012", "m01.o2"),
        _link("dm847.m01.bank.013", "m01.o3"),
        _link("dm847.m01.bank.014", "m01.o4"),
        _link("dm847.m01.bank.015", "m01.o4", "m01.o6"),
        _link("dm847.m01.bank.016", "m01.o5"),
        _link("dm847.m01.bank.017", "m01.o5"),
        _link("dm847.m01.bank.018", "m01.o5"),
        _link("dm847.m01.bank.019", "m01.o2", "m01.o6"),
        _link("dm847.m01.bank.020", "m01.o6"),
    ),
)

_CATALOGS = {DM847_M01_OBJECTIVE_LINKS.module_id: DM847_M01_OBJECTIVE_LINKS}


def objective_links_for_module(module_id: str) -> ObjectiveLinkCatalog | None:
    """Return the complete mapping for one module when it has been authored."""

    return _CATALOGS.get(module_id)


__all__ = [
    "DM847_M01_OBJECTIVE_LINKS",
    "ObjectiveLink",
    "ObjectiveLinkCatalog",
    "objective_links_for_module",
]
