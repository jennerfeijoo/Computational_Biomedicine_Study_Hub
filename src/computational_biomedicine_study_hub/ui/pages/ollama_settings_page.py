"""PySide6 settings page for validating a local Ollama installation."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject, QSettings, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...integrations import (
    OllamaClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaModel,
    OllamaProtocolError,
)

ClientFactory = Callable[[OllamaConfig], OllamaClient]


class OllamaProbeWorker(QObject):
    """Run the local connection probe outside the GUI thread."""

    succeeded = Signal(str, object)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, client: OllamaClient) -> None:
        super().__init__()
        self._client = client

    @Slot()
    def run(self) -> None:
        """Read the server version and installed models."""
        try:
            version = self._client.get_version()
            models = self._client.list_models()
        except (OllamaConnectionError, OllamaProtocolError) as exc:
            self.failed.emit(str(exc))
        else:
            self.succeeded.emit(version, models)
        finally:
            self.finished.emit()


class OllamaSettingsPage(QWidget):
    """Configure, validate and persist the local Ollama connection."""

    BASE_URL_KEY = "ollama/base_url"
    MODEL_KEY = "ollama/model"

    def __init__(
        self,
        settings: QSettings | None = None,
        client_factory: ClientFactory | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("ollamaSettingsPage")

        self._settings = settings or QSettings()
        self._client_factory = client_factory or OllamaClient
        self._probe_thread: QThread | None = None
        self._probe_worker: OllamaProbeWorker | None = None

        self._base_url = QLineEdit(self._stored_base_url())
        self._base_url.setObjectName("ollamaBaseUrl")
        self._base_url.setPlaceholderText("http://localhost:11434/api")

        self._probe_button = QPushButton("Probar conexión")
        self._probe_button.setObjectName("primaryActionButton")
        self._probe_button.clicked.connect(self.start_probe)

        self._status = QLabel("Conexión no comprobada.")
        self._status.setObjectName("ollamaStatus")
        self._status.setWordWrap(True)
        self._set_status_state("idle")

        self._version = QLabel("—")
        self._version.setObjectName("ollamaVersion")

        self._models = QComboBox()
        self._models.setObjectName("ollamaModelSelector")
        self._models.setEnabled(False)

        self._save_button = QPushButton("Guardar configuración")
        self._save_button.setObjectName("secondaryActionButton")
        self._save_button.setEnabled(False)
        self._save_button.clicked.connect(self.save_preferences)

        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.addRow("URL local:", self._base_url)
        form.addRow("Estado:", self._status)
        form.addRow("Versión detectada:", self._version)
        form.addRow("Modelo:", self._models)

        actions = QHBoxLayout()
        actions.addWidget(self._probe_button)
        actions.addWidget(self._save_button)
        actions.addStretch(1)

        group = QGroupBox("Ollama local")
        group.setObjectName("settingsGroup")
        group_layout = QVBoxLayout(group)
        group_layout.addLayout(form)
        group_layout.addLayout(actions)

        explanation = QLabel(
            "Esta pantalla solo verifica la instalación local y permite seleccionar "
            "el modelo que usarán futuras funciones de tutoría y evaluación."
        )
        explanation.setObjectName("settingsExplanation")
        explanation.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(explanation)
        layout.addWidget(group)
        layout.addStretch(1)

    @property
    def base_url(self) -> str:
        """Return the current URL field value."""
        return self._base_url.text().strip()

    @property
    def selected_model(self) -> str:
        """Return the currently selected local model name."""
        return self._models.currentText().strip()

    @property
    def status_text(self) -> str:
        """Return the visible connection status."""
        return self._status.text()

    @Slot()
    def start_probe(self) -> None:
        """Validate Ollama and discover models without freezing the interface."""
        if self._probe_thread is not None and self._probe_thread.isRunning():
            return

        config = OllamaConfig(base_url=self.base_url)
        client = self._client_factory(config)

        thread = QThread(self)
        worker = OllamaProbeWorker(client)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.succeeded.connect(self.apply_probe_success)
        worker.failed.connect(self.apply_probe_failure)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._probe_finished)

        self._probe_thread = thread
        self._probe_worker = worker
        self._probe_button.setEnabled(False)
        self._save_button.setEnabled(False)
        self._models.setEnabled(False)
        self._models.clear()
        self._version.setText("—")
        self._status.setText("Conectando con Ollama…")
        self._set_status_state("pending")
        thread.start()

    @Slot(str, object)
    def apply_probe_success(self, version: str, models_payload: object) -> None:
        """Display a successful connection result."""
        models = tuple(
            model
            for model in models_payload
            if isinstance(model, OllamaModel)
        ) if isinstance(models_payload, tuple) else ()

        self._version.setText(version)
        self._models.clear()
        self._models.addItems([model.name for model in models])

        stored_model = str(self._settings.value(self.MODEL_KEY, "")).strip()
        if stored_model:
            stored_index = self._models.findText(stored_model)
            if stored_index >= 0:
                self._models.setCurrentIndex(stored_index)

        if models:
            self._status.setText(
                f"Conexión correcta. Se detectaron {len(models)} modelos locales."
            )
            self._models.setEnabled(True)
            self._save_button.setEnabled(True)
        else:
            self._status.setText(
                "Conexión correcta, pero Ollama no informó modelos instalados."
            )
            self._save_button.setEnabled(False)

        self._set_status_state("success")

    @Slot(str)
    def apply_probe_failure(self, message: str) -> None:
        """Display a connection or protocol failure."""
        self._version.setText("—")
        self._models.clear()
        self._models.setEnabled(False)
        self._save_button.setEnabled(False)
        self._status.setText(message)
        self._set_status_state("error")

    @Slot()
    def save_preferences(self) -> None:
        """Persist the normalized URL and selected model."""
        normalized_url = OllamaConfig(base_url=self.base_url).normalized_base_url()
        self._base_url.setText(normalized_url)
        self._settings.setValue(self.BASE_URL_KEY, normalized_url)
        self._settings.setValue(self.MODEL_KEY, self.selected_model)
        self._settings.sync()
        self._status.setText(
            f"Configuración guardada para el modelo {self.selected_model}."
        )
        self._set_status_state("success")

    @Slot()
    def _probe_finished(self) -> None:
        self._probe_button.setEnabled(True)
        self._probe_thread = None
        self._probe_worker = None

    def _stored_base_url(self) -> str:
        value = str(
            self._settings.value(
                self.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        )
        return OllamaConfig(base_url=value).normalized_base_url()

    def _set_status_state(self, state: str) -> None:
        self._status.setProperty("connectionState", state)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
