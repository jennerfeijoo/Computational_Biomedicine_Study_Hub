"""Authored academic content and retrieval-ready support material."""

from __future__ import annotations

from .bundles import LocalizedModuleBundle, ModuleBundle, validate_bundle_catalog
from .localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningModule,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)
from .models import (
    AssessmentItem,
    AssessmentOption,
    ConceptBlock,
    LearningModule,
    LearningObjective,
    PracticeExercise,
    TutorKnowledgeDocument,
    TutorSupportPacket,
    WorkedExample,
)

__all__ = [
    "AssessmentItem",
    "AssessmentOption",
    "ConceptBlock",
    "LearningModule",
    "LearningObjective",
    "LocalizedAssessmentItem",
    "LocalizedAssessmentOption",
    "LocalizedConceptBlock",
    "LocalizedLearningModule",
    "LocalizedLearningObjective",
    "LocalizedModuleBundle",
    "LocalizedPracticeExercise",
    "LocalizedText",
    "LocalizedTutorSupportPacket",
    "LocalizedWorkedExample",
    "ModuleBundle",
    "PracticeExercise",
    "TutorKnowledgeDocument",
    "TutorSupportPacket",
    "WorkedExample",
    "validate_bundle_catalog",
]
