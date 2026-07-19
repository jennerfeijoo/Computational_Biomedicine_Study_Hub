"""Learner-facing semantic document renderer for cumulative assessments."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from html import escape
from typing import Any

from ..academic.localization import localize_value
from ..academic.models import CourseContent, CumulativeAssessment

_SECTION_ALIASES = {
    "requirements": ("analysis_portfolio", "report_requirements", "project_requirements"),
    "tracks": ("portfolio_tracks", "project_tracks"),
    "structure": ("report_blueprint", "report_structure"),
    "rubrics": ("portfolio_rubric", "project_rubric", "report_rubric", "oral_rubric"),
    "cases": ("publication_appraisal_cases", "scientific_review_cases"),
    "questions": ("oral_question_bank",),
    "checklists": ("quality_checks", "reproducibility_checklist", "completion_criteria"),
}


class CumulativeAssessmentRenderer:
    """Render known cumulative-assessment concepts without exposing its YAML schema."""

    def __init__(
        self,
        assessment: CumulativeAssessment,
        course: CourseContent,
        *,
        course_title: str,
        locale: str,
    ) -> None:
        self._assessment = assessment
        self._course = course
        self._course_title = course_title
        self._locale = locale
        self._copy = _COPY[locale]
        visible = _learner_visible(assessment.raw)
        self._raw = _mapping(visible)

    def render_html(self) -> str:
        """Return one complete, ordered learner document."""
        title = self._assessment.title.resolve(self._locale)
        metadata = _mapping(self._raw.get("metadata"))
        note = self._text(metadata.get("note"))
        purpose = self._purpose(metadata)

        parts = [
            "<article>",
            f"<h1>{escape(title)}</h1>",
            f"<p><b>{escape(self._copy['course'])}:</b> {escape(self._course_title)}</p>",
            f"<p><i>{escape(note or self._copy['preparation_notice'])}</i></p>",
            (
                f"<p>{escape(self._copy['coverage'].format(count=len(self._course.modules), course=self._course_title))}</p>"
            ),
            self._section(self._copy["purpose"], self._paragraph(purpose)),
            self._section(self._copy["competencies"], self._competencies()),
            self._section(self._copy["components"], self._components()),
            self._section(self._copy["tracks"], self._tracks()),
            self._section(self._copy["structure"], self._structure()),
            self._section(self._copy["rubric"], self._rubrics()),
            self._section(self._copy["review_cases"], self._review_cases()),
            self._section(self._copy["defense_questions"], self._defense_questions()),
            self._section(self._copy["checklist"], self._checklists()),
            "</article>",
        ]
        return "".join(part for part in parts if part)

    def _purpose(self, metadata: Mapping[str, Any]) -> str:
        for key in ("scope", "description", "purpose"):
            text = self._text(metadata.get(key))
            if text:
                return text
        requirements = self._first_mapping(_SECTION_ALIASES["requirements"])
        return self._text(requirements.get("purpose")) or self._course.summary.resolve(self._locale)

    def _competencies(self) -> str:
        values = tuple(
            objective.statement.resolve(self._locale)
            for objective in self._course.learning_outcomes
            if objective.statement.resolve(self._locale).strip()
        )
        return self._list(values) or self._paragraph(self._copy["not_specified"])

    def _components(self) -> str:
        requirements = self._first_mapping(_SECTION_ALIASES["requirements"])
        components = _sequence(
            requirements.get("mandatory_components", requirements.get("mandatory_elements"))
        )
        rendered = [
            self._described_item(_mapping(item), index=index)
            for index, item in enumerate(components, start=1)
        ]
        prohibited = self._strings(requirements.get("prohibited_shortcuts"))
        if prohibited:
            rendered.extend(
                (
                    f"<h3>{escape(self._copy['avoid'])}</h3>",
                    self._list(prohibited),
                )
            )
        return "".join(rendered) or self._paragraph(self._copy["not_specified"])

    def _tracks(self) -> str:
        tracks = self._first_sequence(_SECTION_ALIASES["tracks"])
        rendered: list[str] = []
        detail_keys = (
            ("required_features", "required"),
            ("required_elements", "required"),
            ("required_methods", "methods"),
            ("required_controls", "controls"),
            ("required_sensitivity", "sensitivity"),
        )
        for index, value in enumerate(tracks, start=1):
            item = _mapping(value)
            title = self._text(item.get("title")) or self._generated_title(item, index)
            description = self._text(item.get("core_question"))
            rendered.extend((f"<h3>{escape(title)}</h3>", self._paragraph(description)))
            for key, label_key in detail_keys:
                values = self._strings(item.get(key))
                if values:
                    rendered.extend(
                        (
                            f"<p><b>{escape(self._copy[label_key])}</b></p>",
                            self._list(values),
                        )
                    )
        return "".join(rendered) or self._paragraph(self._copy["not_specified"])

    def _structure(self) -> str:
        structure = self._first_mapping(_SECTION_ALIASES["structure"])
        sections = _sequence(structure.get("recommended_sections"))
        rendered = [
            self._described_item(
                _mapping(item),
                index=index,
                title_keys=("title", "section", "name"),
                description_keys=("description", "purpose"),
            )
            for index, item in enumerate(sections, start=1)
        ]
        for key, label_key in (
            ("required_tables", "tables"),
            ("required_figures", "figures"),
        ):
            values = self._strings(structure.get(key))
            if values:
                rendered.extend((f"<h3>{escape(self._copy[label_key])}</h3>", self._list(values)))

        oral = self._first_mapping(("oral_practice_blueprint", "oral_practice"))
        phases = _sequence(oral.get("recommended_phases", oral.get("phases")))
        if phases:
            rendered.append(f"<h3>{escape(self._copy['oral_structure'])}</h3>")
            rendered.extend(
                self._described_item(
                    _mapping(item),
                    index=index,
                    title_keys=("title", "phase", "name"),
                    description_keys=("description", "purpose"),
                )
                for index, item in enumerate(phases, start=1)
            )
        return "".join(rendered) or self._paragraph(self._copy["not_specified"])

    def _rubrics(self) -> str:
        rows: list[str] = []
        for key in _SECTION_ALIASES["rubrics"]:
            rubric = _mapping(self._raw.get(key))
            for index, value in enumerate(_sequence(rubric.get("criteria")), start=1):
                criterion = _mapping(value)
                title = self._text(
                    criterion.get("title", criterion.get("name", criterion.get("criterion")))
                ) or self._identifier_label(str(criterion.get("id", "")), index)
                excellent = self._text(criterion.get("excellent"))
                if not excellent:
                    excellent = self._text(_mapping(criterion.get("descriptors")).get("excellent"))
                points = self._rubric_points(criterion)
                rows.append(
                    "<tr>"
                    f"<td><b>{escape(title)}</b></td>"
                    f"<td>{escape(points)}</td>"
                    f"<td>{escape(excellent)}</td>"
                    "</tr>"
                )
        if not rows:
            return self._paragraph(self._copy["not_specified"])
        return (
            '<table border="1" cellspacing="0" cellpadding="7" width="100%">'
            "<thead><tr>"
            f"<th>{escape(self._copy['criterion'])}</th>"
            f"<th>{escape(self._copy['points'])}</th>"
            f"<th>{escape(self._copy['excellent'])}</th>"
            "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
        )

    def _review_cases(self) -> str:
        cases = self._first_sequence(_SECTION_ALIASES["cases"])
        rendered = [
            self._described_item(
                _mapping(item),
                index=index,
                title_keys=("title", "name"),
                description_keys=("stem", "scenario", "prompt", "description"),
                numbered_title=self._copy["case_number"],
            )
            for index, item in enumerate(cases, start=1)
        ]
        return "".join(rendered) or self._paragraph(self._copy["not_specified"])

    def _defense_questions(self) -> str:
        questions = self._first_sequence(_SECTION_ALIASES["questions"])
        nested_bank = _mapping(self._raw.get("review_and_defense_bank"))
        questions = (*questions, *_sequence(nested_bank.get("questions")))
        prompts = tuple(
            text
            for item in questions
            for text in (
                self._text(
                    _mapping(item).get(
                        "prompt",
                        _mapping(item).get("question", _mapping(item).get("text")),
                    )
                ),
            )
            if text
        )
        return self._ordered_list(prompts) or self._paragraph(self._copy["not_specified"])

    def _checklists(self) -> str:
        rendered: list[str] = []
        for key in _SECTION_ALIASES["checklists"]:
            value = self._raw.get(key)
            if isinstance(value, Mapping):
                for group, entries in value.items():
                    strings = self._strings(entries)
                    if not strings:
                        continue
                    label = _CHECKLIST_LABELS[self._locale].get(
                        str(group),
                        self._copy["check_group"],
                    )
                    rendered.extend((f"<h3>{escape(label)}</h3>", self._list(strings)))
            else:
                strings = self._strings(value)
                if strings:
                    rendered.append(self._list(strings))
        return "".join(rendered) or self._paragraph(self._copy["not_specified"])

    def _described_item(
        self,
        item: Mapping[str, Any],
        *,
        index: int,
        title_keys: tuple[str, ...] = ("title", "name"),
        description_keys: tuple[str, ...] = ("description", "purpose"),
        numbered_title: str = "",
    ) -> str:
        title = next((self._text(item.get(key)) for key in title_keys if item.get(key)), "")
        description = next(
            (self._text(item.get(key)) for key in description_keys if item.get(key)),
            "",
        )
        if not title:
            if numbered_title:
                title = numbered_title.format(number=index)
            else:
                title = self._title_from_description(description) or self._generated_title(
                    item, index
                )
        return f"<h3>{escape(title)}</h3>{self._paragraph(description)}"

    def _generated_title(self, item: Mapping[str, Any], index: int) -> str:
        identifier = str(item.get("id", "")).strip()
        return self._identifier_label(identifier, index)

    def _identifier_label(self, identifier: str, index: int) -> str:
        leaf = identifier.rsplit(".", 1)[-1]
        tokens = [token for token in leaf.replace("-", "_").split("_") if token]
        translated = [
            _IDENTIFIER_WORDS[self._locale].get(token.casefold(), token)
            for token in tokens
            if not token.casefold().startswith(("q0", "m0", "lo0"))
        ]
        if translated:
            return " ".join(translated).capitalize()
        return self._copy["item_number"].format(number=index)

    def _rubric_points(self, criterion: Mapping[str, Any]) -> str:
        points = criterion.get("points")
        if isinstance(points, (int, float)) and not isinstance(points, bool):
            return f"{points:g}"
        weight = criterion.get("weight")
        if isinstance(weight, (int, float)) and not isinstance(weight, bool):
            return f"{weight * 100:g}%"
        return "—"

    def _first_mapping(self, keys: tuple[str, ...]) -> Mapping[str, Any]:
        return next(
            (mapping for key in keys for mapping in (_mapping(self._raw.get(key)),) if mapping),
            {},
        )

    def _first_sequence(self, keys: tuple[str, ...]) -> tuple[object, ...]:
        return next(
            (sequence for key in keys for sequence in (_sequence(self._raw.get(key)),) if sequence),
            (),
        )

    def _text(self, value: object) -> str:
        localized = localize_value(value, self._locale)
        return localized.strip() if isinstance(localized, str) else ""

    def _strings(self, value: object) -> tuple[str, ...]:
        localized = localize_value(value, self._locale)
        if isinstance(localized, str):
            return (localized.strip(),) if localized.strip() else ()
        if isinstance(localized, Sequence) and not isinstance(localized, (str, bytes)):
            return tuple(str(item).strip() for item in localized if str(item).strip())
        return ()

    @staticmethod
    def _title_from_description(description: str) -> str:
        if not description:
            return ""
        first_clause = description.split(".", 1)[0]
        segments = [segment.strip() for segment in first_clause.split(",") if segment.strip()]
        title = " · ".join(segments[:2])
        return title[:70].rstrip()

    @staticmethod
    def _paragraph(value: str) -> str:
        return f"<p>{escape(value)}</p>" if value else ""

    @staticmethod
    def _list(values: Sequence[str]) -> str:
        return "<ul>" + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ul>"

    @staticmethod
    def _ordered_list(values: Sequence[str]) -> str:
        return "<ol>" + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ol>"

    @staticmethod
    def _section(title: str, body: str) -> str:
        return f"<section><h2>{escape(title)}</h2>{body}</section>"


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: object) -> tuple[object, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(value)


_HIDDEN_KEYS = {
    "answer_key",
    "canonical_answer",
    "canonical_explanation",
    "correct_answer",
    "correct_answers",
    "expected_analysis",
    "expected_elements",
    "grading_guide",
    "hidden_examiner_support",
    "hidden_grading_guide",
    "hidden_support",
    "insufficient",
    "model_answer",
    "solution",
    "solutions",
}


def _learner_visible(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            str(key): _learner_visible(item)
            for key, item in value.items()
            if str(key).casefold() not in _HIDDEN_KEYS
            and not str(key).casefold().startswith("hidden_")
        }
    if isinstance(value, list):
        return [_learner_visible(item) for item in value]
    return value


_COPY = {
    "es": {
        "course": "Asignatura",
        "preparation_notice": (
            "Material de preparación académica; no sustituye las instrucciones oficiales."
        ),
        "coverage": "Cubre los {count} módulos de {course}.",
        "purpose": "Propósito",
        "competencies": "Competencias evaluadas",
        "components": "Componentes obligatorios",
        "tracks": "Líneas de proyecto",
        "structure": "Estructura recomendada",
        "rubric": "Rúbrica",
        "review_cases": "Casos de revisión",
        "defense_questions": "Preguntas de defensa",
        "checklist": "Checklist",
        "avoid": "Prácticas que deben evitarse",
        "required": "Elementos requeridos",
        "methods": "Métodos requeridos",
        "controls": "Controles requeridos",
        "sensitivity": "Análisis de sensibilidad",
        "tables": "Tablas requeridas",
        "figures": "Figuras requeridas",
        "oral_structure": "Estructura de práctica oral",
        "criterion": "Criterio",
        "points": "Puntos o peso",
        "excellent": "Desempeño excelente",
        "case_number": "Caso {number}",
        "item_number": "Elemento {number}",
        "check_group": "Comprobaciones",
        "not_specified": "No se especifica una sección adicional.",
    },
    "en": {
        "course": "Course",
        "preparation_notice": (
            "Academic preparation material; it does not replace official instructions."
        ),
        "coverage": "Covers all {count} modules in {course}.",
        "purpose": "Purpose",
        "competencies": "Assessed competencies",
        "components": "Mandatory components",
        "tracks": "Project tracks",
        "structure": "Recommended structure",
        "rubric": "Rubric",
        "review_cases": "Review cases",
        "defense_questions": "Defense questions",
        "checklist": "Checklist",
        "avoid": "Practices to avoid",
        "required": "Required elements",
        "methods": "Required methods",
        "controls": "Required controls",
        "sensitivity": "Sensitivity analysis",
        "tables": "Required tables",
        "figures": "Required figures",
        "oral_structure": "Oral-practice structure",
        "criterion": "Criterion",
        "points": "Points or weight",
        "excellent": "Excellent performance",
        "case_number": "Case {number}",
        "item_number": "Item {number}",
        "check_group": "Checks",
        "not_specified": "No additional section is specified.",
    },
    "da": {
        "course": "Kursus",
        "preparation_notice": (
            "Akademisk forberedelsesmateriale; det erstatter ikke officielle instruktioner."
        ),
        "coverage": "Dækker alle {count} moduler i {course}.",
        "purpose": "Formål",
        "competencies": "Vurderede kompetencer",
        "components": "Obligatoriske komponenter",
        "tracks": "Projektspor",
        "structure": "Anbefalet struktur",
        "rubric": "Rubrik",
        "review_cases": "Review-cases",
        "defense_questions": "Forsvarsspørgsmål",
        "checklist": "Tjekliste",
        "avoid": "Praksisser der skal undgås",
        "required": "Krævede elementer",
        "methods": "Krævede metoder",
        "controls": "Krævede kontroller",
        "sensitivity": "Følsomhedsanalyse",
        "tables": "Krævede tabeller",
        "figures": "Krævede figurer",
        "oral_structure": "Struktur for mundtlig træning",
        "criterion": "Kriterium",
        "points": "Point eller vægt",
        "excellent": "Fremragende præstation",
        "case_number": "Case {number}",
        "item_number": "Element {number}",
        "check_group": "Kontroller",
        "not_specified": "Der er ikke angivet en yderligere sektion.",
    },
}

_CHECKLIST_LABELS = {
    "es": {
        "inputs": "Entradas",
        "project_structure": "Estructura del proyecto",
        "environment": "Entorno",
        "execution": "Ejecución",
        "audit": "Auditoría",
        "content_complete_when": "Contenido completo",
        "analysis_complete_when": "Análisis completo",
        "review_ready_when": "Preparación para revisión",
    },
    "en": {
        "inputs": "Inputs",
        "project_structure": "Project structure",
        "environment": "Environment",
        "execution": "Execution",
        "audit": "Audit",
        "content_complete_when": "Content complete",
        "analysis_complete_when": "Analysis complete",
        "review_ready_when": "Ready for review",
    },
    "da": {
        "inputs": "Input",
        "project_structure": "Projektstruktur",
        "environment": "Miljø",
        "execution": "Kørsel",
        "audit": "Audit",
        "content_complete_when": "Indhold komplet",
        "analysis_complete_when": "Analyse komplet",
        "review_ready_when": "Klar til review",
    },
}

_IDENTIFIER_WORDS = {
    "es": {
        "question": "pregunta",
        "estimand": "estimando",
        "design": "diseño",
        "data": "datos",
        "quality": "calidad",
        "provenance": "procedencia",
        "contract": "contrato",
        "reproducible": "reproducible",
        "reproducibility": "reproducibilidad",
        "descriptive": "descriptivo",
        "visualization": "visualización",
        "statistical": "estadístico",
        "model": "modelo",
        "modeling": "modelado",
        "inference": "inferencia",
        "diagnostics": "diagnósticos",
        "sensitivity": "sensibilidad",
        "limitations": "limitaciones",
        "communication": "comunicación",
        "formulation": "formulación",
        "method": "método",
        "reasoning": "razonamiento",
        "implementation": "implementación",
        "validation": "validación",
        "interpretation": "interpretación",
        "results": "resultados",
        "biological": "biológica",
        "multivariate": "multivariante",
        "preprocessing": "preprocesamiento",
    },
    "en": {},
    "da": {
        "question": "spørgsmål",
        "estimand": "estimand",
        "design": "design",
        "data": "data",
        "quality": "kvalitet",
        "provenance": "proveniens",
        "reproducibility": "reproducerbarhed",
        "statistical": "statistisk",
        "model": "model",
        "sensitivity": "følsomhed",
        "limitations": "begrænsninger",
        "communication": "kommunikation",
        "validation": "validering",
        "interpretation": "fortolkning",
    },
}

__all__ = ["CumulativeAssessmentRenderer"]
