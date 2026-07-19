"""Regression tests for the ordered DM857 authored-module catalog."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import MODULES


def test_dm857_catalog_contains_modules_one_through_fourteen_in_order() -> None:
    assert [module.module_id for module in MODULES] == [
        f"dm857.m{number:02d}" for number in range(1, 15)
    ]
