"""Academic integrity tests for the BMB831 authored modules."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb831 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    MODULES,
    OBJECTIVE_QUESTION_BANKS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def test_bmb831_registers_nine_complete_modules() -> None:
    expected_ids = tuple(f"bmb831.m{number:02d}" for number in range(1, 10))
    reviewed_extensions = {f"bmb831.m{number:02d}" for number in range(2, 6)}
    expected_versions = {
        module_id: "1.1.0" if module_id in reviewed_extensions else "1.0.0"
        for module_id in expected_ids
    }
    assert tuple(module.module_id for module in MODULES) == expected_ids
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 9
    assert set(OBJECTIVE_QUESTION_BANKS) == set(expected_ids)
    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 144

    for bundle in BUNDLES:
        module = bundle.module
        expected_assessment_count = 9 if module.module_id in reviewed_extensions else 8
        assert module.course_code == "BMB831"
        assert len(module.objectives) >= 4
        assert len(module.concepts) >= 4
        assert len(module.worked_examples) >= 2
        assert len(module.practice_exercises) >= 6
        assert len(module.assessment_items) == expected_assessment_count
        assert len(bundle.objective_question_bank) == 16
        assert bundle.content_version == expected_versions[module.module_id]
        assert all(can_execute_r(example.code) for example in module.worked_examples)


def _module_text(index: int) -> str:
    module = MODULES[index]
    return " ".join(
        (
            module.title,
            module.summary,
            *(objective.statement for objective in module.objectives),
            *(concept.title for concept in module.concepts),
            *(concept.body for concept in module.concepts),
            *(practice.explanation for practice in module.practice_exercises),
        )
    ).casefold()


def test_bmb831_synthea_module_preserves_scientific_boundaries() -> None:
    text = _module_text(0)
    assert "synthea" in text
    assert "sintétic" in text
    assert "paciente" in text
    assert "cardinalidad" in text
    assert "fuga temporal" in text
    assert "ómic" in text
    assert "no sustit" in text


def test_bmb831_omics_modules_cover_matrix_and_inference_contracts() -> None:
    matrix_text = _module_text(1)
    differential_text = _module_text(2)

    assert "matriz" in matrix_text
    assert "metadata" in matrix_text
    assert "normalización" in matrix_text
    assert "muestra" in matrix_text
    assert "lote" in matrix_text
    assert "sesgo composicional" in matrix_text
    assert "factor de normalización" in matrix_text

    assert "contraste" in differential_text
    assert "diseño" in differential_text
    assert "dispersión" in differential_text
    assert "tamaño del efecto" in differential_text
    assert "multiplicidad" in differential_text
    assert "benjamini-hochberg" in differential_text
    assert "empírico-bayes" in differential_text
    assert "préstamo de información" in differential_text


def test_bmb831_multivariate_and_visualization_modules_are_advanced() -> None:
    multivariate_text = _module_text(3)
    visualization_text = _module_text(4)

    assert "pca" in multivariate_text
    assert "scores" in multivariate_text
    assert "loadings" in multivariate_text
    assert "distancia" in multivariate_text
    assert "clustering" in multivariate_text
    assert "estabilidad" in multivariate_text
    assert "fuga" in multivariate_text
    assert "min(p, n - 1)" in multivariate_text
    assert "subespacio" in multivariate_text

    assert "pregunta" in visualization_text
    assert "unidad analítica" in visualization_text
    assert "volcano" in visualization_text
    assert "ma plot" in visualization_text
    assert "heatmap" in visualization_text
    assert "incertidumbre" in visualization_text
    assert "accesibilidad" in visualization_text
    assert "reproduc" in visualization_text
    assert "desviación estándar" in visualization_text
    assert "error estándar" in visualization_text
    assert "intervalo predictivo" in visualization_text


def test_bmb831_final_modules_cover_public_omics_proteins_and_reporting() -> None:
    public_omics_text = _module_text(5)
    protein_text = _module_text(6)
    interpretation_text = _module_text(7)
    report_text = _module_text(8)

    assert "transcript" in public_omics_text
    assert "proteóm" in public_omics_text
    assert "snapshot" in public_omics_text
    assert "checksum" in public_omics_text

    assert "secuencia" in protein_text
    assert "interpro" in protein_text
    assert "uniprot" in protein_text
    assert "pdb" in protein_text
    assert "alphafold" in protein_text

    assert "universo" in interpretation_text
    assert "enriquecimiento" in interpretation_text
    assert "pathway" in interpretation_text
    assert "red" in interpretation_text
    assert "circular" in interpretation_text

    assert "publicación" in report_text
    assert "estimando" in report_text
    assert "validez" in report_text
    assert "informe" in report_text
    assert "inglés" in report_text


def test_bmb831_corrects_public_sources_and_hydropathy_example() -> None:
    public_sources = LOCALIZED_BUNDLES[5].localized_module.tutor_support.source_basis
    assert any(source.endswith("/limma.html") for source in public_sources)
    assert all("/limpa.html" not in source for source in public_sources)

    for locale in AppLocale:
        bundle = LOCALIZED_BUNDLES[6].materialize(locale)
        example = next(
            item for item in bundle.module.worked_examples if item.example_id == "m07.e02"
        )
        assert example.expected_output == "best_start=5\nbest_score=3.60"
        assert "ILMV" in example.explanation


def test_bmb831_locales_preserve_assessment_identity() -> None:
    for localized_bundle in LOCALIZED_BUNDLES:
        materialized = {locale: localized_bundle.materialize(locale) for locale in AppLocale}
        reference = materialized[AppLocale.SPANISH_SPAIN]
        reference_ids = tuple(item.item_id for item in reference.objective_question_bank)
        reference_option_ids = tuple(item.option_ids for item in reference.objective_question_bank)
        reference_correct_ids = tuple(
            item.correct_option_ids for item in reference.objective_question_bank
        )

        for locale, bundle in materialized.items():
            assert bundle.module.module_id == reference.module.module_id
            assert bundle.module.title.strip()
            assert tuple(item.item_id for item in bundle.objective_question_bank) == reference_ids
            assert (
                tuple(item.option_ids for item in bundle.objective_question_bank)
                == reference_option_ids
            )
            assert (
                tuple(item.correct_option_ids for item in bundle.objective_question_bank)
                == reference_correct_ids
            ), locale


def test_bmb831_activity_ids_are_unique_within_and_across_modules() -> None:
    all_identifiers: list[str] = []
    for bundle in BUNDLES:
        module = bundle.module
        local_identifiers = (
            *(item.exercise_id for item in module.practice_exercises),
            *(item.item_id for item in module.assessment_items),
            *(item.item_id for item in bundle.objective_question_bank),
        )
        local_number = module.module_id.rsplit("m", maxsplit=1)[-1]
        assert all(
            identifier.startswith((f"bmb831.m{local_number}.", f"m{local_number}."))
            for identifier in local_identifiers
        )
        assert len(local_identifiers) == len(set(local_identifiers))
        all_identifiers.extend(local_identifiers)

    assert len(all_identifiers) == len(set(all_identifiers))
