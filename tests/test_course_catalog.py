from __future__ import annotations

from computational_biomedicine_study_hub.courses import COURSES, courses_for_semester
from computational_biomedicine_study_hub.courses.catalog import validate_catalog


def test_first_semester_catalog_contains_expected_courses() -> None:
    courses = courses_for_semester(1)

    assert {course.code for course in courses} == {
        "DM857",
        "DM847",
        "BMB830",
        "BMB831",
    }
    assert sum(course.ects for course in courses) == 30


def test_course_routes_are_unique_and_stable() -> None:
    validate_catalog(COURSES)

    assert len({course.route for course in COURSES}) == len(COURSES)
    assert {course.route for course in COURSES} == {
        "course/dm857",
        "course/dm847",
        "course/bmb830",
        "course/bmb831",
    }
