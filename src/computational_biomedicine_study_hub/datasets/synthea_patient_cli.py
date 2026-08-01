"""Command-line interface for deterministic Synthea patient-table derivation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from .synthea_patient_table import (
    PatientTableBuildError,
    PatientTableConfig,
    build_synthea_patient_table,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cb-synthea-build-patient-table",
        description=(
            "Build a leakage-aware one-row-per-patient analytical table from a validated "
            "Synthea CSV snapshot. The output remains synthetic evidence."
        ),
    )
    parser.add_argument("directory", help="Directory containing extracted Synthea CSV files.")
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV path for the derived patient table.",
    )
    parser.add_argument(
        "--metadata",
        help="Optional metadata JSON path. Defaults beside the output CSV.",
    )
    parser.add_argument(
        "--source-label",
        default="local-synthea-csv-snapshot",
        help="Human-readable source label used during snapshot inspection.",
    )
    parser.add_argument(
        "--window-days",
        type=int,
        default=365,
        help="Number of days in the strict pre-index feature window.",
    )
    parser.add_argument("--train-percent", type=int, default=70)
    parser.add_argument("--validation-percent", type=int, default=15)
    parser.add_argument("--test-percent", type=int, default=15)
    parser.add_argument(
        "--split-salt",
        default="synthea-patient-table-v1",
        help="Stable salt for deterministic patient-level split assignment.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Build one analytical table and return a process-compatible status code."""

    arguments = _parser().parse_args(argv)
    try:
        config = PatientTableConfig(
            window_days=cast(int, arguments.window_days),
            split_percentages=(
                cast(int, arguments.train_percent),
                cast(int, arguments.validation_percent),
                cast(int, arguments.test_percent),
            ),
            split_salt=cast(str, arguments.split_salt),
        )
        report = build_synthea_patient_table(
            Path(cast(str, arguments.directory)),
            Path(cast(str, arguments.output)),
            metadata_path=(
                Path(cast(str, arguments.metadata)) if arguments.metadata is not None else None
            ),
            config=config,
            source_label=cast(str, arguments.source_label),
        )
    except (PatientTableBuildError, ValueError) as error:
        print(f"Synthea patient-table build failed: {error}")
        return 2

    print("Synthea patient table: BUILT")
    print(f"Rows: {report.row_count}")
    print(f"Excluded without index encounter: {report.excluded_without_index}")
    print(f"Output SHA-256: {report.output_sha256}")
    print(f"Artifact fingerprint: {report.artifact_fingerprint}")
    print(f"Output file: {report.output_filename}")
    print(f"Metadata file: {report.metadata_filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
