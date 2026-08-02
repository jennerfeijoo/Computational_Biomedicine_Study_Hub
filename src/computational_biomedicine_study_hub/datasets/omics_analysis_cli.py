"""Command-line interface for omics analytical-input validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .omics_analysis import (
    DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME,
    OmicsAnalysisSeverity,
    inspect_omics_analysis_input,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cb-omics-analysis-inspect",
        description=(
            "Validate lineage, a feature-by-sample assay, and one-row-per-sample metadata "
            "before omics modelling. No normalization, imputation, or modelling is performed."
        ),
    )
    parser.add_argument("source_id", help="Stable source ID from the public omics registry.")
    parser.add_argument("directory", help="Directory containing analysis_plan.json and inputs.")
    parser.add_argument(
        "--plan",
        default=DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME,
        help=(
            "Relative analysis-plan path inside the directory "
            f"(default: {DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME})."
        ),
    )
    parser.add_argument("--manifest", help="Optional output path for the transition manifest.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Inspect one declared analytical input and return a process-compatible status."""

    arguments = _parser().parse_args(argv)
    source_id = cast(str, arguments.source_id)
    directory = Path(cast(str, arguments.directory))
    plan_filename = cast(str, arguments.plan)
    manifest_argument = cast(str | None, arguments.manifest)

    try:
        report = inspect_omics_analysis_input(
            directory,
            source_id=source_id,
            plan_filename=plan_filename,
        )
    except ValueError as error:
        print(f"Omics analytical input: INVALID\nERROR source-registry: {error}")
        return 2

    error_count = sum(
        issue.count for issue in report.issues if issue.severity is OmicsAnalysisSeverity.ERROR
    )
    warning_count = sum(
        issue.count for issue in report.issues if issue.severity is OmicsAnalysisSeverity.WARNING
    )
    status = "VALID" if report.valid else "INVALID"
    feature_count = 0 if report.assay is None else report.assay.feature_count
    sample_count = 0 if report.assay is None else report.assay.sample_count
    print(
        f"Omics analytical input: {status}\n"
        f"Source: {report.source.source_id}\n"
        f"Features: {feature_count}\n"
        f"Samples: {sample_count}\n"
        f"Sample sets match: {str(report.sample_sets_match).upper()}\n"
        f"Errors: {error_count}\n"
        f"Warnings: {warning_count}"
    )
    print(f"Fingerprint: {report.fingerprint}")

    for issue in report.issues:
        location_parts = tuple(
            value
            for value in (
                f"path={issue.relative_path}" if issue.relative_path else None,
                f"column={issue.column}" if issue.column else None,
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
