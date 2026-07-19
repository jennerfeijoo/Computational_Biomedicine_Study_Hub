"""Typed, UI-independent access to the canonical academic corpus."""

from .catalog import AcademicCatalog
from .loader import AcademicContentError, SemesterContentLoader, default_content_root
from .models import (
    ConceptBlock,
    CourseContent,
    CumulativeAssessment,
    Flashcard,
    GlossaryEntry,
    HiddenTutorSupport,
    LearningObjective,
    LocalizedText,
    ModuleContent,
    ObjectiveQuestion,
    OpenAssessmentItem,
    PracticeExercise,
    WorkedExample,
)

__all__ = [
    "AcademicCatalog",
    "AcademicContentError",
    "ConceptBlock",
    "CourseContent",
    "CumulativeAssessment",
    "Flashcard",
    "GlossaryEntry",
    "HiddenTutorSupport",
    "LearningObjective",
    "LocalizedText",
    "ModuleContent",
    "ObjectiveQuestion",
    "OpenAssessmentItem",
    "PracticeExercise",
    "SemesterContentLoader",
    "WorkedExample",
    "default_content_root",
]
