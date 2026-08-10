"""AI generation, grading and reinforcement services for active study features."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from ..content.models import LearningModule
from ..integrations.ollama_chat import ChatMessage, ChatRole, OllamaChatClient
from ..storage.ai_learning_store import AILearningStore, FlashcardRecord, GeneratedQuestion


@dataclass(frozen=True, slots=True)
class CodeFeedback:
    correctness: str
    complexity: str
    best_practices: str
    improvement: str


FLASHCARD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"cards": {"type": "array", "items": {
        "type": "object",
        "properties": {"front": {"type": "string"}, "back": {"type": "string"}},
        "required": ["front", "back"],
        "additionalProperties": False,
    }}},
    "required": ["cards"],
    "additionalProperties": False,
}

QUESTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"questions": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ["multiple_choice", "short_reasoning"]},
            "prompt": {"type": "string"},
            "options": {"type": "array", "items": {"type": "string"}},
            "correct_answer": {"type": "string"},
            "rationale": {"type": "string"},
            "rubric": {"type": "array", "items": {"type": "string"}},
            "module_id": {"type": "string"},
        },
        "required": ["type", "prompt", "options", "correct_answer", "rationale", "rubric", "module_id"],
        "additionalProperties": False,
    }}},
    "required": ["questions"],
    "additionalProperties": False,
}

SHORT_GRADE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"correct": {"type": "boolean"}, "feedback": {"type": "string"}},
    "required": ["correct", "feedback"],
    "additionalProperties": False,
}

CODE_FEEDBACK_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "correctness": {"type": "string"},
        "complexity": {"type": "string"},
        "best_practices": {"type": "string"},
        "improvement": {"type": "string"},
    },
    "required": ["correctness", "complexity", "best_practices", "improvement"],
    "additionalProperties": False,
}


class AIStudyService:
    """Keep AI transport, authored grounding and persistence coordinated."""

    def __init__(self, store: AILearningStore, client: OllamaChatClient | None = None) -> None:
        self.store = store
        self.client = client or OllamaChatClient()

    def generate_flashcards(self, module: LearningModule, *, count: int = 8) -> tuple[FlashcardRecord, ...]:
        count = max(1, min(count, 20))
        context = self._module_context(module)
        response = self.client.chat(
            (ChatMessage(ChatRole.SYSTEM, "Create concise study flashcards only from the supplied authored module."),
             ChatMessage(ChatRole.USER, f"Generate {count} flashcards.\n\n{context}")),
            temperature=0.35,
            format_schema=FLASHCARD_SCHEMA,
        )
        payload = self._json(response.content)
        source_hash = hashlib.sha256(context.encode("utf-8")).hexdigest()
        now = datetime.now(UTC).isoformat()
        cards = tuple(
            FlashcardRecord(
                card_id=str(uuid4()), course_code=module.course_code, module_id=module.module_id,
                front=str(card["front"]).strip(), back=str(card["back"]).strip(),
                source_hash=source_hash, created_at=now,
            )
            for card in payload.get("cards", [])
            if isinstance(card, dict) and str(card.get("front", "")).strip()
            and str(card.get("back", "")).strip()
        )
        if not cards:
            raise ValueError("The AI returned no valid flashcards.")
        self.store.save_flashcards(cards)
        return cards

    def generate_assessment(self, modules: tuple[LearningModule, ...], *, count: int = 10) -> tuple[GeneratedQuestion, ...]:
        if not modules:
            raise ValueError("At least one module is required.")
        if len({module.course_code for module in modules}) != 1:
            raise ValueError("Assessment modules must belong to one course.")
        count = max(2, min(count, 30))
        weights = self.module_weights(modules)
        context = "\n\n".join(self._module_context(module) for module in modules)
        response = self.client.chat(
            (ChatMessage(ChatRole.SYSTEM,
                "Generate rigorous study questions only from the supplied authored content. "
                "Mix multiple-choice and short-answer reasoning. Return source module_id only for internal provenance. "
                "The visible prompt must never contain the source module title or module ID. "
                "Do not mention source modules in rationale text. Prioritize larger weakness weights."),
             ChatMessage(ChatRole.USER,
                f"Generate {count} questions from these modules.\nWeakness weights: "
                f"{json.dumps(weights, ensure_ascii=False, sort_keys=True)}\n\n{context}")),
            temperature=0.55,
            format_schema=QUESTION_SCHEMA,
        )
        payload = self._json(response.content)
        allowed = {module.module_id: module for module in modules}
        now = datetime.now(UTC).isoformat()
        questions: list[GeneratedQuestion] = []
        for item in payload.get("questions", []):
            if not isinstance(item, dict):
                continue
            module_id = str(item.get("module_id", "")).strip()
            kind = str(item.get("type", "")).strip()
            if module_id not in allowed or kind not in {"multiple_choice", "short_reasoning"}:
                continue
            options = tuple(str(option).strip() for option in item.get("options", []) if str(option).strip())
            if kind == "multiple_choice" and len(options) < 2:
                continue
            prompt = str(item.get("prompt", "")).strip()
            answer = str(item.get("correct_answer", "")).strip()
            rationale = str(item.get("rationale", "")).strip()
            rubric = tuple(str(value).strip() for value in item.get("rubric", []) if str(value).strip())
            if not prompt or not answer or not rationale:
                continue
            source_module = allowed[module_id]
            if self._mentions_module(prompt, source_module) or self._mentions_module(rationale, source_module):
                continue
            questions.append(GeneratedQuestion(
                question_id=str(uuid4()), course_code=source_module.course_code, module_id=module_id,
                question_type=kind, prompt=prompt, options=options, correct_answer=answer,
                rationale=rationale, rubric=rubric, created_at=now,
            ))
        if not questions:
            raise ValueError("The AI returned no valid anonymous assessment questions.")
        result = tuple(questions[:count])
        self.store.save_generated_questions(result)
        return result

    def grade_short_answer(self, question: GeneratedQuestion, answer: str) -> tuple[bool, str]:
        response = self.client.chat(
            (ChatMessage(ChatRole.SYSTEM,
                "Grade a student's short reasoning answer against the supplied question, reference answer and rubric. "
                "Do not require exact wording. Explain the key reasoning evidence in the feedback."),
             ChatMessage(ChatRole.USER,
                "Question:\n" + question.prompt + "\n\nReference answer:\n" + question.correct_answer
                + "\n\nRubric:\n" + "\n- ".join(question.rubric)
                + "\n\nStudent answer:\n" + answer)),
            temperature=0.15,
            format_schema=SHORT_GRADE_SCHEMA,
        )
        payload = self._json(response.content)
        return bool(payload.get("correct")), str(payload.get("feedback", "")).strip()

    def grade_multiple_choice(self, question: GeneratedQuestion, answer: str) -> tuple[bool, str]:
        correct = answer.strip().casefold() == question.correct_answer.strip().casefold()
        return correct, question.rationale if correct else f"Incorrect. {question.rationale}"

    def module_weights(self, modules: tuple[LearningModule, ...]) -> dict[str, float]:
        performance = self.store.module_performance(modules[0].course_code)
        raw: dict[str, float] = {}
        for module in modules:
            attempts, correct = performance.get(module.module_id, (0, 0))
            accuracy = correct / attempts if attempts else 0.5
            raw[module.module_id] = max(0.6, min(2.5, 1.0 + (0.5 - accuracy) * 3.0))
        total = sum(raw.values()) or 1.0
        return {key: round(value / total * len(raw), 4) for key, value in raw.items()}

    def review_code(self, *, course_code: str, module: LearningModule, exercise_id: str,
                    prompt: str, source_code: str) -> CodeFeedback:
        response = self.client.chat(
            (ChatMessage(ChatRole.SYSTEM,
                "Review student code for the supplied educational exercise. Return exactly four structured fields. "
                "Do not invent runtime results. Analyze algorithmic complexity from the code shown. The improvement "
                "may include rewritten code, but explain why it is better."),
             ChatMessage(ChatRole.USER,
                f"Course: {course_code}\nModule: {module.title}\nExercise: {exercise_id}\n"
                f"Problem:\n{prompt}\n\nStudent code:\n{source_code}")),
            temperature=0.2,
            format_schema=CODE_FEEDBACK_SCHEMA,
        )
        payload = self._json(response.content)
        feedback = CodeFeedback(
            correctness=str(payload["correctness"]).strip(), complexity=str(payload["complexity"]).strip(),
            best_practices=str(payload["best_practices"]).strip(), improvement=str(payload["improvement"]).strip(),
        )
        self.store.save_code_feedback(
            course_code=course_code, module_id=module.module_id, exercise_id=exercise_id,
            source_code=source_code, correctness=feedback.correctness, complexity=feedback.complexity,
            best_practices=feedback.best_practices, improvement=feedback.improvement,
        )
        return feedback

    @staticmethod
    def _module_context(module: LearningModule) -> str:
        """Build bounded authored grounding without leaking reference answers to generation."""
        sections = [
            f"Course: {module.course_code}", f"Module ID: {module.module_id}",
            f"Title: {module.title}", f"Summary: {module.summary}",
            "Objectives:\n- " + "\n- ".join(o.statement for o in module.objectives),
        ]
        sections.extend(
            f"Concept: {c.title}\n{c.body}\nKey points:\n- " + "\n- ".join(c.key_points)
            for c in module.concepts
        )
        sections.extend(
            f"Worked example: {e.title}\nProblem: {e.problem}\nReasoning:\n- " + "\n- ".join(e.reasoning)
            for e in module.worked_examples
        )
        sections.extend(
            f"Practice prompt: {e.prompt}\nActivity: {e.activity_type.value}"
            for e in module.practice_exercises
        )
        sections.extend(
            f"Assessment prompt: {i.prompt}\nType: {i.activity_type.value}\nOptions: " + " | ".join(i.options)
            for i in module.assessment_items
        )
        return "\n\n".join(sections)[:28_000]

    @staticmethod
    def _mentions_module(text: str, module: LearningModule) -> bool:
        normalized = text.casefold()
        return any(value.casefold() in normalized for value in (module.module_id, module.title) if value.strip())

    @staticmethod
    def _json(content: str) -> dict[str, Any]:
        payload = json.loads(content)
        if not isinstance(payload, dict):
            raise ValueError("AI structured response must be a JSON object.")
        return payload


__all__ = ["AIStudyService", "CodeFeedback"]
