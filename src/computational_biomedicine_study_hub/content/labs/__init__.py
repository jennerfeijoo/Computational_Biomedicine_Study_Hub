"""Authored internal preparation laboratories for computational biomedicine."""

from .dm847_lab_01 import DM847_LAB_01
from .dm857_lab_01 import DM857_LAB_01

LABS = (DM857_LAB_01, DM847_LAB_01)

__all__ = ["DM847_LAB_01", "DM857_LAB_01", "LABS"]
