"""Normalize mechanically invalid scalar syntax in the semester-one YAML corpus.

The original curriculum uses many compact localized mappings such as
``{es: ¿...?, en: What ...?, da: Hvad ...?}``.  Question marks, colons,
braces, and backticks in those unquoted values make otherwise valid content
impossible to parse with a standards-compliant safe YAML loader.

This script quotes those scalar values without translating or otherwise
changing their text.  It is intentionally narrow and idempotent.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "academic_content" / "semester_1"
LOCALE_LINE = re.compile(r"^(\s*)(es|en|da):\s*(\S.*)$")
BACKTICK_VALUE = re.compile(r"^(\s*(?:-\s+)?[^:#\n]+:\s*)(`.*)$")
BACKTICK_ITEM = re.compile(r"^(\s*-\s+)(`.*)$")


def _delimiter_at_depth(text: str, start: int, delimiter: str) -> int:
    depth = 1
    index = start
    while index < len(text):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return -1
        if depth == 1 and text.startswith(delimiter, index):
            return index
        index += 1
    return -1


def _closing_brace(text: str, start: int) -> int:
    depth = 1
    for index in range(start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return -1


def _quote_localized_flow_mappings(line: str) -> str:
    cursor = 0
    while True:
        start = line.find("{es:", cursor)
        if start < 0:
            return line

        es_start = start + len("{es:")
        en_marker = _delimiter_at_depth(line, es_start, ", en:")
        if en_marker < 0:
            cursor = es_start
            continue
        en_start = en_marker + len(", en:")
        da_marker = _delimiter_at_depth(line, en_start, ", da:")
        if da_marker < 0:
            cursor = en_start
            continue
        da_start = da_marker + len(", da:")
        end = _closing_brace(line, da_start)
        if end < 0:
            cursor = da_start
            continue

        values = {
            "es": line[es_start:en_marker].strip(),
            "en": line[en_start:da_marker].strip(),
            "da": line[da_start:end].strip(),
        }
        replacement = json.dumps(values, ensure_ascii=False)
        line = f"{line[:start]}{replacement}{line[end + 1 :]}"
        cursor = start + len(replacement)


def normalize_line(line: str) -> str:
    """Return a semantically equivalent line with ambiguous scalars quoted."""
    line = _quote_localized_flow_mappings(line)

    locale_match = LOCALE_LINE.match(line)
    if locale_match:
        indent, locale, value = locale_match.groups()
        if not value.startswith(("'", '"', "|", ">", "{", "[")):
            return f"{indent}{locale}: {json.dumps(value, ensure_ascii=False)}"

    backtick_match = BACKTICK_VALUE.match(line)
    if backtick_match:
        prefix, value = backtick_match.groups()
        return f"{prefix}{json.dumps(value, ensure_ascii=False)}"

    item_match = BACKTICK_ITEM.match(line)
    if item_match:
        prefix, value = item_match.groups()
        return f"{prefix}{json.dumps(value, ensure_ascii=False)}"

    return line


def normalize_text(text: str) -> str:
    """Normalize a complete YAML document while preserving its newline style."""
    newline = "\r\n" if "\r\n" in text else "\n"
    trailing_newline = text.endswith(("\n", "\r"))
    normalized = newline.join(normalize_line(line) for line in text.splitlines())
    return normalized + (newline if trailing_newline else "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write normalized files; otherwise only report files that would change",
    )
    args = parser.parse_args()

    changed: list[Path] = []
    for path in sorted(ROOT.rglob("*.yaml")):
        original = path.read_text(encoding="utf-8")
        normalized = normalize_text(original)
        if normalized == original:
            continue
        changed.append(path)
        if args.write:
            path.write_text(normalized, encoding="utf-8", newline="")

    verb = "normalized" if args.write else "would normalize"
    print(f"{verb} {len(changed)} YAML files")
    for path in changed:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
