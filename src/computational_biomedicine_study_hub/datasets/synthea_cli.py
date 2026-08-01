"""Command-line interface for local Synthea CSV snapshot inspection."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .synthea_snapshot import IssueSeverity, inspect_synthea_csv_directory


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cb-synthea-inspect",
        description=(
            "Validate core Synthea CSV tables and write a reproducibility manifest. "
            "The data remain explicitly synthetic."
        ),
    )
    parser.add_argument("directory", help="Directory containing extracted Synthea CSV files.")
    parser.add_argument(
        "--manifest",
        help="Optional output path for the JSON manifest.",
    )
    parser.add_argument(
        "--source-label",
        default="local-synthea-csv-snapshot",
        help="Human-readable source label stored in the manifest.",
    )
    return parser


def _summary(report_valid: bool, table_count: int, error_count: int, warning_count: int) -> str:
    status = "VALID" if report_valid else "INVALID"
    return (
        f"Synthea snapshot: {status}\n"
        f"Tables profiled: {table_count}\n"
        f"Errors: {error_count}\n"
        f"Warnings: {warning_count}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Inspect one extracted snapshot and return a process-compatible status code."""

    arguments = _parser().parse_args(argv)
    directory = Path(cast(str, arguments.directory))
    source_label = cast(str, arguments.source_label)
    manifest_argument = cast(str | None, arguments.manifest)

    report = inspect_synthea_csv_directory(directory, source_label=source_label)
    error_count = sum(
        issue.count for issue in report.issues if issue.severity is IssueSeverity.ERROR
    )
    warning_count = sum(
        issue.count for issue in report.issues if issue.severity is IssueSeverity.WARNING
    )
    print(_summary(report.valid, len(report.tables), error_count, warning_count))
    print(f"Fingerprint: {report.fingerprint}")

    for issue in report.issues:
        location = f" [{issue.filename}]" if issue.filename else ""
        print(
            f"{issue.severity.value.upper()}{location} {issue.code}: "
            f"{issue.message} (count={issue.count})"
        )

    if manifest_argument is not None:
        manifest_path = Path(manifest_argument)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(report.to_json() + "\n", encoding="utf-8")
        print(f"Manifest written: {manifest_path}")

    return 0 if report.valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
