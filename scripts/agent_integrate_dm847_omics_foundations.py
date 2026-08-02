"""Temporary branch integration script for the DM847 M01/M10 review."""

from __future__ import annotations

from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Could not find {label}")
    return text.replace(old, new, 1)


def update_init() -> None:
    path = Path("src/computational_biomedicine_study_hub/content/dm847/__init__.py")
    text = path.read_text()

    anchor = """from .book_grounded_motifs_networks import (
    apply_motif_network_extensions,
    update_motif_network_audit,
    update_motif_network_source_catalog,
)
"""
    text = replace_once(
        text,
        anchor,
        anchor
        + """from .book_grounded_omics_foundations import (
    apply_omics_foundations_extensions,
    update_omics_foundations_audit,
)
""",
        "motif/network import block",
    )

    text = replace_once(
        text,
        """DM847_MODULE_SOURCE_AUDIT = update_motif_network_audit(
    update_hmm_bwt_audit(_BASE_DM847_MODULE_SOURCE_AUDIT)
)
""",
        """DM847_MODULE_SOURCE_AUDIT = update_omics_foundations_audit(
    update_motif_network_audit(
        update_hmm_bwt_audit(_BASE_DM847_MODULE_SOURCE_AUDIT)
    )
)
""",
        "cumulative audit block",
    )

    text = replace_once(
        text,
        ") = apply_motif_network_extensions(\n",
        ") = apply_omics_foundations_extensions(\n    apply_motif_network_extensions(\n",
        "extension application opening",
    )
    application_end = """            )
        )
    )
)

_LOCALIZED_MODULES = (
"""
    text = replace_once(
        text,
        application_end,
        """            )
        )
    )
    )
)

_LOCALIZED_MODULES = (
""",
        "extension application closing",
    )

    old_versions = """_CONTENT_VERSIONS = (
    "1.0.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
)
"""
    new_versions = """_CONTENT_VERSIONS = (
    "1.1.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
)
"""
    text = replace_once(text, old_versions, new_versions, "content versions")
    text = replace_once(
        text,
        '    "apply_motif_network_extensions",\n',
        '    "apply_motif_network_extensions",\n'
        '    "apply_omics_foundations_extensions",\n',
        "public extension export",
    )
    path.write_text(text)


def update_reviewed_sets() -> None:
    paths = (
        Path("tests/test_dm847_core_modules.py"),
        Path("tests/test_dm847_book_grounded_audit.py"),
        Path("tests/test_dm847_hmm_bwt_review.py"),
        Path("tests/test_dm847_motif_network_review.py"),
    )
    for path in paths:
        text = path.read_text()
        text = replace_once(
            text,
            '    "dm847.m03",\n',
            '    "dm847.m01",\n    "dm847.m03",\n',
            f"reviewed set opening in {path}",
        )
        text = replace_once(
            text,
            '    "dm847.m09",\n}',
            '    "dm847.m09",\n    "dm847.m10",\n}',
            f"reviewed set closing in {path}",
        )
        path.write_text(text)

    path = Path("tests/test_dm847_motif_network_review.py")
    text = path.read_text()
    text = replace_once(
        text,
        """    assert {module_id for module_id, state in state_by_module.items() if state == "pending"} == {
        "dm847.m01",
        "dm847.m02",
        "dm847.m07",
        "dm847.m10",
    }
""",
        """    assert {module_id for module_id, state in state_by_module.items() if state == "pending"} == {
        "dm847.m02",
        "dm847.m07",
    }
""",
        "motif/network pending set",
    )
    path.write_text(text)


def update_docs() -> None:
    path = Path("docs/dm847-book-grounded-audit.md")
    text = path.read_text()
    text = replace_once(
        text,
        "| M01 Molecular information | Active course scope; biological-question framing and sequence orientation | Pending |",
        "| M01 Molecular information | Volume I chapter 1 plus active course scope | Consistent |",
        "M01 audit row",
    )
    text = replace_once(
        text,
        "| M10 OMICS learning | Volume II chapter 8 plus active course scope | Pending |",
        "| M10 OMICS learning | Volume II chapter 8 plus active course scope | Consistent |",
        "M10 audit row",
    )
    insertion = """
## Completed focused review: M01

The existing module already covered molecular information flow, sequence alphabets, ambiguity, strand orientation, coordinate systems, regulation, bacterial genetics, phages, provenance, and biological question framing.

The missing boundary was an explicit computational problem contract. The extension now covers:

- inputs, outputs, alphabets, orientation, and coordinate conventions;
- overlap and reverse-complement policies;
- invalid symbols, empty patterns, and short-input edge cases;
- known-answer examples and invariants before algorithm selection;
- separation of computational correctness from biological interpretation.

The deterministic example searches canonical DNA on the supplied strand with zero-based positions and overlapping matches:

```text
[0, 2]
```

Stable IDs:

- `m01.bg.o1`
- `computational-problem-contracts`
- `m01.bg.e01`
- `m01.bg.p01`
- `dm847.m01.book.001`

Content version: `1.1.0`.

## Completed focused review: M10

The existing module already covered OMICS matrix design, preprocessing, leakage, PCA, clustering, supervised learning, nested validation, metrics, interpretation, and reproducibility.

The missing algorithmic boundary was the relation between clustering objective, initialization, assignment type, and scientific stability. The extension now covers:

- hard k-means assignments and distortion;
- Lloyd updates and local optima;
- multiple restarts and comparable objectives;
- soft responsibilities that sum to one;
- hierarchical distance and linkage choices;
- dependence on transformation, scaling, feature selection, and batch;
- resampling stability and external replication.

The deterministic example compares two Lloyd restarts:

```text
{'left_start': ((1.0, 12.5), 11.286), 'right_start': ((5.5, 20.0), 17.929)}
```

Stable IDs:

- `m10.bg.o1`
- `clustering-objectives-initialization-and-stability`
- `m10.bg.e01`
- `m10.bg.p01`
- `dm847.m10.book.001`

Content version: `1.1.0`.
"""
    text = replace_once(text, "\n## Source boundary\n", insertion + "\n## Source boundary\n", "docs insertion")
    path.write_text(text)


def main() -> None:
    update_init()
    update_reviewed_sets()
    update_docs()


if __name__ == "__main__":
    main()
