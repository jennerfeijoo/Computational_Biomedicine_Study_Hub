"""Reusable interactive widgets for the study hub."""

from .adaptive_review_session_widget import AdaptiveReviewSessionWidget
from .appearance_selector import AppearanceSelector
from .challenge_tutor_panel import (
    ChallengeTutorExecutor,
    ChallengeTutorPanel,
    ChallengeTutorRunner,
    QtChallengeTutorExecutor,
)
from .confidence_selector import ConfidenceSelector
from .dm857_practice_widget import DM857GuidedPracticeWidget, DM857PracticeCard
from .floating_tutor_chat import (
    FloatingTutorChat,
    OllamaTutorChatRunner,
    QtTutorChatExecutor,
    TutorChatExecutor,
    TutorChatRunner,
    TutorSelectionEventFilter,
    position_floating_tutor,
)
from .guided_practice_widget import GuidedPracticeCard, GuidedPracticeWidget
from .objective_assessment_widget import ObjectiveAssessmentWidget, ObjectiveQuestionCard
from .python_challenge_widget import PythonChallengeWidget
from .python_lab_widget import PythonLabWidget
from .r_lab_widget import RLabWidget

__all__ = [
    "AdaptiveReviewSessionWidget",
    "AppearanceSelector",
    "ChallengeTutorExecutor",
    "ChallengeTutorPanel",
    "ChallengeTutorRunner",
    "ConfidenceSelector",
    "DM857GuidedPracticeWidget",
    "DM857PracticeCard",
    "FloatingTutorChat",
    "GuidedPracticeCard",
    "GuidedPracticeWidget",
    "ObjectiveAssessmentWidget",
    "ObjectiveQuestionCard",
    "OllamaTutorChatRunner",
    "PythonChallengeWidget",
    "PythonLabWidget",
    "QtChallengeTutorExecutor",
    "QtTutorChatExecutor",
    "RLabWidget",
    "TutorChatExecutor",
    "TutorChatRunner",
    "TutorSelectionEventFilter",
    "position_floating_tutor",
]
