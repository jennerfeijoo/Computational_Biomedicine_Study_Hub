"""Offline persistence adapters."""

from .sqlite_progress import SCHEMA_VERSION, SQLiteProgressRepository

__all__ = ["SCHEMA_VERSION", "SQLiteProgressRepository"]
