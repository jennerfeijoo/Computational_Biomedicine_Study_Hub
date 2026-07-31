"""Authored-context tutoring services for local language models."""

from .adaptive_session import (
    TutorAssistanceLevel,
    TutorSessionSnapshot,
    TutorSessionTurn,
    bounded_history,
)
from .challenge_diagnostic import (
    ChallengeDiagnostic,
    ChallengeDiagnosticCase,
    ChallengeTutorPromptBuilder,
    ChallengeTutorResponse,
    ChallengeTutorService,
)
from .context import (
    ModuleTutorPromptBuilder,
    RankedTutorDocument,
    TutorContext,
    TutorDocumentRetriever,
    TutorPrompt,
)

__all__ = [
    "ChallengeDiagnostic",
    "ChallengeDiagnosticCase",
    "ChallengeTutorPromptBuilder",
    "ChallengeTutorResponse",
    "ChallengeTutorService",
    "ModuleTutorPromptBuilder",
    "RankedTutorDocument",
    "TutorAssistanceLevel",
    "TutorContext",
    "TutorDocumentRetriever",
    "TutorPrompt",
    "TutorSessionSnapshot",
    "TutorSessionTurn",
    "bounded_history",
]
