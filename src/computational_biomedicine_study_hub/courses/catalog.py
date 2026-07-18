"""Central course catalog assembled from independent course modules."""

from __future__ import annotations

from collections.abc import Iterable

from .bmb830 import COURSE as BMB830
from .bmb831 import COURSE as BMB831
from .dm847 import COURSE as DM847
from .dm857 import COURSE as DM857
from .models import CourseRegistration


COURSES: tuple[CourseRegistration, ...] = tuple(
    sorted(
        (DM857, DM847, BMB830, BMB831),
        key=lambda course: (course.semester, course.code),
    )
)


def validate_catalog(courses: Iterable[CourseRegistration] = COURSES) -> None:
    """Reject duplicate codes and routes before the UI is constructed."""
    course_list = tuple(courses)
    codes = [course.code.casefold() for course in course_list]
    routes = [course.route for course in course_list]

    if len(codes) != len(set(codes)):
        raise ValueError("Course codes must be unique.")
    if len(routes) != len(set(routes)):
        raise ValueError("Course routes must be unique.")


def courses_for_semester(semester: int) -> tuple[CourseRegistration, ...]:
    """Return the registered courses for one semester."""
    return tuple(course for course in COURSES if course.semester == semester)


validate_catalog()
