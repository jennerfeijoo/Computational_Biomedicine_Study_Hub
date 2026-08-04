"""Authored artifact-based technical reasoning stations."""

from dataclasses import replace

from .dm847 import DM847_TECHNICAL_STATIONS as _DM847_RAW_STATIONS

_LAB_ID_ALIASES = {
    "dm847.lab01.sequence-mapping": "dm847.lab01.short-read-mapping",
    "dm847.lab03.sequence-index": "dm847.lab03.sequence-indexes",
    "dm847.lab04.hidden-markov-model": "dm847.lab04.hidden-markov-models",
}

DM847_TECHNICAL_STATIONS = tuple(
    replace(
        station,
        lab_id=_LAB_ID_ALIASES.get(station.lab_id, station.lab_id),
        source_basis=tuple(_LAB_ID_ALIASES.get(item, item) for item in station.source_basis),
    )
    for station in _DM847_RAW_STATIONS
)

STATIONS_BY_LAB = {
    lab_id: tuple(station for station in DM847_TECHNICAL_STATIONS if station.lab_id == lab_id)
    for lab_id in {
        "dm847.lab01.short-read-mapping",
        "dm847.lab02.pairwise-alignment",
        "dm847.lab03.sequence-indexes",
        "dm847.lab04.hidden-markov-models",
    }
}

__all__ = ["DM847_TECHNICAL_STATIONS", "STATIONS_BY_LAB"]
