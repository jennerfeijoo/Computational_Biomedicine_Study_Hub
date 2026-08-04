"""Domain and authored-content tests for artifact-based technical stations."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from computational_biomedicine_study_hub.content.technical_stations import (
    DM847_TECHNICAL_STATIONS,
    STATIONS_BY_LAB,
)
from computational_biomedicine_study_hub.i18n.locales import SUPPORTED_LOCALES, AppLocale
from computational_biomedicine_study_hub.learning.technical_stations import (
    TechnicalStationAttempt,
    TechnicalStationKind,
    TechnicalStationSnapshot,
    render_technical_station_record,
)

_EXPECTED_LABS = {
    "dm847.lab01.short-read-mapping",
    "dm847.lab02.pairwise-alignment",
    "dm847.lab03.sequence-indexes",
    "dm847.lab04.hidden-markov-models",
}


def test_dm847_station_registry_has_four_stations_per_current_lab() -> None:
    assert len(DM847_TECHNICAL_STATIONS) == 16
    assert set(STATIONS_BY_LAB) == _EXPECTED_LABS
    assert all(len(stations) == 4 for stations in STATIONS_BY_LAB.values())
    assert {station.lab_id for station in DM847_TECHNICAL_STATIONS} == _EXPECTED_LABS
    assert len({station.station_id for station in DM847_TECHNICAL_STATIONS}) == 16


def test_station_content_is_complete_in_every_supported_locale() -> None:
    kinds = {station.kind for station in DM847_TECHNICAL_STATIONS}
    assert {
        TechnicalStationKind.CODE_READING,
        TechnicalStationKind.EXECUTION_TRACE,
        TechnicalStationKind.DEBUGGING,
        TechnicalStationKind.OUTPUT_INTERPRETATION,
        TechnicalStationKind.METHOD_SELECTION,
        TechnicalStationKind.COMPLEXITY_ANALYSIS,
        TechnicalStationKind.SCIENTIFIC_INTERPRETATION,
    } <= kinds

    for station in DM847_TECHNICAL_STATIONS:
        assert station.artifact.strip()
        assert station.source_basis
        for locale in SUPPORTED_LOCALES:
            assert station.title.text(locale)
            assert station.artifact_title.text(locale)
            assert station.prompt.text(locale)
            assert all(criterion.text.text(locale) for criterion in station.criteria)


def test_response_change_invalidates_prior_self_review() -> None:
    station = DM847_TECHNICAL_STATIONS[0]
    now = datetime(2026, 8, 4, 18, 0, tzinfo=UTC)
    attempt = TechnicalStationAttempt.new(station, now=now).with_response(
        "A sufficiently detailed technical explanation that exceeds the minimum response length."
    )
    for criterion in station.criteria:
        attempt = attempt.with_criterion(criterion.criterion_id, True)
    attempt = attempt.mark_reviewed(station)
    assert attempt.reviewed

    revised = attempt.with_response(
        "A revised technical explanation that must be reviewed again after its content changes."
    )

    assert not revised.reviewed
    assert revised.reviewed_at is None
    assert revised.checked_criteria == frozenset()


def test_mark_reviewed_requires_substantive_response_and_all_criteria() -> None:
    station = DM847_TECHNICAL_STATIONS[0]
    attempt = TechnicalStationAttempt.new(station).with_response("too short")
    with pytest.raises(ValueError, match="substantive"):
        attempt.mark_reviewed(station)

    attempt = attempt.with_response(
        "This response defines inputs, coordinates, boundary behaviour, and validation decisions."
    )
    with pytest.raises(ValueError, match="Every"):
        attempt.mark_reviewed(station)

    for criterion in station.criteria:
        attempt = attempt.with_criterion(criterion.criterion_id, True)
    reviewed = attempt.mark_reviewed(station)
    assert reviewed.reviewed
    assert reviewed.reviewed_at is not None


def test_snapshot_round_trip_and_completion_ratio() -> None:
    stations = STATIONS_BY_LAB["dm847.lab01.short-read-mapping"]
    station = stations[0]
    attempt = TechnicalStationAttempt.new(station).with_response(
        "This answer addresses the complete contract, boundary behaviour, and invalid inputs."
    )
    for criterion in station.criteria:
        attempt = attempt.with_criterion(criterion.criterion_id, True)
    attempt = attempt.mark_reviewed(station)
    snapshot = TechnicalStationSnapshot().with_attempt(attempt)

    restored = TechnicalStationSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    assert restored.completion_ratio(stations) == 0.25


def test_export_states_formative_boundary_without_exam_claim() -> None:
    station = DM847_TECHNICAL_STATIONS[0]
    attempt = TechnicalStationAttempt.new(station).with_response(
        "A technical explanation grounded in the concrete code artifact and its explicit contract."
    )
    rendered = render_technical_station_record(station, attempt, AppLocale.ENGLISH)

    assert "not an official exam simulation" in rendered
    assert "not" in rendered
    assert station.station_id in rendered
