"""Persistent Socratic oral-exam practice for BMB830."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QSettings,
    Qt,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...content.bmb830 import LOCALIZED_BUNDLES
from ...i18n.bmb830_oral_copy import (
    BMB830OralCopyKey,
    bmb830_oral_criterion_text,
    bmb830_oral_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...integrations import (
    DEFAULT_CHAT_MODEL,
    BMB830OralEvaluationResult,
    BMB830OralEvaluator,
    OllamaConfig,
)
from ...learning.bmb830_oral_exam import (
    BMB830OralAttempt,
    BMB830OralPrompt,
    BMB830OralSnapshot,
    OralCriterion,
    bmb830_oral_prompt_bank,
)
from ...learning.mentor import (
    MentorJournalSnapshot,
    MentorMode,
    MentorTurnRecord,
)
from ...learning.mentor_context import build_module_mentor_context
from ...storage import (
    BMB830OralExamStore,
    MentorJournalStore,
    SQLiteProgressStore,
)

OralTask = Callable[[], BMB830OralEvaluationResult]
OralSuccessCallback = Callable[[int, BMB830OralEvaluationResult], None]
OralFailureCallback = Callable[[int, Exception], None]


class OralEvaluationRunner(Protocol):
    """Evaluate one learner transcript through an injected local service."""

    def evaluate(
        self,
        *,
        prompt: BMB830OralPrompt,
        transcript: str,
        authoritative_context: str,
        locale: AppLocale,
        previous_follow_up: str = "",
    ) -> BMB830OralEvaluationResult:
        """Return structured formative feedback."""


class OralEvaluationExecutor(Protocol):
    """Run blocking local-model work outside the GUI thread."""

    def submit(
        self,
        request_id: int,
        task: OralTask,
        on_success: OralSuccessCallback,
        on_failure: OralFailureCallback,
    ) -> None:
        """Schedule one evaluation."""

    def cancel(self, request_id: int) -> None:
        """Detach one evaluation from the page."""


class _OralTaskSignals(QObject):
    succeeded = Signal(int, object)
    failed = Signal(int, object)


class _OralTaskRunnable(QRunnable):
    def __init__(self, request_id: int, task: OralTask) -> None:
        super().__init__()
        self._request_id = request_id
        self._task = task
        self.signals = _OralTaskSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self) -> None:
        try:
            result = self._task()
        except Exception as exc:  # pragma: no cover - worker boundary
            self.signals.failed.emit(self._request_id, exc)
        else:
            self.signals.succeeded.emit(self._request_id, result)


class QtOralEvaluationExecutor:
    """Use Qt's shared thread pool for local oral-answer evaluation."""

    def __init__(self, thread_pool: QThreadPool | None = None) -> None:
        self._thread_pool = thread_pool or QThreadPool.globalInstance()

    def submit(
        self,
        request_id: int,
        task: OralTask,
        on_success: OralSuccessCallback,
        on_failure: OralFailureCallback,
    ) -> None:
        runnable = _OralTaskRunnable(request_id, task)
        runnable.signals.succeeded.connect(on_success)
        runnable.signals.failed.connect(on_failure)
        self._thread_pool.start(runnable)

    def cancel(self, request_id: int) -> None:
        del request_id


