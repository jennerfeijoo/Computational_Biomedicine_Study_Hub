from __future__ import annotations

import re
from pathlib import Path

import pytest
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QFrame, QLabel, QPlainTextEdit

from computational_biomedicine_study_hub.academic import SemesterContentLoader
from computational_biomedicine_study_hub.academic.catalog import AcademicCatalog as SourceCatalog
from computational_biomedicine_study_hub.academic.models import (
    ExampleKind,
    ExampleLanguage,
    ExampleOutputKind,
)
from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.content.models import WorkedExample
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.academic_catalog import AcademicCatalog
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage
from computational_biomedicine_study_hub.ui.r_syntax_highlighter import RSyntaxHighlighter


@pytest.fixture(scope="module")
def source_catalog() -> SourceCatalog:
    return SemesterContentLoader().load()


def test_every_worked_example_has_a_consistent_structural_classification(
    source_catalog: SourceCatalog,
) -> None:
    examples = tuple(
        example
        for course in source_catalog.courses
        for module in course.modules
        for example in module.worked_examples
    )

    assert examples
    for example in examples:
        has_code = bool(example.code.resolve("en").strip())
        has_output = bool(example.expected_output.resolve("en").strip())

        assert isinstance(example.example_kind, ExampleKind)
        assert example.language is None or isinstance(example.language, ExampleLanguage)
        assert isinstance(example.output_kind, ExampleOutputKind)
        assert has_code is (example.language is not None)
        assert has_output is (example.output_kind is not ExampleOutputKind.NONE)


def test_bmb830_has_authored_r_coverage_at_the_required_module_grain(
    source_catalog: SourceCatalog,
) -> None:
    course = source_catalog.course("bmb830")
    r_examples_by_module = {
        module.id: tuple(
            example
            for example in module.worked_examples
            if example.example_kind is ExampleKind.R_CODE
        )
        for module in course.modules
    }

    assert len(r_examples_by_module["bmb830.m01"]) >= 1
    assert all(len(r_examples_by_module[f"bmb830.m{number:02}"]) >= 2 for number in range(2, 11))


def test_bmb831_has_r_examples_in_every_module_and_omics_specific_workflows(
    source_catalog: SourceCatalog,
) -> None:
    course = source_catalog.course("bmb831")
    r_examples_by_module = {
        module.id: tuple(
            example
            for example in module.worked_examples
            if example.example_kind is ExampleKind.R_CODE
        )
        for module in course.modules
    }

    assert all(r_examples_by_module.values())
    omics_vocabulary = re.compile(
        (
            r"SummarizedExperiment|DESeqDataSet|assay\(|p\.adjust|hypergeom|"
            r"proteins?|pathway|multi.?omics"
        ),
        re.IGNORECASE,
    )
    for number in range(7, 12):
        module_examples = r_examples_by_module[f"bmb831.m{number:02}"]
        authored_text = "\n".join(
            f"{example.code.resolve('en')}\n{example.explanation.resolve('en')}"
            for example in module_examples
        )
        assert omics_vocabulary.search(authored_text), f"BMB831 M{number:02}"


def test_authored_r_examples_are_complete_and_locale_safe(
    source_catalog: SourceCatalog,
) -> None:
    r_examples = tuple(
        example
        for course_code in ("bmb830", "bmb831")
        for module in source_catalog.course(course_code).modules
        for example in module.worked_examples
        if example.example_kind is ExampleKind.R_CODE
    )

    assert len(r_examples) >= 42
    for example in r_examples:
        code = example.code.resolve("en")
        assert example.language is ExampleLanguage.R
        assert code.strip()
        assert example.output_kind is not ExampleOutputKind.NONE
        assert example.expected_output.resolve("en").strip()
        assert all(example.explanation.resolve(locale).strip() for locale in ("es", "en", "da"))

        uses_randomness = bool(
            re.search(r"\b(sample|sample\.int|rnorm|runif|rbinom|boot)\s*\(", code)
        )
        if uses_randomness:
            assert "set.seed(" in code


