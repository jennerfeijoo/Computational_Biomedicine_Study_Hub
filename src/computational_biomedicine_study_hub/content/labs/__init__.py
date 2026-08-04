"""Authored internal preparation laboratories for computational biomedicine."""

from .dm847_lab_01 import DM847_LAB_01
from .dm847_lab_02 import DM847_LAB_02
from .dm847_lab_03 import DM847_LAB_03
from .dm857_lab_01 import DM857_LAB_01
from .workspace_catalog import WORKSPACE_TEMPLATES
from .workspaces import WORKSPACE_TEMPLATES as _LEGACY_WORKSPACE_TEMPLATES

_LEGACY_WORKSPACE_TEMPLATES.update(WORKSPACE_TEMPLATES)

LABS = (DM857_LAB_01, DM847_LAB_01, DM847_LAB_02, DM847_LAB_03)

__all__ = [
    "DM847_LAB_01",
    "DM847_LAB_02",
    "DM847_LAB_03",
    "DM857_LAB_01",
    "LABS",
    "WORKSPACE_TEMPLATES",
]
