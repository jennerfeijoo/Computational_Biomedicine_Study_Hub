"""Registered multi-file workspace templates for computational laboratories."""

from __future__ import annotations

from .dm847_workspace_01 import DM847_LAB_01_WORKSPACE
from .workspaces import DM857_LAB_01_WORKSPACE

WORKSPACE_TEMPLATES = {
    DM857_LAB_01_WORKSPACE.lab_id: DM857_LAB_01_WORKSPACE,
    DM847_LAB_01_WORKSPACE.lab_id: DM847_LAB_01_WORKSPACE,
}

__all__ = [
    "DM847_LAB_01_WORKSPACE",
    "DM857_LAB_01_WORKSPACE",
    "WORKSPACE_TEMPLATES",
]
