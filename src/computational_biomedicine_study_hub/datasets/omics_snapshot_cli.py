"""Command-line interface for registered public-omics snapshot validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .omics_snapshot import (
    DEFAULT_OMICS_PLAN_FILENAME,
    OmicsSnapshotSeverity,
    inspect_public_omics_snapshot,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cb-omics-inspect",
        description=(
            "Validate a declared local snapshot for one registered public omics source and "
            "optionally write a deterministic SHA-256 manifest. No remote content is downloaded."
        ),
    )
    parser.add_argument("source_id", help="Stable source ID from the public omics registry.")
    parser.add_argument("directory", help="Directory containing the local snapshot and plan.")
    parser.add_argument(
        "--plan",
        default=DEFAULT_OMICS_PLAN_FILENAME,
        help=f"Relative plan path inside the snapshot directory (default: {DEFAULT_OMICS_PLAN_FILENAME}).",
    )
    parser.add_argument(
        "--manifest",
        help="Optional output path for the generated JSON manifest.",
    )
    return parser


def _summary(
    source_id: str,
    report_valid: bool,
    artifact_count: int,
    error_count: int,
    warning_count: int,
) -> str:
    status = "VALID" if report_valid else "INVALID"
    return (
        f"Public omics snapshot: {status}\n"
        f"Source: {source_id}\n"
        f"Artifacts profiled: {artifact_count}\n"
        f"Errors: {error_count}\n"
        f"Warnings: {warning_count}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Validate one local snapshot and return a process-compatible status code."""

    arguments = _parser().parse_args(argv)
    source_id = cast(str, arguments.source_id)
    directory = Path(cast(str, arguments.directory))
    plan_filename = cast(str, arguments.plan)
    manifest_argument = cast(str | None, arguments.manifest)

    try:
        report = inspect_public_omics_snapshot(
            directory,
            source_id=source_id,
            plan_filename=plan_filename,
        )
    except ValueError as error:
        print(f"Public omics snapshot: INVALID\nERROR source-registry: {error}")
        return 2

    error_count = sum(
        issue.count for issue in report.issues if issue.severity is OmicsSnapshotSeverity.ERROR
    )
    warning_count = sum(
        issue.count for issue in report.issues if issue.severity is OmicsSnapshotSeverity.WARNING
    )
    print(
        _summary(
            report.source.source_id,
            report.valid,
            len(report.artifacts),
            error_count,
            warning_count,
        )
    )
    print(f"Fingerprint: {report.fingerprint}")

    for issue in report.issues:
        location_parts = tuple(
            value
            for value in (
                f"role={issue.role}" if issue.role else None,
                f"path={issue.relative_path}" if issue.relative_path else None,
            )
            if value is not None
        )
        location = f" [{' '.join(location_parts)}]" if location_parts else ""
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
