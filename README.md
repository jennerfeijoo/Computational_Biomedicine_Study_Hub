# Computational Biomedicine Study Hub

Offline-first desktop study companion for the MSc in Computational Biomedicine.

The application will combine concise theory, worked examples, executable code, problem-solving guidance, common mistakes, and revision tools for the programme's courses. It is designed to grow semester by semester without forcing every course into the same internal structure.

## Initial scope

The first release targets the four first-semester courses:

- **DM857** — Introduction to Programming
- **DM847** — Introduction to Bioinformatics
- **BMB830** — Biostatistics in R I
- **BMB831** — Biostatistics in R II

## Design principles

- **Course-specific structure:** every course may use a different learning layout.
- **Shared application shell:** navigation, search, settings, persistence, and revision tools remain consistent.
- **Offline-first:** the essential learning material must remain usable without internet access.
- **Expandable:** later semesters are added as independent course modules.
- **Testable:** application logic and content validation are covered by automated tests.
- **Reproducible:** Python dependencies and development tooling are explicitly declared.

## Technology

- Python 3.11+
- PySide6
- `src/` package layout
- pytest
- Ruff
- mypy

## Development approach

The project is developed in small, reviewable increments. The first increment establishes the package, quality tooling, and a minimal executable application shell before course-specific content is added.

## Status

Early development.
