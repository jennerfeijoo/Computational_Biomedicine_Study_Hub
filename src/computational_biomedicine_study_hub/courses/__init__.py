"""Independent course modules and the central catalog."""

from __future__ import annotations

from .catalog import COURSES, courses_for_semester
from .models import CourseRegistration

__all__ = ["COURSES", "CourseRegistration", "courses_for_semester"]