def test_r_renderer_omits_empty_sections_and_distinguishes_plot_descriptions(
    qapp,
) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    conceptual = WorkedExample(
        example_id="test.empty",
        title="Conceptual example",
        problem="",
        reasoning=(),
        code="",
        expected_output="",
        explanation="Only this explanation is authored.",
    )
    conceptual_card = reader._example_card(conceptual)

    assert conceptual_card.findChild(QPlainTextEdit, "exampleCode") is None
    assert conceptual_card.findChild(QPlainTextEdit, "exampleOutput") is None
    assert conceptual_card.findChild(QLabel, "examplePlotDescription") is None
    assert conceptual_card.findChild(QLabel, "exampleLanguageBadge") is None

    plot_example = WorkedExample(
        example_id="test.plot",
        title="Plot example",
        problem="Inspect the relationship.",
        reasoning=(),
        code="plot(1:3)",
        expected_output="Three points increase from lower left to upper right.",
        explanation="The trend is positive.",
        example_kind="r_code",
        language="r",
        output_kind="plot_description",
    )
    plot_card = reader._example_card(plot_example)

    assert plot_card.findChild(QPlainTextEdit, "exampleCode") is not None
    assert plot_card.findChild(QPlainTextEdit, "exampleOutput") is None
    assert plot_card.findChild(QLabel, "examplePlotDescription") is not None
    assert plot_card.findChild(QLabel, "exampleLanguageBadge").text() == "R"


def test_bmb830_conceptual_examples_do_not_create_empty_dark_blocks(qapp) -> None:
    module = (
        AcademicCatalog(locale=AppLocale.ENGLISH)
        .module(
            "BMB830",
            "bmb830.m01",
        )
        .module
    )
    reader = ModuleReaderPage(module)
    assert reader.select_section_index(2)
    cards = reader.findChildren(QFrame, "exampleCard")

    assert len(cards) == len(module.worked_examples)
    for example, card in zip(module.worked_examples, cards, strict=True):
        if not example.code.strip():
            assert card.findChild(QPlainTextEdit, "exampleCode") is None
        if not example.expected_output.strip():
            assert card.findChild(QPlainTextEdit, "exampleOutput") is None


def test_dm857_python_examples_keep_their_code_and_output(qapp) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    assert reader.select_section_index(2)
    code_blocks = reader.findChildren(QPlainTextEdit, "exampleCode")
    output_blocks = reader.findChildren(QPlainTextEdit, "exampleOutput")

    assert len(code_blocks) == sum(
        bool(example.code.strip()) for example in MODULE_01_FOUNDATIONS.worked_examples
    )
    assert len(output_blocks) == sum(
        bool(example.expected_output.strip()) for example in MODULE_01_FOUNDATIONS.worked_examples
    )
    assert all(block.property("language") == "python" for block in code_blocks)


def test_r_code_blocks_are_read_only_selectable_and_highlighted(qapp) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    example = WorkedExample(
        example_id="test.highlight",
        title="R highlighting",
        problem="Trace the expression.",
        reasoning=(),
        code='if (TRUE) result <- mean(c(1, 2)) + "ok" # note',
        expected_output='[1] "ok"',
        explanation="The example is display-only.",
        example_kind="r_code",
        language="r",
        output_kind="console",
    )
    card = reader._example_card(example)
    editor = card.findChild(QPlainTextEdit, "exampleCode")

    assert editor is not None
    assert editor.isReadOnly()
    assert editor.property("language") == "r"
    assert editor.lineWrapMode() is QPlainTextEdit.LineWrapMode.NoWrap
    assert editor.toPlainText() == example.code

    document = QTextDocument(example.code)
    highlighter = RSyntaxHighlighter(document)
    highlighter.rehighlight()
    formats = document.firstBlock().layout().formats()
    colors = {
        item.format.foreground().color().name()
        for item in formats
        if item.format.foreground().color().isValid()
    }
    highlighted_positions = {
        position for item in formats for position in range(item.start, item.start + item.length)
    }
    for token in ("if", "TRUE", "<-", "mean", "1", '"ok"', "# note"):
        start = example.code.index(token)
        assert set(range(start, start + len(token))) <= highlighted_positions
    assert len(colors) >= 5


def test_r_examples_do_not_add_an_in_process_or_arbitrary_runner() -> None:
    root = Path(__file__).resolve().parents[1]
    dependency_text = (root / "pyproject.toml").read_text(encoding="utf-8").casefold()
    r_display_sources = "\n".join(
        path.read_text(encoding="utf-8").casefold()
        for path in (
            root
            / "src"
            / "computational_biomedicine_study_hub"
            / "ui"
            / "pages"
            / "module_reader_page.py",
            root / "src" / "computational_biomedicine_study_hub" / "ui" / "r_syntax_highlighter.py",
        )
    )

    assert "rpy2" not in dependency_text
    assert "rpy2" not in r_display_sources
    assert "subprocess" not in r_display_sources
    assert "rscript" not in r_display_sources
