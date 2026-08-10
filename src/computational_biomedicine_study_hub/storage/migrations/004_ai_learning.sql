-- Migration 004: AI-generated learning artifacts.
-- Runtime equivalent: AILearningStore._migrate().
-- This migration is kept as a reviewable SQL contract for local SQLite deployments.

CREATE TABLE IF NOT EXISTS flashcards (
    card_id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    module_id TEXT NOT NULL,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_flashcards_module
    ON flashcards(course_code, module_id, created_at);

CREATE TABLE IF NOT EXISTS generated_questions (
    question_id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    module_id TEXT NOT NULL,
    question_type TEXT NOT NULL CHECK(question_type IN ('multiple_choice', 'short_reasoning')),
    prompt TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    rationale TEXT NOT NULL,
    rubric_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_generated_questions_module
    ON generated_questions(course_code, module_id, created_at);

CREATE TABLE IF NOT EXISTS assessment_attempts (
    attempt_id TEXT PRIMARY KEY,
    question_id TEXT NOT NULL REFERENCES generated_questions(question_id) ON DELETE CASCADE,
    course_code TEXT NOT NULL,
    module_id TEXT NOT NULL,
    is_correct INTEGER NOT NULL CHECK(is_correct IN (0,1)),
    user_answer TEXT NOT NULL,
    feedback TEXT NOT NULL,
    attempted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_assessment_attempts_module
    ON assessment_attempts(course_code, module_id, attempted_at);

CREATE TABLE IF NOT EXISTS module_performance (
    course_code TEXT NOT NULL,
    module_id TEXT NOT NULL,
    attempts INTEGER NOT NULL CHECK(attempts >= 0),
    correct INTEGER NOT NULL CHECK(correct >= 0 AND correct <= attempts),
    updated_at TEXT NOT NULL,
    PRIMARY KEY(course_code, module_id)
);

CREATE TABLE IF NOT EXISTS code_feedback (
    feedback_id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    module_id TEXT NOT NULL,
    exercise_id TEXT NOT NULL,
    source_code TEXT NOT NULL,
    correctness TEXT NOT NULL,
    complexity TEXT NOT NULL,
    best_practices TEXT NOT NULL,
    improvement TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_code_feedback_exercise
    ON code_feedback(course_code, module_id, exercise_id, created_at);

PRAGMA user_version = 1;