class BMB830OralExamPage(QWidget):
    """Practise grounded oral explanations and receive one Socratic follow-up."""

    BASE_URL_KEY = "ollama/base_url"
    MODEL_KEY = "ollama/model"
    NUM_CTX_KEY = "ollama/mentor_num_ctx"
    NUM_PREDICT_KEY = "ollama/oral_num_predict"
    DEFAULT_NUM_CTX = 16_384
    DEFAULT_NUM_PREDICT = 1_800
    DRAFT_PREFIX = "assessment/bmb830_oral/draft/"

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        settings: QSettings | None = None,
        oral_store: BMB830OralExamStore | None = None,
        mentor_store: MentorJournalStore | None = None,
        evaluator: OralEvaluationRunner | None = None,
        executor: OralEvaluationExecutor | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("bmb830OralExamPage")
        self._locale = locale
        self._settings = settings or QSettings()
        self._progress_store = progress_store
        self._prompts = bmb830_oral_prompt_bank(locale)
        self._prompt_by_id = {prompt.prompt_id: prompt for prompt in self._prompts}
        self._module_by_id = {
            bundle.materialize(locale).module.module_id: bundle.materialize(locale).module
            for bundle in LOCALIZED_BUNDLES
        }
        self._store = oral_store
        if self._store is None and progress_store is not None:
            self._store = BMB830OralExamStore.for_progress_store(progress_store)
        self._mentor_store = mentor_store
        if self._mentor_store is None and progress_store is not None:
            self._mentor_store = MentorJournalStore.for_progress_store(progress_store)
        loaded = self._store.load() if self._store is not None else None
        initial_prompt_id = self._prompts[0].prompt_id
        self._snapshot = loaded or BMB830OralSnapshot.empty(initial_prompt_id)
        if self._snapshot.active_prompt_id not in self._prompt_by_id:
            self._snapshot = self._snapshot.with_active_prompt(initial_prompt_id)
        self._evaluator = evaluator or self._build_evaluator()
        self._executor = executor or QtOralEvaluationExecutor()
        self._request_serial = 0
        self._active_request_id: int | None = None
        self._pending_transcript = ""
        self._pending_prompt: BMB830OralPrompt | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setObjectName("bmb830OralScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        body.setObjectName("bmb830OralBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(4, 4, 12, 24)
        layout.setSpacing(14)

        title = QLabel(self._text(BMB830OralCopyKey.TITLE))
        title.setObjectName("bmb830OralTitle")
        layout.addWidget(title)
        intro = QLabel(self._text(BMB830OralCopyKey.INTRO))
        intro.setWordWrap(True)
        layout.addWidget(intro)
        boundary = QLabel(self._text(BMB830OralCopyKey.BOUNDARY))
        boundary.setProperty("tone", "warning")
        boundary.setWordWrap(True)
        layout.addWidget(boundary)

        prompt_group = QGroupBox(self._text(BMB830OralCopyKey.PROMPT))
        prompt_layout = QVBoxLayout(prompt_group)
        self._selector = QComboBox()
        self._selector.setObjectName("bmb830OralPromptSelector")
        for prompt in self._prompts:
            prompt_number = prompt.prompt_id.rsplit("q", maxsplit=1)[-1]
            self._selector.addItem(
                f"{prompt.module_title} · Q{prompt_number}",
                prompt.prompt_id,
            )
        self._selector.currentIndexChanged.connect(self._prompt_changed)
        prompt_layout.addWidget(self._selector)
        self._question = QLabel()
        self._question.setObjectName("bmb830OralQuestion")
        self._question.setWordWrap(True)
        self._question.setTextInteractionFlags(
            self._question.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse
        )
        prompt_layout.addWidget(self._question)
        self._next_button = QPushButton(self._text(BMB830OralCopyKey.NEXT_RECOMMENDED))
        self._next_button.setObjectName("bmb830OralNextButton")
        self._next_button.clicked.connect(self._select_recommended_prompt)
        prompt_layout.addWidget(self._next_button)
        layout.addWidget(prompt_group)

        answer_group = QGroupBox(self._text(BMB830OralCopyKey.TRANSCRIPT))
        answer_layout = QVBoxLayout(answer_group)
        self._transcript = QPlainTextEdit()
        self._transcript.setObjectName("bmb830OralTranscript")
        self._transcript.setMinimumHeight(220)
        self._transcript.setPlaceholderText(self._text(BMB830OralCopyKey.TRANSCRIPT_PLACEHOLDER))
        self._transcript.textChanged.connect(self._save_visible_draft)
        answer_layout.addWidget(self._transcript)
        self._evaluate_button = QPushButton(self._text(BMB830OralCopyKey.EVALUATE))
        self._evaluate_button.setObjectName("bmb830OralEvaluateButton")
        self._evaluate_button.setProperty("buttonRole", "primary")
        self._evaluate_button.clicked.connect(self.evaluate_response)
        answer_layout.addWidget(self._evaluate_button)
        self._status = QLabel()
        self._status.setObjectName("bmb830OralStatus")
        self._status.setWordWrap(True)
        self._status.hide()
        answer_layout.addWidget(self._status)
        layout.addWidget(answer_group)

        self._feedback_group = QGroupBox(self._text(BMB830OralCopyKey.FEEDBACK))
        feedback_layout = QVBoxLayout(self._feedback_group)
        self._feedback = QLabel()
        self._feedback.setObjectName("bmb830OralFeedback")
        self._feedback.setWordWrap(True)
        self._feedback.setTextInteractionFlags(
            self._feedback.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse
        )
        feedback_layout.addWidget(self._feedback)

        scores_title = QLabel(self._text(BMB830OralCopyKey.SCORES))
        scores_title.setObjectName("bmb830OralScoresTitle")
        feedback_layout.addWidget(scores_title)
        self._scores_frame = QFrame()
        self._scores_frame.setObjectName("bmb830OralScores")
        self._scores_grid = QGridLayout(self._scores_frame)
        self._scores_grid.setContentsMargins(0, 0, 0, 0)
        self._score_labels: dict[OralCriterion, QLabel] = {}
        for row, criterion in enumerate(OralCriterion):
            criterion_label = QLabel(bmb830_oral_criterion_text(locale, criterion))
            criterion_label.setProperty("semanticTone", "subtle")
            score_label = QLabel("—")
            score_label.setObjectName(f"bmb830OralScore_{criterion.value}")
            score_label.setWordWrap(True)
            self._scores_grid.addWidget(criterion_label, row, 0)
            self._scores_grid.addWidget(score_label, row, 1)
            self._score_labels[criterion] = score_label
        feedback_layout.addWidget(self._scores_frame)

        self._strengths = self._feedback_label(BMB830OralCopyKey.STRENGTHS)
        self._gaps = self._feedback_label(BMB830OralCopyKey.GAPS)
        self._misconceptions = self._feedback_label(BMB830OralCopyKey.MISCONCEPTIONS)
        self._next_action = self._feedback_label(BMB830OralCopyKey.NEXT_ACTION)
        for widget in (
            self._strengths,
            self._gaps,
            self._misconceptions,
            self._next_action,
        ):
            feedback_layout.addWidget(widget)

        follow_up_title = QLabel(self._text(BMB830OralCopyKey.FOLLOW_UP))
        follow_up_title.setObjectName("bmb830OralFollowUpTitle")
        feedback_layout.addWidget(follow_up_title)
        self._follow_up = QLabel()
        self._follow_up.setObjectName("bmb830OralFollowUp")
        self._follow_up.setWordWrap(True)
        self._follow_up.setTextInteractionFlags(
            self._follow_up.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse
        )
        feedback_layout.addWidget(self._follow_up)
        self._confidence = QLabel()
        self._confidence.setProperty("semanticTone", "subtle")
        feedback_layout.addWidget(self._confidence)
        self._feedback_group.hide()
        layout.addWidget(self._feedback_group)

        history_group = QGroupBox(self._text(BMB830OralCopyKey.HISTORY))
        history_layout = QVBoxLayout(history_group)
        self._history = QLabel()
        self._history.setObjectName("bmb830OralHistory")
        self._history.setWordWrap(True)
        history_layout.addWidget(self._history)
        layout.addWidget(history_group)

        summary_group = QGroupBox(self._text(BMB830OralCopyKey.SUMMARY))
        summary_layout = QVBoxLayout(summary_group)
        self._attempt_count = QLabel()
        self._attempt_count.setObjectName("bmb830OralAttemptCount")
        summary_layout.addWidget(self._attempt_count)
        self._average = QLabel()
        self._average.setObjectName("bmb830OralAverage")
        summary_layout.addWidget(self._average)
        no_grade = QLabel(self._text(BMB830OralCopyKey.NO_OFFICIAL_GRADE))
        no_grade.setProperty("semanticTone", "muted")
        no_grade.setWordWrap(True)
        summary_layout.addWidget(no_grade)
        layout.addWidget(summary_group)
        layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self.select_prompt(self._snapshot.active_prompt_id)

    @property
    def snapshot(self) -> BMB830OralSnapshot:
        return self._snapshot

    @property
    def current_prompt(self) -> BMB830OralPrompt:
        prompt_id = str(self._selector.currentData() or self._snapshot.active_prompt_id)
        return self._prompt_by_id[prompt_id]

    @property
    def transcript_editor(self) -> QPlainTextEdit:
        return self._transcript

    def select_prompt(self, prompt_id: str) -> bool:
        index = self._selector.findData(prompt_id)
        if index < 0:
            return False
        self._selector.setCurrentIndex(index)
        self._load_prompt(prompt_id)
        return True

    @Slot()
    def persist(self) -> None:
        self._save_visible_draft()
        if self._store is not None:
            self._store.save(self._snapshot)

    @Slot()
    def evaluate_response(self) -> None:
        if self._active_request_id is not None:
            return
        transcript = self._transcript.toPlainText().strip()
        if not transcript:
            self._show_status(self._text(BMB830OralCopyKey.EMPTY), "warning")
            return
        prompt = self.current_prompt
        module = self._module_by_id[prompt.module_id]
        context = build_module_mentor_context(
            module,
            section_index=4,
            section_label=self._text(BMB830OralCopyKey.PROMPT),
            progress=self._progress_store,
        )
        latest = self._snapshot.latest_for(prompt.prompt_id)
        previous_follow_up = latest.evaluation.follow_up_question if latest is not None else ""
        self._request_serial += 1
        request_id = self._request_serial
        self._active_request_id = request_id
        self._pending_transcript = transcript
        self._pending_prompt = prompt
        self._set_busy(True)
        self._show_status(self._text(BMB830OralCopyKey.THINKING), "pending")
        self._executor.submit(
            request_id,
            lambda: self._evaluator.evaluate(
                prompt=prompt,
                transcript=transcript,
                authoritative_context=context,
                locale=self._locale,
                previous_follow_up=previous_follow_up,
            ),
            self._accept_evaluation,
            self._accept_failure,
        )

    def cancel_request(self) -> None:
        if self._active_request_id is None:
            return
        request_id = self._active_request_id
        self._executor.cancel(request_id)
        self._active_request_id = None
        self._pending_prompt = None
        self._pending_transcript = ""
        self._request_serial += 1
        self._set_busy(False)
        self._status.hide()

    @Slot(int)
    def _prompt_changed(self, _index: int) -> None:
        prompt_id = str(self._selector.currentData() or "")
        if prompt_id:
            self._load_prompt(prompt_id)

    @Slot()
    def _select_recommended_prompt(self) -> None:
        prompt = self._snapshot.recommended_prompt(self._prompts)
        self.select_prompt(prompt.prompt_id)

    def _load_prompt(self, prompt_id: str) -> None:
        prompt = self._prompt_by_id[prompt_id]
        self._snapshot = self._snapshot.with_active_prompt(prompt_id)
        self._question.setText(prompt.question)
        self._transcript.blockSignals(True)
        self._transcript.setPlainText(str(self._settings.value(self._draft_key(prompt_id), "")))
        self._transcript.blockSignals(False)
        latest = self._snapshot.latest_for(prompt_id)
        if latest is None:
            self._feedback_group.hide()
        else:
            self._render_evaluation(latest)
        self._update_history()
        self._update_summary()
        self.persist()

    def _accept_evaluation(
        self,
        request_id: int,
        result: BMB830OralEvaluationResult,
    ) -> None:
        prompt = self._pending_prompt
        if request_id != self._active_request_id or prompt is None:
            return
        response = result.response
        attempt = BMB830OralAttempt(
            attempt_id=f"bmb830-oral-{uuid4().hex}",
            prompt_id=prompt.prompt_id,
            module_id=prompt.module_id,
            transcript=self._pending_transcript,
            evaluation=result.evaluation,
            created_at=datetime.now(UTC),
            model=response.model,
            prompt_eval_count=response.prompt_eval_count,
            eval_count=response.eval_count,
            total_duration_ns=response.total_duration_ns,
        )
        self._snapshot = self._snapshot.append(attempt)
        self._append_mentor_turn(prompt, attempt)
        self.persist()
        self._active_request_id = None
        self._pending_prompt = None
        self._pending_transcript = ""
        self._set_busy(False)
        self._show_status(self._text(BMB830OralCopyKey.SAVED), "success")
        self._render_evaluation(attempt)
        self._update_history()
        self._update_summary()

    def _accept_failure(self, request_id: int, error: Exception) -> None:
        if request_id != self._active_request_id:
            return
        self._active_request_id = None
        self._pending_prompt = None
        self._pending_transcript = ""
        self._set_busy(False)
        detail = str(error).strip() or error.__class__.__name__
        self._show_status(
            self._text(BMB830OralCopyKey.ERROR, detail=detail),
            "error",
        )

    def _append_mentor_turn(
        self,
        prompt: BMB830OralPrompt,
        attempt: BMB830OralAttempt,
    ) -> None:
        if self._mentor_store is None:
            return
        journal = self._mentor_store.load() or MentorJournalSnapshot.empty()
        evaluation = attempt.evaluation
        assistant = f"{evaluation.feedback}\n\n{evaluation.follow_up_question}"
        turn = MentorTurnRecord(
            session_id="bmb830-oral-exam",
            created_at=attempt.created_at,
            context=f"BMB830 | {prompt.module_id} | oral exam practice",
            mode=MentorMode.EVALUATE,
            user_message=f"{prompt.question}\n\n{attempt.transcript}",
            assistant_message=assistant,
            observation=evaluation.to_mentor_observation(),
            model=attempt.model,
            prompt_eval_count=attempt.prompt_eval_count,
            eval_count=attempt.eval_count,
            total_duration_ns=attempt.total_duration_ns,
        )
        self._mentor_store.save(journal.append(turn))

    def _render_evaluation(self, attempt: BMB830OralAttempt) -> None:
        evaluation = attempt.evaluation
        self._feedback.setText(evaluation.feedback)
        for criterion in OralCriterion:
            result = evaluation.score_for(criterion)
            self._score_labels[criterion].setText(f"{result.score}/4 — {result.evidence}")
        self._strengths.setText(
            self._observation_text(BMB830OralCopyKey.STRENGTHS, evaluation.strengths)
        )
        self._gaps.setText(self._observation_text(BMB830OralCopyKey.GAPS, evaluation.gaps))
        self._misconceptions.setText(
            self._observation_text(
                BMB830OralCopyKey.MISCONCEPTIONS,
                evaluation.misconceptions,
            )
        )
        self._next_action.setText(
            f"{self._text(BMB830OralCopyKey.NEXT_ACTION)}: {evaluation.recommended_next_action}"
        )
        self._follow_up.setText(evaluation.follow_up_question)
        self._confidence.setText(
            self._text(
                BMB830OralCopyKey.CONFIDENCE,
                percent=round(evaluation.confidence * 100),
            )
        )
        self._feedback_group.show()

    def _update_history(self) -> None:
        attempts = self._snapshot.attempts_for(self.current_prompt.prompt_id)
        if not attempts:
            self._history.setText(self._text(BMB830OralCopyKey.NO_HISTORY))
            return
        lines = []
        for index, attempt in enumerate(reversed(attempts[-5:]), start=1):
            timestamp = attempt.created_at.astimezone().strftime("%Y-%m-%d %H:%M")
            lines.append(
                f"{index}. {timestamp} — {attempt.evaluation.average_score:.2f}/4 — "
                f"{attempt.evaluation.recommended_next_action}"
            )
        self._history.setText("\n".join(lines))

    def _update_summary(self) -> None:
        self._attempt_count.setText(
            self._text(BMB830OralCopyKey.ATTEMPTS, count=len(self._snapshot.attempts))
        )
        average = self._snapshot.average_score
        score = "—" if average is None else f"{average:.2f}"
        self._average.setText(self._text(BMB830OralCopyKey.AVERAGE, score=score))

    def _feedback_label(self, key: BMB830OralCopyKey) -> QLabel:
        label = QLabel()
        label.setObjectName(key.value.replace(".", "_"))
        label.setWordWrap(True)
        label.setProperty("semanticTone", "muted")
        return label

    def _observation_text(
        self,
        key: BMB830OralCopyKey,
        values: tuple[str, ...],
    ) -> str:
        content = "; ".join(values) if values else "—"
        return f"{self._text(key)}: {content}"

    @Slot()
    def _save_visible_draft(self) -> None:
        if not hasattr(self, "_selector"):
            return
        prompt_id = str(self._selector.currentData() or "")
        if prompt_id:
            self._settings.setValue(
                self._draft_key(prompt_id),
                self._transcript.toPlainText(),
            )

    def _draft_key(self, prompt_id: str) -> str:
        return f"{self.DRAFT_PREFIX}{prompt_id}"

    def _build_evaluator(self) -> BMB830OralEvaluator:
        base_url = str(
            self._settings.value(
                self.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        ).strip()
        model = str(self._settings.value(self.MODEL_KEY, DEFAULT_CHAT_MODEL)).strip()
        return BMB830OralEvaluator(
            config=OllamaConfig(base_url=base_url),
            model=model or DEFAULT_CHAT_MODEL,
            num_ctx=self._positive_setting(self.NUM_CTX_KEY, self.DEFAULT_NUM_CTX),
            num_predict=self._positive_setting(
                self.NUM_PREDICT_KEY,
                self.DEFAULT_NUM_PREDICT,
            ),
        )

    def _positive_setting(self, key: str, default: int) -> int:
        raw = self._settings.value(key, default)
        if isinstance(raw, bool):
            return default
        try:
            value = int(str(raw))
        except ValueError:
            return default
        return value if value > 0 else default

    def _set_busy(self, busy: bool) -> None:
        self._evaluate_button.setEnabled(not busy)
        self._next_button.setEnabled(not busy)
        self._selector.setEnabled(not busy)
        self._transcript.setReadOnly(busy)

    def _show_status(self, text: str, state: str) -> None:
        self._status.setText(text)
        self._status.setProperty("chatState", state)
        self._status.show()
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)

    def _text(self, key: BMB830OralCopyKey, **values: object) -> str:
        return bmb830_oral_text(self._locale, key, **values)


__all__ = [
    "BMB830OralExamPage",
    "OralEvaluationExecutor",
    "OralEvaluationRunner",
    "QtOralEvaluationExecutor",
]
