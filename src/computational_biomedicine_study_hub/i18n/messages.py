"""Stable translation keys for the application shell and learning reader."""

from __future__ import annotations

from enum import StrEnum


class MessageKey(StrEnum):
    """User-facing messages that must exist in every supported language."""

    APP_NAME = "app.name"
    PRODUCT_NAME = "app.product_name"

    NAV_GENERAL = "nav.section.general"
    NAV_SEMESTER = "nav.section.semester"
    NAV_LEARNING = "nav.section.learning"
    NAV_RESOURCES = "nav.section.resources"
    NAV_SYSTEM = "nav.section.system"
    NAV_HOME = "nav.home"
    NAV_REVIEW = "nav.review"
    NAV_ASSESSMENTS = "nav.assessments"
    NAV_FLASHCARDS = "nav.flashcards"
    NAV_STUDY_LAB = "nav.study_lab"
    NAV_GLOSSARY = "nav.glossary"
    NAV_SETTINGS = "nav.settings"

    PAGE_HOME_TITLE = "page.home.title"
    PAGE_HOME_SUBTITLE = "page.home.subtitle"
    PAGE_REVIEW_TITLE = "page.review.title"
    PAGE_REVIEW_SUBTITLE = "page.review.subtitle"
    PAGE_ASSESSMENTS_TITLE = "page.assessments.title"
    PAGE_ASSESSMENTS_SUBTITLE = "page.assessments.subtitle"
    PAGE_FLASHCARDS_TITLE = "page.flashcards.title"
    PAGE_FLASHCARDS_SUBTITLE = "page.flashcards.subtitle"
    PAGE_STUDY_LAB_TITLE = "page.study_lab.title"
    PAGE_STUDY_LAB_SUBTITLE = "page.study_lab.subtitle"
    PAGE_GLOSSARY_TITLE = "page.glossary.title"
    PAGE_GLOSSARY_SUBTITLE = "page.glossary.subtitle"
    PAGE_SETTINGS_TITLE = "page.settings.title"
    PAGE_SETTINGS_SUBTITLE = "page.settings.subtitle"

    HOME_HEADING = "home.heading"
    HOME_DESCRIPTION = "home.description"
    COURSE_METADATA = "course.metadata"
    COURSE_OPEN = "course.open"

    SETTINGS_LANGUAGE_GROUP = "settings.language.group"
    SETTINGS_LANGUAGE_LABEL = "settings.language.label"
    SETTINGS_LANGUAGE_HELP = "settings.language.help"
    SETTINGS_LANGUAGE_SAVED = "settings.language.saved"

    MODULE_LABEL = "module.label"
    MODULE_TAB_OVERVIEW = "module.tab.overview"
    MODULE_TAB_CONCEPTS = "module.tab.concepts"
    MODULE_TAB_EXAMPLES = "module.tab.examples"
    MODULE_TAB_PRACTICE = "module.tab.practice"
    MODULE_TAB_ASSESSMENT = "module.tab.assessment"
    MODULE_PURPOSE = "module.purpose"
    MODULE_OBJECTIVES = "module.objectives"
    MODULE_STUDY_SEQUENCE = "module.study_sequence"
    MODULE_STUDY_SEQUENCE_TEXT = "module.study_sequence_text"
    MODULE_ESSENTIAL_POINTS = "module.essential_points"
    MODULE_PROBLEM = "module.problem"
    MODULE_REASONING = "module.reasoning"
    MODULE_CODE = "module.code"
    MODULE_EXPECTED_OUTPUT = "module.expected_output"
    MODULE_EXPLANATION = "module.explanation"
    MODULE_OPTIONS = "module.options"
    MODULE_GRADING_CRITERIA = "module.grading_criteria"
    MODULE_QUESTION = "module.question"
    MODULE_PRACTICE_NOTICE = "module.practice_notice"
    MODULE_ASSESSMENT_NOTICE = "module.assessment_notice"

    ACTIVITY_WORKED_EXAMPLE = "activity.worked_example"
    ACTIVITY_FLASHCARD = "activity.flashcard"
    ACTIVITY_MULTIPLE_CHOICE = "activity.multiple_choice"
    ACTIVITY_MULTIPLE_SELECT = "activity.multiple_select"
    ACTIVITY_TRUE_FALSE = "activity.true_false"
    ACTIVITY_FILL_BLANK = "activity.fill_blank"
    ACTIVITY_MATCHING = "activity.matching"
    ACTIVITY_ORDERING = "activity.ordering"
    ACTIVITY_CODE_COMPLETION = "activity.code_completion"
    ACTIVITY_CODE_TRACING = "activity.code_tracing"
    ACTIVITY_DEBUGGING = "activity.debugging"
    ACTIVITY_SHORT_ANSWER = "activity.short_answer"
    ACTIVITY_ORAL_EXPLANATION = "activity.oral_explanation"
    ACTIVITY_DATA_INTERPRETATION = "activity.data_interpretation"
    ACTIVITY_PIPELINE_DESIGN = "activity.pipeline_design"


ALL_MESSAGE_KEYS = frozenset(MessageKey)

__all__ = ["ALL_MESSAGE_KEYS", "MessageKey"]
