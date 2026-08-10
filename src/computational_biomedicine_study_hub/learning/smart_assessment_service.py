"""Reliable module-aware assessment generation and programming relevance."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from ..content.models import LearningModule
from ..integrations.ollama_chat import ChatMessage, ChatRole, OllamaChatClient
from ..storage.ai_learning_store import GeneratedQuestion
from .activity_types import ActivityType
from .ai_study_service import AIStudyService


QUESTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["multiple_choice", "short_reasoning"]},
                    "prompt": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "correct_answer": {"type": "string"},
                    "rationale": {"type": "string"},
                    "rubric": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["type", "prompt", "options", "correct_answer", "rationale", "rubric"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["questions"],
    "additionalProperties": False,
}


class _SelectedModelChatClient:
    """Proxy that makes the model selected in Settings apply to every AI operation."""

    def __init__(self, client: OllamaChatClient, model: str) -> None:
        self._client = client
        self._model = model.strip()

    def chat(self, messages, **kwargs):
        if self._model:
            kwargs["model"] = self._model
        return self._client.chat(messages, **kwargs)


class SmartAssessmentService(AIStudyService):
    """Generate mixed assessments one authored module at a time."""

    def __init__(
        self,
        store,
        *,
        client: OllamaChatClient | None = None,
        model: str = "",
    ) -> None:
        base_client = client or OllamaChatClient()
        super().__init__(store, client=_SelectedModelChatClient(base_client, model))

    def generate_assessment(
        self,
        modules: tuple[LearningModule, ...],
        *,
        count: int = 10,
    ) -> tuple[GeneratedQuestion, ...]:
        if not modules:
            raise ValueError("At least one module is required.")
        if len({module.course_code for module in modules}) != 1:
            raise ValueError("Assessment modules must belong to one course.")

        count = max(2, min(count, 30))
        weights = self.module_weights(modules)
        quotas = _allocate_quotas(count, modules, weights)
        generated: list[GeneratedQuestion] = []

        for module in modules:
            generated.extend(self._generate_for_module(module, quotas[module.module_id], weights[module.module_id]))

        if not generated:
            raise ValueError(
                "No se pudieron generar preguntas válidas. Comprueba Ollama, el modelo seleccionado "
                "y la conexión local."
            )

        result = generated[:count]
        _deterministic_shuffle(result)
        final = tuple(result)
        self.store.save_generated_questions(final)
        return final

    def _generate_for_module(
        self,
        module: LearningModule,
        quota: int,
        weakness_weight: float,
    ) -> tuple[GeneratedQuestion, ...]:
        context = self._module_context(module)
        system = (
            "Generate rigorous study questions ONLY from the supplied authored module. "
            "Create a mixture of multiple-choice and short-reasoning questions. "
            "This request is already scoped to one module, so DO NOT output module metadata. "
            "The visible prompt and rationale MUST NOT contain the module title, module ID, course code, "
            "or phrases such as 'this module' or 'in this topic'. Do not reveal provenance. "
            "For multiple-choice questions provide at least four options and one exact correct answer. "
            "For short_reasoning questions use an empty options array and provide a reference answer plus rubric criteria."
        )
        user = (
            f"Generate exactly {quota} questions. Weakness weight is {weakness_weight:.3f}. "
            "Use the weight only to prioritize reinforcement; never mention it.\n\n"
            f"AUTHORED MODULE CONTENT:\n{context}"
        )
        response = self.client.chat(
            (ChatMessage(ChatRole.SYSTEM, system), ChatMessage(ChatRole.USER, user)),
            temperature=0.35,
            format_schema=QUESTION_SCHEMA,
            num_ctx=32768,
            num_predict=3500,
        )
        payload = self._json(response.content)
        now = datetime.now(UTC).isoformat()
        valid: list[GeneratedQuestion] = []
        for item in payload.get("questions", []):
            question = self._validate_question(item, module, now)
            if question is not None:
                valid.append(question)
        return tuple(valid[:quota])

    def _validate_question(
        self,
        item: object,
        module: LearningModule,
        created_at: str,
    ) -> GeneratedQuestion | None:
        if not isinstance(item, dict):
            return None
        kind = str(item.get("type", "")).strip()
        if kind not in {"multiple_choice", "short_reasoning"}:
            return None
        prompt = str(item.get("prompt", "")).strip()
        answer = str(item.get("correct_answer", "")).strip()
        rationale = str(item.get("rationale", "")).strip()
        options = tuple(str(value).strip() for value in item.get("options", []) if str(value).strip())
        rubric = tuple(str(value).strip() for value in item.get("rubric", []) if str(value).strip())
        if not prompt or not answer or not rationale:
            return None
        if kind == "multiple_choice" and len(options) < 4:
            return None
        if kind == "short_reasoning" and options:
            return None
        if self._mentions_module(prompt, module) or self._mentions_module(rationale, module):
            return None
        return GeneratedQuestion(
            question_id=str(uuid4()),
            course_code=module.course_code,
            module_id=module.module_id,
            question_type=kind,
            prompt=prompt,
            options=options,
            correct_answer=answer,
            rationale=rationale,
            rubric=rubric,
            created_at=created_at,
        )


def programming_exercises(module: LearningModule):
    """Return only authored practice exercises that are explicitly code-reviewable."""

    code_types = {ActivityType.CODE_COMPLETION, ActivityType.CODE_TRACING, ActivityType.DEBUGGING}
    return tuple(
        exercise
        for exercise in module.practice_exercises
        if exercise.activity_type in code_types
    )


def _allocate_quotas(
    count: int,
    modules: tuple[LearningModule, ...],
    weights: dict[str, float],
) -> dict[str, int]:
    count = max(count, len(modules))
    quotas = {module.module_id: 1 for module in modules}
    remaining = count - len(modules)
    ordered = sorted(modules, key=lambda module: weights[module.module_id], reverse=True)
    while remaining:
        for module in ordered:
            if remaining == 0:
                break
            quotas[module.module_id] += 1
            remaining -= 1
    return quotas


def _deterministic_shuffle(questions: list[GeneratedQuestion]) -> None:
    """Interleave questions from different source modules without global random state."""

    questions[:] = questions[::2] + questions[1::2]


__all__ = ["SmartAssessmentService", "programming_exercises"]
