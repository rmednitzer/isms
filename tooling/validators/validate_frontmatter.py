#!/usr/bin/env python3
"""
Validate YAML front-matter on every governance markdown file.

Scans docs/, template/governance/, template/operations/, instance/governance/,
instance/operations/ for .md files and validates their front-matter against
tooling/schemas/frontmatter.schema.json.

Exits 0 on success, 1 on violations, 2 on infrastructure errors.

Copyright 2026 isms contributors
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _common import (
    GOVERNANCE_SCAN_ROOTS,
    REPO_ROOT,
    iter_markdown,
    parse_frontmatter,
)
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = REPO_ROOT / "tooling" / "schemas" / "frontmatter.schema.json"


def extract_frontmatter(path: Path) -> dict | None:
    """Return normalised front-matter for a markdown file, or None.

    Kept as a module-level function for backwards compatibility with tests.
    """
    return parse_frontmatter(path, normalise=True)


def validate_file(path: Path, validator: Draft202012Validator) -> list[str]:
    fm = extract_frontmatter(path)
    if fm is None:
        return [f"{path}: missing front-matter"]
    return [
        f"{path}: {e.message} (at {'/'.join(str(p) for p in e.absolute_path)})"
        for e in validator.iter_errors(fm)
    ]


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"ERROR: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        return 2
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors: list[str] = []
    count = 0
    for md in iter_markdown(GOVERNANCE_SCAN_ROOTS):
        count += 1
        errors.extend(validate_file(md, validator))

    print(f"Validated front-matter on {count} markdown files.")
    if errors:
        print(f"{len(errors)} violations:")
        for e in errors:
            print(f"  {e}")
        return 1
    print("All front-matter valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
