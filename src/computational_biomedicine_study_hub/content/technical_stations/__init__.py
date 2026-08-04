"""Authored artifact-based technical reasoning stations."""

from .dm847_alignment import DM847_ALIGNMENT_STATIONS
from .dm847_hmm import DM847_HMM_STATIONS
from .dm847_index import DM847_INDEX_STATIONS
from .dm847_mapping import DM847_MAPPING_STATIONS
from .dm857_project import DM857_PROJECT_STATIONS
from .dm857_project import PROJECT_ID as DM857_PROJECT_ID

DM847_TECHNICAL_STATIONS = (
    *DM847_MAPPING_STATIONS,
    *DM847_ALIGNMENT_STATIONS,
    *DM847_INDEX_STATIONS,
    *DM847_HMM_STATIONS,
)

ALL_TECHNICAL_STATIONS = (
    *DM847_TECHNICAL_STATIONS,
    *DM857_PROJECT_STATIONS,
)

STATIONS_BY_LAB = {
    "dm847.lab01.short-read-mapping": DM847_MAPPING_STATIONS,
    "dm847.lab02.pairwise-alignment": DM847_ALIGNMENT_STATIONS,
    "dm847.lab03.sequence-indexes": DM847_INDEX_STATIONS,
    "dm847.lab04.hidden-markov-models": DM847_HMM_STATIONS,
    DM857_PROJECT_ID: DM857_PROJECT_STATIONS,
}

__all__ = [
    "ALL_TECHNICAL_STATIONS",
    "DM847_TECHNICAL_STATIONS",
    "DM857_PROJECT_ID",
    "DM857_PROJECT_STATIONS",
    "STATIONS_BY_LAB",
]
