"""Platform-appropriate application data paths."""

from __future__ import annotations

import os
from pathlib import Path


def default_progress_database_path() -> Path:
    """Return an overrideable per-user path outside the source checkout."""
    override = os.environ.get("CB_STUDY_HUB_DATA_DIR", "").strip()
    if override:
        base = Path(override).expanduser()
    elif os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        base /= "ComputationalBiomedicineStudyHub"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        base /= "computational-biomedicine-study-hub"
    return base / "progress.sqlite3"


__all__ = ["default_progress_database_path"]
